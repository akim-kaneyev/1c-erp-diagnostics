#!/usr/bin/env python3
"""Validate the synthetic Gate 0-10 eval suite and machine-readable results."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
SUITE_PATH = EVALS / "suite.json"

GATE_KEYS = {str(index) for index in range(11)}
GATE_STATUSES = {"pending", "passed", "blocked", "failed", "stale", "not_required"}
FINAL_STATUSES = {"УСТАНОВЛЕНО", "ВЕРОЯТНО", "ТРЕБУЕТ ПРОВЕРКИ"}
RISKS = {"R0", "R1", "R2", "R3"}
DECISIONS = {"GO", "NO-GO", "NO_ACTION", "EVIDENCE_REQUIRED"}
CURRENT_GOAL_STATUSES = {"closed", "blocked", "open"}
LINKED_INCIDENT_STATUSES = {"resolved", "open", "blocked", "not_in_scope"}
CAPABILITY_STATUSES = {
    "available",
    "confirmation_required",
    "unavailable",
    "prohibited",
}
CAUSAL_STAGES = [
    "document",
    "movement",
    "record_register",
    "consuming_mechanism",
    "accounting_stock_access_result",
    "symptom",
]
CASE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
METADATA_OBJECT = re.compile(
    r"(?<![\w])(?:Документ|Справочник|РегистрНакопления|РегистрСведений|"
    r"РегистрБухгалтерии|ПланСчетов|ПланВидовХарактеристик|Перечисление|"
    r"Обработка|Отчет|ОбщийМодуль|Document|Catalog|AccumulationRegister|"
    r"InformationRegister|AccountingRegister|ChartOfAccounts|CommonModule)"
    r"\.[A-Za-zА-Яа-яЁё0-9_]+"
)
SUITE_KEYS = {
    "schema_version",
    "name",
    "description",
    "required_domains",
    "required_controls",
    "cases",
}
CASE_KEYS = {
    "schema_version",
    "id",
    "title",
    "domain",
    "controls",
    "synthetic",
    "allowed_metadata_objects",
    "prompt",
    "evidence",
    "capabilities",
    "expect",
}
EVIDENCE_KEYS = {"id", "kind", "summary", "proves", "does_not_prove"}
INPUT_CAPABILITY_KEYS = {"name", "status"}
EXPECT_KEYS = {
    "allowed_final_statuses",
    "required_gate_statuses",
    "required_risk",
    "required_decision",
    "allowed_current_goal_statuses",
    "allowed_linked_incident_statuses",
    "max_established_claims",
    "min_claims",
    "min_actions",
    "min_requested_evidence",
    "required_evidence_ids",
    "required_capabilities",
    "require_complete_causal_chain",
    "required_causal_stage_evidence",
}
RESULT_KEYS = {
    "schema_version",
    "case_id",
    "final_status",
    "risk",
    "decision",
    "current_goal_status",
    "linked_incident_status",
    "gates",
    "capabilities",
    "evidence_ids_used",
    "claims",
    "causal_chain",
    "requested_evidence",
    "actions",
    "summary",
}
RESULT_CAPABILITY_KEYS = {"name", "status", "simulated"}
CLAIM_KEYS = {"id", "status", "text", "evidence_ids", "falsifier"}
CAUSAL_CHAIN_KEYS = {"complete", "links"}
CAUSAL_LINK_KEYS = {"stage", "evidence_ids"}
ACTION_KEYS = {
    "description",
    "risk",
    "approved",
    "executed",
    "approval_reference",
    "rollback",
    "validation",
}


def add(errors: list[str], location: str, message: str) -> None:
    errors.append(f"{location}: {message}")


def configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def check_exact_keys(
    value: dict[str, Any],
    expected: set[str],
    errors: list[str],
    location: str,
) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        add(errors, location, "missing fields: " + ", ".join(missing))
    if unexpected:
        add(errors, location, "unexpected fields: " + ", ".join(unexpected))


def load_object(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validator reports malformed input
        add(errors, str(path.relative_to(ROOT)), f"invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        add(errors, str(path.relative_to(ROOT)), "JSON root must be an object")
        return {}
    return value


def nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def text_list(value: Any) -> bool:
    return isinstance(value, list) and all(nonempty_text(item) for item in value)


def iter_text(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_text(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_text(item)


def validate_case(case: dict[str, Any], path: Path, errors: list[str]) -> None:
    location = str(path.relative_to(ROOT))
    check_exact_keys(case, CASE_KEYS, errors, location)
    case_id = case.get("id")
    if case.get("schema_version") != 1:
        add(errors, location, "schema_version must be 1")
    if not isinstance(case_id, str) or not CASE_ID.fullmatch(case_id):
        add(errors, location, "id must be lower-case hyphen-case")
    for field in ("title", "domain", "prompt"):
        if not nonempty_text(case.get(field)):
            add(errors, location, f"{field} must be non-empty text")
    if case.get("synthetic") is not True:
        add(errors, location, "synthetic must be true; public evals cannot contain live case data")
    allowed_objects = case.get("allowed_metadata_objects")
    if not text_list(allowed_objects):
        add(errors, location, "allowed_metadata_objects must be a text list")
    else:
        if len(allowed_objects) != len(set(allowed_objects)):
            add(errors, location, "allowed_metadata_objects must be unique")
        invalid_objects = [
            item for item in allowed_objects if METADATA_OBJECT.fullmatch(item) is None
        ]
        if invalid_objects:
            add(
                errors,
                location,
                "allowed_metadata_objects contains invalid canonical names: "
                + ", ".join(invalid_objects),
            )
    controls = case.get("controls")
    if not text_list(controls) or not controls:
        add(errors, location, "controls must be a non-empty text list")
    if "EVAL_RESULT_JSON" not in str(case.get("prompt", "")):
        add(errors, location, "prompt must request EVAL_RESULT_JSON")

    evidence = case.get("evidence")
    if not isinstance(evidence, list):
        add(errors, location, "evidence must be a list")
        evidence = []
    evidence_ids: list[str] = []
    for index, item in enumerate(evidence):
        item_location = f"{location}.evidence[{index}]"
        if not isinstance(item, dict):
            add(errors, item_location, "must be an object")
            continue
        check_exact_keys(item, EVIDENCE_KEYS, errors, item_location)
        evidence_id = item.get("id")
        if not nonempty_text(evidence_id):
            add(errors, item_location, "id must be non-empty text")
        else:
            evidence_ids.append(str(evidence_id))
        for field in ("kind", "summary"):
            if not nonempty_text(item.get(field)):
                add(errors, item_location, f"{field} must be non-empty text")
        for field in ("proves", "does_not_prove"):
            if not text_list(item.get(field)):
                add(errors, item_location, f"{field} must be a text list")
    if len(evidence_ids) != len(set(evidence_ids)):
        add(errors, location, "evidence ids must be unique")

    capabilities = case.get("capabilities", [])
    if not isinstance(capabilities, list):
        add(errors, location, "capabilities must be a list")
        capabilities = []
    capability_names: list[str] = []
    for index, item in enumerate(capabilities):
        item_location = f"{location}.capabilities[{index}]"
        if not isinstance(item, dict):
            add(errors, item_location, "must be an object")
            continue
        check_exact_keys(item, INPUT_CAPABILITY_KEYS, errors, item_location)
        name = item.get("name")
        status = item.get("status")
        if not nonempty_text(name):
            add(errors, item_location, "name must be non-empty text")
        else:
            capability_names.append(str(name))
        if status not in CAPABILITY_STATUSES:
            add(errors, item_location, f"invalid status {status!r}")
    if len(capability_names) != len(set(capability_names)):
        add(errors, location, "capability names must be unique")

    expect = case.get("expect")
    if not isinstance(expect, dict):
        add(errors, location, "expect must be an object")
        return
    check_exact_keys(expect, EXPECT_KEYS, errors, f"{location}.expect")

    allowed_final = expect.get("allowed_final_statuses")
    if (
        not isinstance(allowed_final, list)
        or not allowed_final
        or not set(allowed_final).issubset(FINAL_STATUSES)
    ):
        add(errors, location, "expect.allowed_final_statuses contains invalid values")

    required_gates = expect.get("required_gate_statuses", {})
    if not isinstance(required_gates, dict):
        add(errors, location, "expect.required_gate_statuses must be an object")
    else:
        for gate, status in required_gates.items():
            if gate not in GATE_KEYS:
                add(errors, location, f"expect references invalid Gate {gate!r}")
            if status not in GATE_STATUSES:
                add(errors, location, f"expect has invalid Gate status {status!r}")

    scalar_enums = {
        "required_risk": RISKS,
        "required_decision": DECISIONS,
    }
    for field, allowed in scalar_enums.items():
        value = expect.get(field)
        if value not in allowed:
            add(errors, location, f"expect.{field} must be one of {sorted(allowed)}")

    list_enums = {
        "allowed_current_goal_statuses": CURRENT_GOAL_STATUSES,
        "allowed_linked_incident_statuses": LINKED_INCIDENT_STATUSES,
    }
    for field, allowed in list_enums.items():
        value = expect.get(field)
        if not isinstance(value, list) or not value or not set(value).issubset(allowed):
            add(errors, location, f"expect.{field} contains invalid values")

    for field in (
        "max_established_claims",
        "min_claims",
        "min_actions",
        "min_requested_evidence",
    ):
        value = expect.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            add(errors, location, f"expect.{field} must be a non-negative integer")
    required_evidence = expect.get("required_evidence_ids")
    if not text_list(required_evidence):
        add(errors, location, "expect.required_evidence_ids must be a text list")
    else:
        if len(required_evidence) != len(set(required_evidence)):
            add(errors, location, "expect.required_evidence_ids must be unique")
        unknown = sorted(set(required_evidence) - set(evidence_ids))
        if unknown:
            add(errors, location, "expect references unknown evidence ids: " + ", ".join(unknown))

    required_capabilities = expect.get("required_capabilities", {})
    if not isinstance(required_capabilities, dict):
        add(errors, location, "expect.required_capabilities must be an object")
    else:
        known = set(capability_names)
        for name, status in required_capabilities.items():
            if name not in known:
                add(errors, location, f"expect references undeclared capability {name!r}")
            if status not in CAPABILITY_STATUSES:
                add(errors, location, f"expect has invalid capability status {status!r}")

    require_chain = expect.get("require_complete_causal_chain")
    if not isinstance(require_chain, bool):
        add(errors, location, "expect.require_complete_causal_chain must be boolean")
    required_stage_evidence = expect.get("required_causal_stage_evidence")
    if not isinstance(required_stage_evidence, dict):
        add(errors, location, "expect.required_causal_stage_evidence must be an object")
    else:
        for stage, required_ids in required_stage_evidence.items():
            if stage not in CAUSAL_STAGES:
                add(errors, location, f"expect references invalid causal stage {stage!r}")
            if not text_list(required_ids) or not required_ids:
                add(errors, location, f"expect causal stage {stage!r} requires evidence ids")
                continue
            if len(required_ids) != len(set(required_ids)):
                add(errors, location, f"expect causal stage {stage!r} has duplicate evidence ids")
            unknown = sorted(set(required_ids) - set(evidence_ids))
            if unknown:
                add(
                    errors,
                    location,
                    f"expect causal stage {stage!r} references unknown evidence: "
                    + ", ".join(unknown),
                )


def load_suite() -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    errors: list[str] = []
    suite = load_object(SUITE_PATH, errors) if SUITE_PATH.is_file() else {}
    if not SUITE_PATH.is_file():
        add(errors, "evals/suite.json", "file is missing")
        return suite, {}, errors
    if suite.get("schema_version") != 1:
        add(errors, "evals/suite.json", "schema_version must be 1")
    check_exact_keys(suite, SUITE_KEYS, errors, "evals/suite.json")
    for field in ("name", "description"):
        if not nonempty_text(suite.get(field)):
            add(errors, "evals/suite.json", f"{field} must be non-empty text")

    entries = suite.get("cases")
    if not isinstance(entries, list) or not entries or not all(nonempty_text(item) for item in entries):
        add(errors, "evals/suite.json", "cases must be a non-empty list of paths")
        entries = []

    cases: dict[str, dict[str, Any]] = {}
    resolved_paths: set[Path] = set()
    eval_root = EVALS.resolve()
    for entry in entries:
        path = (EVALS / str(entry)).resolve()
        try:
            path.relative_to(eval_root)
        except ValueError:
            add(errors, "evals/suite.json", f"case path escapes evals/: {entry}")
            continue
        if path in resolved_paths:
            add(errors, "evals/suite.json", f"duplicate case path: {entry}")
            continue
        resolved_paths.add(path)
        if not path.is_file():
            add(errors, "evals/suite.json", f"case file is missing: {entry}")
            continue
        case = load_object(path, errors)
        validate_case(case, path, errors)
        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in cases:
                add(errors, "evals/suite.json", f"duplicate case id: {case_id}")
            else:
                cases[case_id] = case

    required_domains = suite.get("required_domains")
    if not text_list(required_domains) or not required_domains:
        add(errors, "evals/suite.json", "required_domains must be a non-empty text list")
        required_domains = []
    actual_domains = {case.get("domain") for case in cases.values()}
    missing_domains = sorted(set(required_domains) - actual_domains)
    if missing_domains:
        add(errors, "evals/suite.json", "missing required domains: " + ", ".join(missing_domains))

    required_controls = suite.get("required_controls")
    if not text_list(required_controls) or not required_controls:
        add(errors, "evals/suite.json", "required_controls must be a non-empty text list")
        required_controls = []
    actual_controls = {
        control
        for case in cases.values()
        for control in case.get("controls", [])
        if isinstance(control, str)
    }
    missing_controls = sorted(set(required_controls) - actual_controls)
    if missing_controls:
        add(errors, "evals/suite.json", "missing required controls: " + ", ".join(missing_controls))

    return suite, cases, errors


def validate_result(
    result: dict[str, Any],
    case: dict[str, Any],
    location: str = "result",
) -> list[str]:
    errors: list[str] = []
    case_id = case["id"]
    expect = case["expect"]
    check_exact_keys(result, RESULT_KEYS, errors, location)

    if result.get("schema_version") != 1:
        add(errors, location, "schema_version must be 1")
    if result.get("case_id") != case_id:
        add(errors, location, f"case_id must be {case_id!r}")

    final_status = result.get("final_status")
    if final_status not in FINAL_STATUSES:
        add(errors, location, f"invalid final_status {final_status!r}")
    elif final_status not in expect["allowed_final_statuses"]:
        add(errors, location, f"final_status {final_status!r} is forbidden for this case")

    risk = result.get("risk")
    if risk not in RISKS:
        add(errors, location, f"invalid risk {risk!r}")
    elif risk != expect["required_risk"]:
        add(errors, location, f"risk must be {expect['required_risk']}")

    decision = result.get("decision")
    if decision not in DECISIONS:
        add(errors, location, f"invalid decision {decision!r}")
    elif decision != expect["required_decision"]:
        add(errors, location, f"decision must be {expect['required_decision']}")

    current_goal = result.get("current_goal_status")
    if current_goal not in CURRENT_GOAL_STATUSES:
        add(errors, location, f"invalid current_goal_status {current_goal!r}")
    elif current_goal not in expect["allowed_current_goal_statuses"]:
        add(errors, location, f"current_goal_status {current_goal!r} is forbidden for this case")

    linked_incident = result.get("linked_incident_status")
    if linked_incident not in LINKED_INCIDENT_STATUSES:
        add(errors, location, f"invalid linked_incident_status {linked_incident!r}")
    elif linked_incident not in expect["allowed_linked_incident_statuses"]:
        add(errors, location, f"linked_incident_status {linked_incident!r} is forbidden for this case")

    gates = result.get("gates")
    if not isinstance(gates, dict):
        add(errors, location, "gates must be an object containing Gate 0 through Gate 10")
        gates = {}
    gate_keys = set(gates)
    if gate_keys != GATE_KEYS:
        missing = sorted(GATE_KEYS - gate_keys, key=int)
        extra = sorted(gate_keys - GATE_KEYS)
        if missing:
            add(errors, location, "missing gates: " + ", ".join(missing))
        if extra:
            add(errors, location, "unexpected gates: " + ", ".join(extra))
    for gate, status in gates.items():
        if status not in GATE_STATUSES:
            add(errors, location, f"Gate {gate} has invalid or decorated status {status!r}")
    for gate, required in expect["required_gate_statuses"].items():
        if gates.get(gate) != required:
            add(errors, location, f"Gate {gate} must be {required!r}, got {gates.get(gate)!r}")

    if current_goal == "closed":
        if gates.get("10") != "passed":
            add(errors, location, "closed current goal requires Gate 10 passed")
        unfinished = {
            gate: status
            for gate, status in gates.items()
            if status not in {"passed", "not_required"}
        }
        if unfinished:
            add(errors, location, f"closed current goal has unfinished gates: {unfinished}")
    if gates.get("10") == "passed" and current_goal != "closed":
        add(errors, location, "Gate 10 passed requires current_goal_status closed")

    known_evidence = {item["id"] for item in case.get("evidence", [])}
    used_evidence = result.get("evidence_ids_used")
    if not isinstance(used_evidence, list) or not all(nonempty_text(item) for item in used_evidence):
        add(errors, location, "evidence_ids_used must be a text list")
        used_evidence = []
    elif len(used_evidence) != len(set(used_evidence)):
        add(errors, location, "evidence_ids_used must be unique")
    unknown_used = sorted(set(used_evidence) - known_evidence)
    if unknown_used:
        add(errors, location, "unknown evidence ids used: " + ", ".join(unknown_used))
    missing_required_evidence = sorted(
        set(expect["required_evidence_ids"]) - set(used_evidence)
    )
    if missing_required_evidence:
        add(
            errors,
            location,
            "required evidence ids not used: " + ", ".join(missing_required_evidence),
        )

    capabilities = result.get("capabilities")
    if not isinstance(capabilities, list):
        add(errors, location, "capabilities must be a list")
        capabilities = []
    by_capability: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(capabilities):
        item_location = f"{location}.capabilities[{index}]"
        if not isinstance(item, dict):
            add(errors, item_location, "must be an object")
            continue
        check_exact_keys(item, RESULT_CAPABILITY_KEYS, errors, item_location)
        name = item.get("name")
        status = item.get("status")
        if not nonempty_text(name):
            add(errors, item_location, "name must be non-empty text")
            continue
        if name in by_capability:
            add(errors, item_location, f"duplicate capability {name!r}")
        by_capability[str(name)] = item
        if status not in CAPABILITY_STATUSES:
            add(errors, item_location, f"invalid status {status!r}")
        if item.get("simulated") is not False:
            add(errors, item_location, "simulated must be false")
    for name, required_status in expect["required_capabilities"].items():
        actual = by_capability.get(name)
        if actual is None:
            add(errors, location, f"required capability result is missing: {name}")
        elif actual.get("status") != required_status:
            add(errors, location, f"capability {name} must be {required_status!r}")

    claims = result.get("claims")
    if not isinstance(claims, list):
        add(errors, location, "claims must be a list")
        claims = []
    established_count = 0
    claim_ids: list[str] = []
    for index, claim in enumerate(claims):
        item_location = f"{location}.claims[{index}]"
        if not isinstance(claim, dict):
            add(errors, item_location, "must be an object")
            continue
        check_exact_keys(claim, CLAIM_KEYS, errors, item_location)
        for field in ("id", "text", "falsifier"):
            if not nonempty_text(claim.get(field)):
                add(errors, item_location, f"{field} must be non-empty text")
        if nonempty_text(claim.get("id")):
            claim_ids.append(str(claim["id"]))
        status = claim.get("status")
        if status not in FINAL_STATUSES:
            add(errors, item_location, f"invalid status {status!r}")
        if status == "УСТАНОВЛЕНО":
            established_count += 1
        evidence_ids = claim.get("evidence_ids")
        if not isinstance(evidence_ids, list) or not all(nonempty_text(item) for item in evidence_ids):
            add(errors, item_location, "evidence_ids must be a text list")
            evidence_ids = []
        elif len(evidence_ids) != len(set(evidence_ids)):
            add(errors, item_location, "evidence_ids must be unique")
        unknown = sorted(set(evidence_ids) - known_evidence)
        if unknown:
            add(errors, item_location, "unknown evidence ids: " + ", ".join(unknown))
        if status == "УСТАНОВЛЕНО" and not evidence_ids:
            add(errors, item_location, "established claim requires evidence_ids")
    if len(claim_ids) != len(set(claim_ids)):
        add(errors, location, "claim ids must be unique")
    if len(claims) < expect["min_claims"]:
        add(errors, location, f"claims must contain at least {expect['min_claims']} item(s)")
    if established_count > expect["max_established_claims"]:
        add(
            errors,
            location,
            f"established claims {established_count} exceed allowed maximum "
            f"{expect['max_established_claims']}",
        )

    chain = result.get("causal_chain")
    if not isinstance(chain, dict):
        add(errors, location, "causal_chain must be an object")
        chain = {}
    else:
        check_exact_keys(chain, CAUSAL_CHAIN_KEYS, errors, f"{location}.causal_chain")
    complete = chain.get("complete")
    if not isinstance(complete, bool):
        add(errors, location, "causal_chain.complete must be boolean")
    if complete is not expect["require_complete_causal_chain"]:
        add(
            errors,
            location,
            "causal_chain.complete must be "
            + str(expect["require_complete_causal_chain"]).lower(),
        )
    links = chain.get("links")
    if not isinstance(links, list):
        add(errors, location, "causal_chain.links must be a list")
        links = []
    seen_stages: list[str] = []
    evidence_by_stage: dict[str, set[str]] = {}
    for index, link in enumerate(links):
        item_location = f"{location}.causal_chain.links[{index}]"
        if not isinstance(link, dict):
            add(errors, item_location, "must be an object")
            continue
        check_exact_keys(link, CAUSAL_LINK_KEYS, errors, item_location)
        stage = link.get("stage")
        seen_stages.append(str(stage))
        if stage not in CAUSAL_STAGES:
            add(errors, item_location, f"invalid stage {stage!r}")
        evidence_ids = link.get("evidence_ids")
        if not isinstance(evidence_ids, list) or not all(nonempty_text(item) for item in evidence_ids):
            add(errors, item_location, "evidence_ids must be a text list")
            evidence_ids = []
        elif len(evidence_ids) != len(set(evidence_ids)):
            add(errors, item_location, "evidence_ids must be unique")
        unknown = sorted(set(evidence_ids) - known_evidence)
        if unknown:
            add(errors, item_location, "unknown evidence ids: " + ", ".join(unknown))
        if complete and not evidence_ids:
            add(errors, item_location, "complete causal link requires evidence_ids")
        if isinstance(stage, str):
            evidence_by_stage.setdefault(stage, set()).update(evidence_ids)
    if complete and seen_stages != CAUSAL_STAGES:
        add(errors, location, "complete causal chain must contain all six stages in order")
    elif len(seen_stages) != len(set(seen_stages)):
        add(errors, location, "causal_chain stages must be unique")
    for stage, required_ids in expect["required_causal_stage_evidence"].items():
        missing = sorted(set(required_ids) - evidence_by_stage.get(stage, set()))
        if missing:
            add(
                errors,
                location,
                f"causal stage {stage!r} is missing required evidence: "
                + ", ".join(missing),
            )

    requested = result.get("requested_evidence")
    if not text_list(requested):
        add(errors, location, "requested_evidence must be a text list")
        requested = []
    if len(requested) < expect["min_requested_evidence"]:
        add(
            errors,
            location,
            f"requested_evidence must contain at least {expect['min_requested_evidence']} item(s)",
        )

    actions = result.get("actions")
    if not isinstance(actions, list):
        add(errors, location, "actions must be a list")
        actions = []
    if len(actions) < expect["min_actions"]:
        add(errors, location, f"actions must contain at least {expect['min_actions']} item(s)")
    for index, action in enumerate(actions):
        item_location = f"{location}.actions[{index}]"
        if not isinstance(action, dict):
            add(errors, item_location, "must be an object")
            continue
        check_exact_keys(action, ACTION_KEYS, errors, item_location)
        if not nonempty_text(action.get("description")):
            add(errors, item_location, "description must be non-empty text")
        action_risk = action.get("risk")
        if action_risk not in RISKS:
            add(errors, item_location, f"invalid risk {action_risk!r}")
        for field in ("approved", "executed"):
            if not isinstance(action.get(field), bool):
                add(errors, item_location, f"{field} must be boolean")
        if action_risk == "R3" and action.get("executed") is True:
            if action.get("approved") is not True:
                add(errors, item_location, "executed R3 action requires approved=true")
            for field in ("approval_reference", "rollback", "validation"):
                if not nonempty_text(action.get(field)):
                    add(errors, item_location, f"executed R3 action requires {field}")
    if decision == "NO-GO" and any(action.get("executed") is True for action in actions if isinstance(action, dict)):
        add(errors, location, "NO-GO result cannot contain an executed action")

    if final_status == "УСТАНОВЛЕНО":
        if gates.get("7") != "passed":
            add(errors, location, "УСТАНОВЛЕНО requires Gate 7 passed")
        if complete is not True:
            add(errors, location, "УСТАНОВЛЕНО requires a complete causal chain")
        if gates.get("10") != "passed" or current_goal != "closed":
            add(errors, location, "УСТАНОВЛЕНО requires closed goal and Gate 10 passed")

    if not nonempty_text(result.get("summary")):
        add(errors, location, "summary must be non-empty text")

    allowed_objects = set(case.get("allowed_metadata_objects", []))
    mentioned_objects = {
        match.group(0)
        for text in iter_text(result)
        for match in METADATA_OBJECT.finditer(text)
    }
    undeclared_objects = sorted(mentioned_objects - allowed_objects)
    if undeclared_objects:
        add(
            errors,
            location,
            "result names metadata objects absent from case evidence: "
            + ", ".join(undeclared_objects),
        )

    return errors


def result_skeleton(case_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": case_id,
        "final_status": "<УСТАНОВЛЕНО|ВЕРОЯТНО|ТРЕБУЕТ ПРОВЕРКИ>",
        "risk": "<R0|R1|R2|R3>",
        "decision": "<GO|NO-GO|NO_ACTION|EVIDENCE_REQUIRED>",
        "current_goal_status": "<closed|blocked|open>",
        "linked_incident_status": "<resolved|open|blocked|not_in_scope>",
        "gates": {
            str(index): "<pending|passed|blocked|failed|stale|not_required>"
            for index in range(11)
        },
        "capabilities": [],
        "evidence_ids_used": [],
        "claims": [],
        "causal_chain": {"complete": False, "links": []},
        "requested_evidence": [],
        "actions": [],
        "summary": "<краткий итог>",
    }


def render_prompt(case: dict[str, Any]) -> str:
    evidence_lines = []
    for item in case.get("evidence", []):
        evidence_lines.append(
            f"- {item['id']} ({item['kind']}): {item['summary']}\n"
            f"  Доказывает: {'; '.join(item['proves']) or 'ничего сверх источника'}.\n"
            f"  Не доказывает: {'; '.join(item['does_not_prove']) or 'не указано'}."
        )
    capability_lines = [
        f"- {item['name']}: {item['status']}" for item in case.get("capabilities", [])
    ]
    skeleton = json.dumps(result_skeleton(case["id"]), ensure_ascii=False, indent=2)
    return (
        "@one-c-erp-diagnostics\n\n"
        f"Синтетический регрессионный кейс `{case['id']}`. Реальные данные отсутствуют.\n\n"
        f"{case['prompt']}\n\n"
        "Исходные доказательства:\n"
        + ("\n".join(evidence_lines) if evidence_lines else "- Доказательства не предоставлены.")
        + "\n\nФактически заданные возможности:\n"
        + ("\n".join(capability_lines) if capability_lines else "- Не заданы; выполни Gate 0.")
        + "\n\nВерни только один JSON-объект без Markdown. Используй этот каркас; "
        "заполни все Gate 0–10 каноническими статусами, не копируй значения-заглушки:\n\n"
        + skeleton
    )


def result_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(path.glob("*.result.json"))
    return []


def main() -> int:
    configure_utf8_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, help="Result JSON file or directory")
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Require exactly one valid result for every suite case",
    )
    parser.add_argument("--render", metavar="CASE_ID", help="Render an eval prompt without expectations")
    args = parser.parse_args()

    suite, cases, errors = load_suite()
    if errors:
        print("EVAL SUITE VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.render:
        case = cases.get(args.render)
        if case is None:
            print(f"Unknown case id: {args.render}", file=sys.stderr)
            return 1
        print(render_prompt(case))
        return 0

    if args.results is None:
        print("EVAL SUITE VALIDATION: PASS")
        print(f"Cases: {len(cases)}")
        print("Domains: " + ", ".join(suite["required_domains"]))
        print("Controls: " + ", ".join(suite["required_controls"]))
        return 0

    files = result_files(args.results)
    if not files:
        print(f"No result JSON files found at {args.results}", file=sys.stderr)
        return 1

    seen: set[str] = set()
    result_errors: list[str] = []
    for path in files:
        result = load_object(path, result_errors)
        case_id = result.get("case_id")
        if not isinstance(case_id, str) or case_id not in cases:
            add(result_errors, str(path), f"unknown case_id {case_id!r}")
            continue
        if case_id in seen:
            add(result_errors, str(path), f"duplicate result for {case_id}")
            continue
        seen.add(case_id)
        result_errors.extend(validate_result(result, cases[case_id], str(path)))

    if args.require_complete:
        missing = sorted(set(cases) - seen)
        if missing:
            add(result_errors, str(args.results), "missing results: " + ", ".join(missing))
        extra_count = len(files) - len(seen)
        if extra_count:
            add(result_errors, str(args.results), f"contains {extra_count} duplicate/unknown result file(s)")

    if result_errors:
        print("EVAL RESULT VALIDATION: FAIL", file=sys.stderr)
        for error in result_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("EVAL RESULT VALIDATION: PASS")
    print(f"Validated results: {len(seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
