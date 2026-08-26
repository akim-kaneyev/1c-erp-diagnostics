#!/usr/bin/env python3
"""Validate deterministic case-state identity, references and invalidation closure."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1
STATE_KEYS = {
    "schema_version",
    "case_id",
    "evidence",
    "runs",
    "claims",
    "documents",
    "gates",
    "active_index",
}
EVIDENCE_KEYS = {
    "id",
    "status",
    "derived_from",
    "run_id",
    "artifact_hash",
    "transformation",
    "tool",
    "tool_version",
    "limitations",
    "superseded_by",
    "invalidates_ids",
}
RUN_KEYS = {
    "id",
    "case_id",
    "status",
    "input_evidence_ids",
    "input_hashes",
    "release",
    "extension_set",
    "period",
    "tool",
    "tool_version",
    "operation",
    "limitations",
    "started_at",
    "completed_at",
    "superseded_by",
    "invalidates_ids",
}
CLAIM_KEYS = {
    "id",
    "status",
    "evidence_ids",
    "depends_on_claim_ids",
    "document_ids",
    "historical_document_ids",
    "superseded_by",
    "invalidates_ids",
}
DOCUMENT_KEYS = {
    "id",
    "status",
    "claim_ids",
    "superseded_by",
    "invalidates_ids",
}
GATE_KEYS = {"id", "status", "claim_ids"}
ACTIVE_INDEX_KEYS = {"run_id", "claim_ids", "document_ids"}

EVIDENCE_STATUSES = {"active", "stale", "superseded", "withdrawn"}
RUN_STATUSES = {"current", "stale", "superseded", "withdrawn"}
CLAIM_STATUSES = {
    "УСТАНОВЛЕНО",
    "ВЕРОЯТНО",
    "ТРЕБУЕТ ПРОВЕРКИ",
    "stale",
    "superseded",
    "withdrawn",
}
DOCUMENT_STATUSES = {"current", "historical", "superseded", "withdrawn"}
GATE_STATUSES = {"pending", "passed", "blocked", "failed", "stale", "not_required"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:\\?[\"']?(?:password|passwd|api[_.-]?key|access[_.-]?token|refresh[_.-]?token|"
    r"client[_.-]?secret|private[_.-]?key|sonar[_.-]?token|"
    r"aws[_.-]?secret[_.-]?access[_.-]?key)\\?[\"']?|"
    r"sonar\.(?:token|login))\s*[:=]"
)
BEARER_AUTHORIZATION = re.compile(
    r"(?i)\\?[\"']?authorization\\?[\"']?\s*[:=]\s*\\?[\"']?\s*bearer\s+\S{8,}"
)
JSON_UNICODE_ESCAPE = re.compile(r"\\+[uU]([0-9A-Fa-f]{4})")
ESCAPED_QUOTE = re.compile(r"\\+([\"'])")
CAMEL_CASE_BOUNDARY = re.compile(
    r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])"
)
CREDENTIAL_KEYS = {
    "password",
    "passwd",
    "api_key",
    "access_token",
    "refresh_token",
    "client_secret",
    "private_key",
    "sonar_token",
    "sonar_login",
    "authorization",
    "proxy_authorization",
    "aws_secret_access_key",
}
PRIVATE_KEY_MARKERS = (
    "BEGIN " + "PRIVATE KEY",
    "BEGIN " + "RSA PRIVATE KEY",
    "BEGIN " + "EC PRIVATE KEY",
    "BEGIN " + "OPENSSH PRIVATE KEY",
    "BEGIN " + "ENCRYPTED PRIVATE KEY",
)
PRIVATE_KEY_HEADER = re.compile(
    r"-----BEGIN [^-\r\n]{0,80}" + "PRIVATE KEY" + r"(?: BLOCK)?-----",
    re.IGNORECASE,
)
PUTTY_PRIVATE_KEY_HEADER = re.compile(
    r"^\s*PuTTY-User-Key-File-[23]\s*:", re.IGNORECASE | re.MULTILINE
)
SSH2_PRIVATE_KEY_HEADER = re.compile(
    r"-{4,}\s*BEGIN\s+SSH2(?:\s+ENCRYPTED)?\s+PRIVATE\s+KEY\s*-{4,}",
    re.IGNORECASE,
)


def nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def safe_text_list(value: Any) -> list[str]:
    if not isinstance(value, list) or not all(nonempty_text(item) for item in value):
        return []
    return [str(item).strip() for item in value]


def valid_text_list(value: Any) -> bool:
    return isinstance(value, list) and all(nonempty_text(item) for item in value)


def normalize_security_text(value: str) -> tuple[str, bool]:
    """Decode bounded JSON escaping; unresolved deep nesting fails closed."""
    normalized = value
    for _ in range(8):
        updated = JSON_UNICODE_ESCAPE.sub(
            lambda match: chr(int(match.group(1), 16)),
            normalized,
        )
        updated = ESCAPED_QUOTE.sub(lambda match: match.group(1), updated)
        if updated == normalized:
            break
        normalized = updated
    unresolved = JSON_UNICODE_ESCAPE.search(normalized) is not None
    return normalized, unresolved


def contains_credential_like_content(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text, unresolved_key_escape = normalize_security_text(str(key))
            normalized_key = (
                CAMEL_CASE_BOUNDARY.sub("_", key_text.strip())
                .lower()
                .replace("-", "_")
                .replace(".", "_")
            )
            if unresolved_key_escape and item not in (None, "", "redacted", "<redacted>"):
                return True
            if normalized_key in CREDENTIAL_KEYS and item not in (None, "", "redacted", "<redacted>"):
                return True
            if contains_credential_like_content(item):
                return True
        return False
    if isinstance(value, list):
        return any(contains_credential_like_content(item) for item in value)
    if isinstance(value, str):
        normalized, unresolved_escape = normalize_security_text(value)
        upper = normalized.upper()
        return (
            unresolved_escape
            or SECRET_ASSIGNMENT.search(normalized) is not None
            or BEARER_AUTHORIZATION.search(normalized) is not None
            or PRIVATE_KEY_HEADER.search(normalized) is not None
            or PUTTY_PRIVATE_KEY_HEADER.search(normalized) is not None
            or SSH2_PRIVATE_KEY_HEADER.search(normalized) is not None
            or any(marker in upper for marker in PRIVATE_KEY_MARKERS)
        )
    return False


def parse_timestamp(value: Any) -> datetime | None:
    if not nonempty_text(value):
        return None
    normalized = str(value).strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def issue(code: str, location: str, message: str) -> dict[str, str]:
    return {"code": code, "location": location, "message": message}


def exact_keys(
    value: dict[str, Any],
    expected: set[str],
    location: str,
    errors: list[dict[str, str]],
) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(issue("missing_fields", location, "missing fields: " + ", ".join(missing)))
    if extra:
        errors.append(issue("unexpected_fields", location, "unexpected fields: " + ", ".join(extra)))


def text_list(
    value: Any,
    location: str,
    errors: list[dict[str, str]],
    *,
    unique: bool = True,
) -> list[str]:
    if not isinstance(value, list) or not all(nonempty_text(item) for item in value):
        errors.append(issue("invalid_list", location, "must be a list of non-empty strings"))
        return []
    result = [str(item).strip() for item in value]
    if unique and len(result) != len(set(result)):
        errors.append(issue("duplicate_reference", location, "references must be unique"))
    return result


def optional_ref(value: Any, location: str, errors: list[dict[str, str]]) -> str | None:
    if value is None:
        return None
    if not nonempty_text(value):
        errors.append(issue("invalid_reference", location, "must be null or non-empty text"))
        return None
    return str(value).strip()


def object_list(
    state: dict[str, Any],
    field: str,
    keys: set[str],
    errors: list[dict[str, str]],
) -> list[dict[str, Any]]:
    value = state.get(field)
    if not isinstance(value, list):
        errors.append(issue("invalid_collection", field, "must be a list"))
        return []
    result: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        location = f"{field}[{index}]"
        if not isinstance(item, dict):
            errors.append(issue("invalid_item", location, "must be an object"))
            continue
        exact_keys(item, keys, location, errors)
        result.append(item)
    return result


def collect_ids(
    items: list[dict[str, Any]],
    kind: str,
    errors: list[dict[str, str]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    index: dict[str, dict[str, Any]] = {}
    ordered: list[str] = []
    for position, item in enumerate(items):
        location = f"{kind}[{position}].id"
        item_id = item.get("id")
        if not nonempty_text(item_id):
            errors.append(issue("invalid_id", location, "must be non-empty text"))
            continue
        normalized = str(item_id).strip()
        ordered.append(normalized)
        if normalized in index:
            errors.append(issue("duplicate_id", location, f"duplicate {kind} ID {normalized}"))
        else:
            index[normalized] = item
    return index, ordered


def check_refs(
    refs: list[str],
    known: set[str],
    location: str,
    errors: list[dict[str, str]],
) -> None:
    for ref in refs:
        if ref not in known:
            errors.append(issue("unknown_reference", location, f"unknown reference {ref}"))


def invalid_reference_list(raw_value: Any, refs: list[str], known: set[str]) -> bool:
    return (
        not valid_text_list(raw_value)
        or len(refs) != len(set(refs))
        or bool(set(refs) - known)
    )


def cycle_nodes(graph: dict[str, set[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: list[str] = []
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        if node in done:
            return
        if node in active:
            start = visiting.index(node)
            cycle = visiting[start:] + [node]
            if cycle not in cycles:
                cycles.append(cycle)
            return
        active.add(node)
        visiting.append(node)
        for target in sorted(graph.get(node, set())):
            if target in graph:
                visit(target)
        visiting.pop()
        active.remove(node)
        done.add(node)

    for node in sorted(graph):
        visit(node)
    return cycles


def validate_state(state: Any) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    if not isinstance(state, dict):
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL",
            "case_id": "unknown",
            "invalidated_run_ids": [],
            "invalidated_evidence_ids": [],
            "invalidated_claim_ids": [],
            "invalidated_document_ids": [],
            "invalidated_gate_ids": [],
            "errors": [issue("invalid_state", "state", "root must be an object")],
        }

    if contains_credential_like_content(state):
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL",
            "case_id": "redacted",
            "invalidated_run_ids": [],
            "invalidated_evidence_ids": [],
            "invalidated_claim_ids": [],
            "invalidated_document_ids": [],
            "invalidated_gate_ids": [],
            "errors": [
                issue(
                    "credential_exposure",
                    "state",
                    "credential-like content detected; value suppressed, remove/redact and rotate",
                )
            ],
        }

    exact_keys(state, STATE_KEYS, "state", errors)
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(issue("invalid_schema", "schema_version", "must be 1"))
    case_id = state.get("case_id")
    if not nonempty_text(case_id):
        errors.append(issue("invalid_case_id", "case_id", "must be non-empty text"))
        case_id = "unknown"
    else:
        case_id = str(case_id).strip()

    evidence_items = object_list(state, "evidence", EVIDENCE_KEYS, errors)
    run_items = object_list(state, "runs", RUN_KEYS, errors)
    claim_items = object_list(state, "claims", CLAIM_KEYS, errors)
    document_items = object_list(state, "documents", DOCUMENT_KEYS, errors)
    gate_items = object_list(state, "gates", GATE_KEYS, errors)

    evidence, evidence_order = collect_ids(evidence_items, "evidence", errors)
    runs, run_order = collect_ids(run_items, "runs", errors)
    claims, claim_order = collect_ids(claim_items, "claims", errors)
    documents, document_order = collect_ids(document_items, "documents", errors)
    gates, gate_order = collect_ids(gate_items, "gates", errors)
    schema_invalid_evidence = {
        item_id for item_id, item in evidence.items() if set(item) != EVIDENCE_KEYS
    }
    schema_invalid_runs = {
        item_id for item_id, item in runs.items() if set(item) != RUN_KEYS
    }
    schema_invalid_claims = {
        item_id for item_id, item in claims.items() if set(item) != CLAIM_KEYS
    }
    schema_invalid_documents = {
        item_id for item_id, item in documents.items() if set(item) != DOCUMENT_KEYS
    }
    schema_invalid_gates = {
        item_id for item_id, item in gates.items() if set(item) != GATE_KEYS
    }
    required_gate_ids = {str(index) for index in range(11)}
    missing_gate_ids = sorted(required_gate_ids - set(gates), key=int)
    if missing_gate_ids:
        errors.append(
            issue(
                "missing_gate",
                "gates",
                "missing Gate IDs: " + ", ".join(missing_gate_ids),
            )
        )

    global_ids: dict[str, str] = {}
    for kind, values in (
        ("evidence", evidence_order),
        ("run", run_order),
        ("claim", claim_order),
        ("document", document_order),
    ):
        for item_id in values:
            previous = global_ids.get(item_id)
            if previous is not None and previous != kind:
                errors.append(
                    issue(
                        "cross_entity_duplicate_id",
                        kind,
                        f"ID {item_id} is already used by {previous}",
                    )
                )
            else:
                global_ids[item_id] = kind
    known_global_ids = set(global_ids)
    global_temporal: dict[str, set[str]] = {
        item_id: set() for item_id in known_global_ids
    }

    evidence_derivation: dict[str, set[str]] = {item_id: set() for item_id in evidence}
    evidence_supersession: dict[str, set[str]] = {item_id: set() for item_id in evidence}
    run_supersession: dict[str, set[str]] = {item_id: set() for item_id in runs}
    claim_dependencies: dict[str, set[str]] = {item_id: set() for item_id in claims}
    claim_temporal: dict[str, set[str]] = {item_id: set() for item_id in claims}
    document_supersession: dict[str, set[str]] = {item_id: set() for item_id in documents}
    evidence_parents_by_id: dict[str, list[str]] = {}
    evidence_run_by_id: dict[str, str | None] = {}
    invalidates_by_id: dict[str, list[str]] = {}
    run_inputs_by_id: dict[str, list[str]] = {}
    run_hashes_by_id: dict[str, list[str]] = {}
    run_extensions_by_id: dict[str, list[str]] = {}
    run_limitations_by_id: dict[str, list[str]] = {}
    claim_evidence_by_id: dict[str, list[str]] = {}
    claim_dependencies_by_id: dict[str, list[str]] = {}
    claim_documents_by_id: dict[str, list[str]] = {}
    claim_historical_documents_by_id: dict[str, list[str]] = {}
    document_claims_by_id: dict[str, list[str]] = {}
    gate_claims_by_id: dict[str, list[str]] = {}
    hash_mismatched_runs: set[str] = set()
    identity_invalid_runs: set[str] = set(schema_invalid_runs)
    structurally_invalid_evidence: set[str] = set(schema_invalid_evidence)
    structurally_invalid_claims: set[str] = set(schema_invalid_claims)
    structurally_invalid_documents: set[str] = set(schema_invalid_documents)
    structurally_invalid_gates: set[str] = set(schema_invalid_gates)
    run_started_by_id: dict[str, datetime | None] = {}
    run_completed_by_id: dict[str, datetime | None] = {}

    for item_id, item in evidence.items():
        location = f"evidence.{item_id}"
        status = item.get("status")
        if status not in EVIDENCE_STATUSES:
            errors.append(issue("invalid_status", location + ".status", "status is outside the allowed enum"))
            structurally_invalid_evidence.add(item_id)
        raw_parents = item.get("derived_from")
        parents = text_list(item.get("derived_from"), location + ".derived_from", errors)
        evidence_parents_by_id[item_id] = parents
        check_refs(parents, set(evidence), location + ".derived_from", errors)
        if invalid_reference_list(raw_parents, parents, set(evidence)):
            structurally_invalid_evidence.add(item_id)
        evidence_derivation[item_id].update(parents)
        raw_run_id = item.get("run_id")
        run_id = optional_ref(item.get("run_id"), location + ".run_id", errors)
        evidence_run_by_id[item_id] = run_id
        if run_id is not None:
            check_refs([run_id], set(runs), location + ".run_id", errors)
        if (raw_run_id is not None and run_id is None) or (
            run_id is not None and run_id not in runs
        ):
            structurally_invalid_evidence.add(item_id)
        transformation = item.get("transformation")
        tool = item.get("tool")
        tool_version = item.get("tool_version")
        if parents:
            if not nonempty_text(transformation):
                errors.append(
                    issue(
                        "derivation_identity_incomplete",
                        location + ".transformation",
                        "derived Evidence requires a non-empty transformation",
                    )
                )
                structurally_invalid_evidence.add(item_id)
            if run_id is None and (
                not nonempty_text(tool) or not nonempty_text(tool_version)
            ):
                errors.append(
                    issue(
                        "derivation_identity_incomplete",
                        location,
                        "derived Evidence without a Run requires tool and tool_version",
                    )
                )
                structurally_invalid_evidence.add(item_id)
            if run_id is not None and (tool is not None or tool_version is not None):
                errors.append(
                    issue(
                        "ambiguous_derivation_identity",
                        location,
                        "Run-linked Evidence inherits tool identity from the Run; Evidence tool fields must be null",
                    )
                )
                structurally_invalid_evidence.add(item_id)
        elif any(value is not None for value in (transformation, tool, tool_version)):
            errors.append(
                issue(
                    "unexpected_derivation_identity",
                    location,
                    "source Evidence without parents must use null derivation identity fields",
                )
            )
            structurally_invalid_evidence.add(item_id)
        raw_limitations = item.get("limitations")
        limitations = text_list(raw_limitations, location + ".limitations", errors)
        if not valid_text_list(raw_limitations) or len(limitations) != len(set(limitations)):
            structurally_invalid_evidence.add(item_id)
        artifact_hash = item.get("artifact_hash")
        if not isinstance(artifact_hash, str) or SHA256.fullmatch(artifact_hash) is None:
            errors.append(issue("invalid_hash", location + ".artifact_hash", "must be a lowercase SHA-256"))
            structurally_invalid_evidence.add(item_id)
        superseded_by = optional_ref(item.get("superseded_by"), location + ".superseded_by", errors)
        if superseded_by is not None:
            check_refs([superseded_by], set(evidence), location + ".superseded_by", errors)
            evidence_supersession[item_id].add(superseded_by)
            global_temporal[item_id].add(superseded_by)
        raw_invalidates = item.get("invalidates_ids")
        invalidates = text_list(raw_invalidates, location + ".invalidates_ids", errors)
        invalidates_by_id[item_id] = invalidates
        check_refs(invalidates, known_global_ids, location + ".invalidates_ids", errors)
        if invalid_reference_list(raw_invalidates, invalidates, known_global_ids):
            structurally_invalid_evidence.add(item_id)
        for target in invalidates:
            if target in global_temporal:
                global_temporal[target].add(item_id)

    for item_id, item in runs.items():
        location = f"runs.{item_id}"
        status = item.get("status")
        if status not in RUN_STATUSES:
            errors.append(issue("invalid_status", location + ".status", "status is outside the allowed enum"))
            identity_invalid_runs.add(item_id)
        if item.get("case_id") != case_id:
            errors.append(issue("run_case_mismatch", location + ".case_id", "must match state.case_id"))
            identity_invalid_runs.add(item_id)
        raw_input_evidence = item.get("input_evidence_ids")
        input_evidence = text_list(item.get("input_evidence_ids"), location + ".input_evidence_ids", errors)
        run_inputs_by_id[item_id] = input_evidence
        check_refs(input_evidence, set(evidence), location + ".input_evidence_ids", errors)
        if (
            not valid_text_list(raw_input_evidence)
            or len(input_evidence) != len(set(input_evidence))
            or set(input_evidence) - set(evidence)
        ):
            identity_invalid_runs.add(item_id)
        if not input_evidence:
            errors.append(
                issue(
                    "run_identity_incomplete",
                    location + ".input_evidence_ids",
                    "must contain at least one input Evidence ID",
                )
            )
            identity_invalid_runs.add(item_id)
        raw_input_hashes = item.get("input_hashes")
        input_hashes = text_list(
            item.get("input_hashes"),
            location + ".input_hashes",
            errors,
            unique=False,
        )
        run_hashes_by_id[item_id] = input_hashes
        if not valid_text_list(raw_input_hashes):
            identity_invalid_runs.add(item_id)
        for index, input_hash in enumerate(input_hashes):
            if SHA256.fullmatch(input_hash) is None:
                identity_invalid_runs.add(item_id)
                errors.append(
                    issue(
                        "invalid_hash",
                        location + f".input_hashes[{index}]",
                        "must be a lowercase SHA-256",
                    )
                )
        if len(input_evidence) != len(input_hashes):
            errors.append(issue("run_identity_incomplete", location, "input Evidence IDs and hashes must have equal counts"))
            identity_invalid_runs.add(item_id)
        for evidence_id, input_hash in zip(input_evidence, input_hashes):
            artifact_hash = evidence.get(evidence_id, {}).get("artifact_hash")
            if (
                isinstance(artifact_hash, str)
                and SHA256.fullmatch(artifact_hash) is not None
                and input_hash != artifact_hash
            ):
                hash_mismatched_runs.add(item_id)
                identity_invalid_runs.add(item_id)
                errors.append(
                    issue(
                        "run_input_hash_mismatch",
                        location + ".input_hashes",
                        "input hash does not match the referenced Evidence artifact hash",
                    )
                )
        for field in (
            "release",
            "period",
            "tool",
            "tool_version",
            "operation",
            "started_at",
            "completed_at",
        ):
            if not nonempty_text(item.get(field)):
                errors.append(issue("run_identity_incomplete", location + f".{field}", "must be non-empty text"))
                identity_invalid_runs.add(item_id)
        started_at = parse_timestamp(item.get("started_at"))
        completed_at = parse_timestamp(item.get("completed_at"))
        run_started_by_id[item_id] = started_at
        run_completed_by_id[item_id] = completed_at
        if started_at is None:
            errors.append(issue("invalid_timestamp", location + ".started_at", "must be an ISO-8601 timestamp with timezone"))
            identity_invalid_runs.add(item_id)
        if completed_at is None:
            errors.append(issue("invalid_timestamp", location + ".completed_at", "must be an ISO-8601 timestamp with timezone"))
            identity_invalid_runs.add(item_id)
        if started_at is not None and completed_at is not None and completed_at < started_at:
            errors.append(issue("invalid_timestamp_order", location, "completed_at must not precede started_at"))
            identity_invalid_runs.add(item_id)
        raw_extension_set = item.get("extension_set")
        run_extensions_by_id[item_id] = text_list(
            item.get("extension_set"), location + ".extension_set", errors
        )
        if (
            not valid_text_list(raw_extension_set)
            or len(run_extensions_by_id[item_id])
            != len(set(run_extensions_by_id[item_id]))
        ):
            identity_invalid_runs.add(item_id)
        raw_limitations = item.get("limitations")
        run_limitations_by_id[item_id] = text_list(
            raw_limitations, location + ".limitations", errors
        )
        if (
            not valid_text_list(raw_limitations)
            or len(run_limitations_by_id[item_id])
            != len(set(run_limitations_by_id[item_id]))
        ):
            identity_invalid_runs.add(item_id)
        superseded_by = optional_ref(item.get("superseded_by"), location + ".superseded_by", errors)
        if superseded_by is not None:
            check_refs([superseded_by], set(runs), location + ".superseded_by", errors)
            run_supersession[item_id].add(superseded_by)
            global_temporal[item_id].add(superseded_by)
        raw_invalidates = item.get("invalidates_ids")
        invalidates = text_list(raw_invalidates, location + ".invalidates_ids", errors)
        invalidates_by_id[item_id] = invalidates
        check_refs(invalidates, known_global_ids, location + ".invalidates_ids", errors)
        if invalid_reference_list(raw_invalidates, invalidates, known_global_ids):
            identity_invalid_runs.add(item_id)
        for target in invalidates:
            if target in global_temporal:
                global_temporal[target].add(item_id)

    for run_id in runs:
        output_ids = sorted(
            evidence_id
            for evidence_id, producing_run_id in evidence_run_by_id.items()
            if producing_run_id == run_id
        )
        if not output_ids:
            errors.append(
                issue(
                    "run_identity_incomplete",
                    f"runs.{run_id}",
                    "Run requires at least one output Evidence with an artifact hash",
                )
            )
            identity_invalid_runs.add(run_id)

    for evidence_id, run_id in evidence_run_by_id.items():
        if run_id is None or run_id not in runs:
            continue
        run_inputs = run_inputs_by_id.get(run_id, [])
        lineage = evidence_parents_by_id.get(evidence_id, [])
        if evidence_id in run_inputs:
            errors.append(
                issue(
                    "run_output_is_input",
                    f"evidence.{evidence_id}.run_id",
                    "Evidence produced by a Run cannot be an input of the same Run",
                )
            )
            structurally_invalid_evidence.add(evidence_id)
            identity_invalid_runs.add(run_id)
        if len(lineage) != len(set(lineage)) or set(lineage) != set(run_inputs):
            errors.append(
                issue(
                    "run_output_lineage_mismatch",
                    f"evidence.{evidence_id}.derived_from",
                    "derived_from must exactly match the producing Run input Evidence IDs",
                )
            )
            structurally_invalid_evidence.add(evidence_id)
            identity_invalid_runs.add(run_id)

    for item_id, item in claims.items():
        location = f"claims.{item_id}"
        status = item.get("status")
        if status not in CLAIM_STATUSES:
            errors.append(issue("invalid_status", location + ".status", "status is outside the allowed enum"))
            structurally_invalid_claims.add(item_id)
        raw_evidence_ids = item.get("evidence_ids")
        evidence_ids = text_list(item.get("evidence_ids"), location + ".evidence_ids", errors)
        claim_evidence_by_id[item_id] = evidence_ids
        check_refs(evidence_ids, set(evidence), location + ".evidence_ids", errors)
        if invalid_reference_list(raw_evidence_ids, evidence_ids, set(evidence)):
            structurally_invalid_claims.add(item_id)
        if status in {"УСТАНОВЛЕНО", "ВЕРОЯТНО", "ТРЕБУЕТ ПРОВЕРКИ"} and not evidence_ids:
            errors.append(
                issue(
                    "claim_evidence_incomplete",
                    location + ".evidence_ids",
                    "a material claim requires at least one supporting Evidence ID",
                )
            )
            structurally_invalid_claims.add(item_id)
        raw_dependencies = item.get("depends_on_claim_ids")
        dependencies = text_list(item.get("depends_on_claim_ids"), location + ".depends_on_claim_ids", errors)
        claim_dependencies_by_id[item_id] = dependencies
        check_refs(dependencies, set(claims), location + ".depends_on_claim_ids", errors)
        if invalid_reference_list(raw_dependencies, dependencies, set(claims)):
            structurally_invalid_claims.add(item_id)
        claim_dependencies[item_id].update(dependencies)
        raw_document_ids = item.get("document_ids")
        raw_historical_ids = item.get("historical_document_ids")
        document_ids = text_list(item.get("document_ids"), location + ".document_ids", errors)
        historical_ids = text_list(item.get("historical_document_ids"), location + ".historical_document_ids", errors)
        claim_documents_by_id[item_id] = document_ids
        claim_historical_documents_by_id[item_id] = historical_ids
        check_refs(document_ids, set(documents), location + ".document_ids", errors)
        check_refs(historical_ids, set(documents), location + ".historical_document_ids", errors)
        if invalid_reference_list(
            raw_document_ids, document_ids, set(documents)
        ) or invalid_reference_list(
            raw_historical_ids, historical_ids, set(documents)
        ):
            structurally_invalid_claims.add(item_id)
        superseded_by = optional_ref(item.get("superseded_by"), location + ".superseded_by", errors)
        if superseded_by is not None:
            check_refs([superseded_by], set(claims), location + ".superseded_by", errors)
            claim_temporal[item_id].add(superseded_by)
            global_temporal[item_id].add(superseded_by)
        raw_invalidates = item.get("invalidates_ids")
        invalidates = text_list(raw_invalidates, location + ".invalidates_ids", errors)
        invalidates_by_id[item_id] = invalidates
        check_refs(invalidates, known_global_ids, location + ".invalidates_ids", errors)
        if invalid_reference_list(raw_invalidates, invalidates, known_global_ids):
            structurally_invalid_claims.add(item_id)
        for target in invalidates:
            if target in global_temporal:
                global_temporal[target].add(item_id)

    for item_id, item in documents.items():
        location = f"documents.{item_id}"
        status = item.get("status")
        if status not in DOCUMENT_STATUSES:
            errors.append(issue("invalid_status", location + ".status", "status is outside the allowed enum"))
            structurally_invalid_documents.add(item_id)
        raw_claim_ids = item.get("claim_ids")
        claim_ids = text_list(item.get("claim_ids"), location + ".claim_ids", errors)
        document_claims_by_id[item_id] = claim_ids
        check_refs(claim_ids, set(claims), location + ".claim_ids", errors)
        if invalid_reference_list(raw_claim_ids, claim_ids, set(claims)):
            structurally_invalid_documents.add(item_id)
        superseded_by = optional_ref(item.get("superseded_by"), location + ".superseded_by", errors)
        if superseded_by is not None:
            check_refs([superseded_by], set(documents), location + ".superseded_by", errors)
            document_supersession[item_id].add(superseded_by)
            global_temporal[item_id].add(superseded_by)
        raw_invalidates = item.get("invalidates_ids")
        invalidates = text_list(raw_invalidates, location + ".invalidates_ids", errors)
        invalidates_by_id[item_id] = invalidates
        check_refs(invalidates, known_global_ids, location + ".invalidates_ids", errors)
        if invalid_reference_list(raw_invalidates, invalidates, known_global_ids):
            structurally_invalid_documents.add(item_id)
        for target in invalidates:
            if target in global_temporal:
                global_temporal[target].add(item_id)

    for item_id, item in gates.items():
        location = f"gates.{item_id}"
        if item_id not in {str(index) for index in range(11)}:
            errors.append(issue("invalid_gate_id", location, "gate ID must be 0 through 10"))
            structurally_invalid_gates.add(item_id)
        status = item.get("status")
        if status not in GATE_STATUSES:
            errors.append(issue("invalid_status", location + ".status", "status is outside the allowed enum"))
            structurally_invalid_gates.add(item_id)
        raw_claim_ids = item.get("claim_ids")
        claim_ids = text_list(item.get("claim_ids"), location + ".claim_ids", errors)
        gate_claims_by_id[item_id] = claim_ids
        check_refs(claim_ids, set(claims), location + ".claim_ids", errors)
        if invalid_reference_list(raw_claim_ids, claim_ids, set(claims)):
            structurally_invalid_gates.add(item_id)

    active_index = state.get("active_index")
    if not isinstance(active_index, dict):
        errors.append(issue("invalid_active_index", "active_index", "must be an object"))
        active_index = {}
    else:
        exact_keys(active_index, ACTIVE_INDEX_KEYS, "active_index", errors)
    active_claims = text_list(active_index.get("claim_ids"), "active_index.claim_ids", errors)
    active_documents = text_list(active_index.get("document_ids"), "active_index.document_ids", errors)
    active_run_id = optional_ref(active_index.get("run_id"), "active_index.run_id", errors)
    check_refs(active_claims, set(claims), "active_index.claim_ids", errors)
    check_refs(active_documents, set(documents), "active_index.document_ids", errors)
    if active_run_id is not None:
        check_refs([active_run_id], set(runs), "active_index.run_id", errors)
    elif any(item.get("status") == "current" for item in runs.values()):
        errors.append(
            issue(
                "missing_active_run",
                "active_index.run_id",
                "a current run requires an explicit active run ID",
            )
        )

    for older_run_id, newer_run_ids in run_supersession.items():
        older_completed = run_completed_by_id.get(older_run_id)
        for newer_run_id in newer_run_ids:
            newer_started = run_started_by_id.get(newer_run_id)
            if (
                older_completed is not None
                and newer_started is not None
                and newer_started < older_completed
            ):
                errors.append(
                    issue(
                        "invalid_supersession_chronology",
                        f"runs.{older_run_id}.superseded_by",
                        "superseding run must not start before the superseded run completed",
                    )
                )
                identity_invalid_runs.add(newer_run_id)

    for graph_name, graph in (
        ("evidence.derived_from", evidence_derivation),
        ("evidence.superseded_by", evidence_supersession),
        ("runs.superseded_by", run_supersession),
        ("claims.depends_on", claim_dependencies),
        ("claims.superseded_by/invalidates", claim_temporal),
        ("documents.superseded_by", document_supersession),
        ("global.superseded_by/invalidates", global_temporal),
    ):
        for cycle in cycle_nodes(graph):
            errors.append(issue("reference_cycle", graph_name, "cycle: " + " -> ".join(cycle)))
            cycle_ids = set(cycle)
            if graph_name.startswith("evidence."):
                structurally_invalid_evidence.update(cycle_ids & set(evidence))
            elif graph_name.startswith("runs."):
                identity_invalid_runs.update(cycle_ids & set(runs))
            elif graph_name.startswith("claims."):
                structurally_invalid_claims.update(cycle_ids & set(claims))
            elif graph_name.startswith("documents."):
                structurally_invalid_documents.update(cycle_ids & set(documents))
            else:
                for cycle_id in cycle_ids:
                    entity_kind = global_ids.get(cycle_id)
                    if entity_kind == "evidence":
                        structurally_invalid_evidence.add(cycle_id)
                    elif entity_kind == "run":
                        identity_invalid_runs.add(cycle_id)
                    elif entity_kind == "claim":
                        structurally_invalid_claims.add(cycle_id)
                    elif entity_kind == "document":
                        structurally_invalid_documents.add(cycle_id)

    def run_fingerprint(item_id: str, item: dict[str, Any]) -> tuple[Any, ...]:
        evidence_ids = run_inputs_by_id.get(item_id, [])
        hashes = run_hashes_by_id.get(item_id, [])
        pairs = tuple(sorted(zip(evidence_ids, hashes))) if len(evidence_ids) == len(hashes) else ()
        return (
            item.get("case_id"),
            pairs,
            item.get("release"),
            tuple(sorted(run_extensions_by_id.get(item_id, []))),
            item.get("period"),
            item.get("tool"),
            item.get("tool_version"),
            item.get("operation"),
            tuple(sorted(run_limitations_by_id.get(item_id, []))),
            item.get("started_at"),
            item.get("completed_at"),
        )

    incompatible_runs: set[str] = set()
    active_run = runs.get(active_run_id) if active_run_id is not None else None
    if active_run is not None:
        if active_run.get("status") != "current" or active_run.get("superseded_by") is not None:
            errors.append(
                issue(
                    "invalid_active_run",
                    "active_index.run_id",
                    "active run must have current status and no superseding run",
                )
            )
        active_fingerprint = run_fingerprint(str(active_run_id), active_run)
        for run_id, item in runs.items():
            if item.get("status") == "current" and (
                run_id != active_run_id
                or run_fingerprint(run_id, item) != active_fingerprint
            ):
                incompatible_runs.add(run_id)
                errors.append(
                    issue(
                        "incompatible_current_run",
                        f"runs.{run_id}",
                        "only the active run ID may be current; identity and timestamps must match its execution",
                    )
                )

    directly_invalidated = {
        target
        for targets in invalidates_by_id.values()
        for target in targets
        if isinstance(target, str) and target in known_global_ids
    }
    invalid_runs = {
        item_id
        for item_id, item in runs.items()
        if item.get("status") != "current" or item.get("superseded_by") is not None
    } | incompatible_runs | hash_mismatched_runs | identity_invalid_runs | (directly_invalidated & set(runs))
    invalid_evidence = {
        item_id
        for item_id, item in evidence.items()
        if item.get("status") != "active"
        or item.get("superseded_by") is not None
    } | structurally_invalid_evidence | (directly_invalidated & set(evidence))
    changed = True
    while changed:
        changed = False
        for item_id, item in runs.items():
            if item_id in invalid_runs:
                continue
            invalid_outputs = {
                evidence_id
                for evidence_id, producing_run_id in evidence_run_by_id.items()
                if producing_run_id == item_id and evidence_id in invalid_evidence
            }
            if (
                set(run_inputs_by_id.get(item_id, [])) & invalid_evidence
                or invalid_outputs
            ):
                invalid_runs.add(item_id)
                changed = True
        for item_id, item in evidence.items():
            if item_id in invalid_evidence:
                continue
            if (
                set(evidence_parents_by_id.get(item_id, [])) & invalid_evidence
                or evidence_run_by_id.get(item_id) in invalid_runs
            ):
                invalid_evidence.add(item_id)
                changed = True
    invalid_documents = {
        item_id
        for item_id, item in documents.items()
        if item.get("status") in {"superseded", "withdrawn"}
        or item.get("superseded_by") is not None
    } | structurally_invalid_documents | (directly_invalidated & set(documents))
    historical_documents = {
        item_id
        for item_id, item in documents.items()
        if item.get("status") == "historical"
    }
    invalid_claims = {
        item_id
        for item_id, item in claims.items()
        if item.get("status") in {"stale", "superseded", "withdrawn"}
        or item.get("superseded_by") is not None
    } | structurally_invalid_claims | (directly_invalidated & set(claims))
    invalid_claims.update(
        item_id
        for item_id in claims
        if set(claim_documents_by_id.get(item_id, [])) & historical_documents
    )

    changed = True
    while changed:
        changed = False
        for item_id, item in claims.items():
            if item_id in invalid_claims:
                continue
            if (
                set(claim_evidence_by_id.get(item_id, [])) & invalid_evidence
                or set(claim_dependencies_by_id.get(item_id, [])) & invalid_claims
                or set(claim_documents_by_id.get(item_id, [])) & invalid_documents
            ):
                invalid_claims.add(item_id)
                changed = True
        for item_id, item in documents.items():
            if item_id in invalid_documents:
                continue
            claim_side_dependencies = {
                claim_id
                for claim_id, document_ids in claim_documents_by_id.items()
                if item_id in document_ids
            }
            if (
                set(document_claims_by_id.get(item_id, []))
                | claim_side_dependencies
            ) & invalid_claims:
                invalid_documents.add(item_id)
                changed = True

    active_claim_set = set(active_claims) - invalid_claims
    active_material_claim_set = {
        claim_id
        for claim_id in active_claim_set
        if claims.get(claim_id, {}).get("status")
        in {"УСТАНОВЛЕНО", "ВЕРОЯТНО", "ТРЕБУЕТ ПРОВЕРКИ"}
    }
    unmapped_passed_gates: set[str] = set()
    if claims:
        for gate_id, item in gates.items():
            if not gate_id.isdigit() or int(gate_id) < 6 or item.get("status") != "passed":
                continue
            mapped_claims = set(gate_claims_by_id.get(gate_id, []))
            if (
                not mapped_claims
                or not mapped_claims.issubset(active_claim_set)
                or not active_material_claim_set.issubset(mapped_claims)
            ):
                unmapped_passed_gates.add(gate_id)
                errors.append(
                    issue(
                        "unmapped_passed_gate",
                        f"gates.{gate_id}.claim_ids",
                        "a passed downstream Gate must cover every active material Claim and reference only active Claims",
                    )
                )

    invalid_projection_gates: set[str] = set()
    if active_run_id in invalid_runs and "5" in gates:
        invalid_projection_gates.add("5")
    if (
        set(active_claims) & invalid_claims
        or set(active_documents) & invalid_documents
    ) and "6" in gates:
        invalid_projection_gates.add("6")

    directly_invalid_gates = {
        item_id
        for item_id, item in gates.items()
        if set(gate_claims_by_id.get(item_id, [])) & invalid_claims
        or item.get("status") == "stale"
    } | unmapped_passed_gates | structurally_invalid_gates | invalid_projection_gates
    invalid_gates = set(directly_invalid_gates)
    numeric_invalid = [int(item_id) for item_id in directly_invalid_gates if item_id.isdigit()]
    if numeric_invalid:
        first_invalid = min(numeric_invalid)
        invalid_gates.update(
            item_id
            for item_id in gates
            if item_id.isdigit()
            and int(item_id) >= first_invalid
            and gates[item_id].get("status") != "not_required"
        )

    for run_id in sorted(invalid_runs):
        if runs.get(run_id, {}).get("status") == "current":
            errors.append(
                issue(
                    "stale_run_status",
                    f"runs.{run_id}",
                    "run with stale/incompatible inputs must be marked stale, superseded or withdrawn",
                )
            )
    if active_run_id in invalid_runs:
        errors.append(
            issue(
                "invalid_active_run",
                "active_index.run_id",
                "active run depends on stale or incompatible evidence",
            )
        )

    for evidence_id in sorted(invalid_evidence):
        if evidence.get(evidence_id, {}).get("status") == "active":
            errors.append(
                issue(
                    "stale_evidence_status",
                    f"evidence.{evidence_id}",
                    "invalidated evidence must be marked stale, superseded or withdrawn",
                )
            )

    for claim_id in sorted(invalid_claims):
        claim = claims.get(claim_id, {})
        if claim.get("status") in {"УСТАНОВЛЕНО", "ВЕРОЯТНО", "ТРЕБУЕТ ПРОВЕРКИ"}:
            errors.append(issue("stale_claim_status", f"claims.{claim_id}", "invalidated claim must be marked stale, superseded or withdrawn"))
    for document_id in sorted(invalid_documents):
        if documents.get(document_id, {}).get("status") == "current":
            errors.append(
                issue(
                    "stale_document_status",
                    f"documents.{document_id}",
                    "document depending on an invalidated claim cannot remain current",
                )
            )
    for claim_id in sorted(set(active_claims) & invalid_claims):
        errors.append(issue("invalid_active_claim", "active_index.claim_ids", f"invalidated claim {claim_id} is still active"))
    for document_id in sorted(set(active_documents)):
        if (
            document_id in invalid_documents
            or documents.get(document_id, {}).get("status") != "current"
        ):
            errors.append(
                issue(
                    "invalid_active_document",
                    "active_index.document_ids",
                    f"non-current document {document_id} is still active",
                )
            )
    for gate_id in sorted(invalid_gates, key=lambda value: int(value) if value.isdigit() else 99):
        if gates.get(gate_id, {}).get("status") != "stale":
            errors.append(issue("stale_gate_status", f"gates.{gate_id}", "invalidated gate and every downstream gate must be stale"))
    for claim_id, item in claims.items():
        for document_id in claim_documents_by_id.get(claim_id, []):
            if (
                document_id in invalid_documents
                or documents.get(document_id, {}).get("status") != "current"
            ):
                errors.append(
                    issue(
                        "superseded_current_source",
                        f"claims.{claim_id}.document_ids",
                        f"document {document_id} requires historical_document_ids or a current replacement",
                    )
                )

    errors.sort(key=lambda item: (item["code"], item["location"], item["message"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if not errors else "FAIL",
        "case_id": case_id,
        "invalidated_run_ids": sorted(invalid_runs),
        "invalidated_evidence_ids": sorted(invalid_evidence),
        "invalidated_claim_ids": sorted(invalid_claims),
        "invalidated_document_ids": sorted(invalid_documents),
        "invalidated_gate_ids": sorted(
            invalid_gates,
            key=lambda value: int(value) if value.isdigit() else 99,
        ),
        "errors": errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def write_result(result: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = json.loads(args.state.read_text(encoding="utf-8"))
        result = validate_state(payload)
    except (OSError, json.JSONDecodeError):
        result = {
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL",
            "case_id": "unknown",
            "invalidated_run_ids": [],
            "invalidated_evidence_ids": [],
            "invalidated_claim_ids": [],
            "invalidated_document_ids": [],
            "invalidated_gate_ids": [],
            "errors": [
                issue(
                    "input_error",
                    "state",
                    "input could not be read or parsed; path and content are suppressed",
                )
            ],
        }
    write_result(result, args.output)
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
