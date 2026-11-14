"""Read-only, loopback-only CodexTestBridge adapter. No third-party code bundled."""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

REVIEWED_SOURCE = "https://github.com/msrv-tech/skills"
REVIEWED_COMMIT = "702dc8dbe0a0d31b1a16af3d871af29b99ef1122"
MAX_BYTES = 4 * 1024 * 1024
SECTIONS = {"catalogs", "documents", "enums", "informationRegisters", "accumulationRegisters"}


class BridgeError(ValueError):
    """Messages deliberately contain no server body, query, credential or local path."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BridgeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def decode(data: bytes) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate_json_key")
            result[key] = value
        return result

    def invalid_constant(value):
        raise BridgeError("non_finite_json")

    require(len(data) <= MAX_BYTES, "response_too_large")
    try:
        result = json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=invalid_constant)
        # Reject exponent overflow too (1e999), which parse_constant does not see.
        encode(result)
    except (ValueError, UnicodeError, RecursionError, TypeError) as exc:
        raise BridgeError("invalid_json") from exc
    require(isinstance(result, dict), "json_object_required")
    return result


def normalize_url(value: str) -> str:
    require(isinstance(value, str) and not re.search(r"[\s\\%]", value), "invalid_endpoint")
    try:
        parts = urllib.parse.urlsplit(value)
        port = parts.port
    except ValueError as exc:
        raise BridgeError("invalid_endpoint") from exc
    require(parts.scheme == "http" and parts.hostname in {"127.0.0.1", "::1"}, "loopback_http_required")
    require(parts.username is None and parts.password is None and not parts.query and not parts.fragment,
            "endpoint_credentials_or_suffix_forbidden")
    require(port is None or 1 <= port <= 65535, "invalid_port")
    require(re.fullmatch(r"(?:/[A-Za-z0-9_-]+)+/hs/codex-test/?", parts.path) is not None,
            "publication_bridge_path_required")
    host = "[::1]" if parts.hostname == "::1" else "127.0.0.1"
    return f"http://{host}" + (f":{port}" if port is not None else "") + parts.path.rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise BridgeError("redirect_forbidden")


def request(base: str, payload: dict | None, timeout: float) -> bytes:
    base = normalize_url(base)
    require(math.isfinite(timeout) and 0 < timeout <= 60, "invalid_timeout")
    body = None if payload is None else encode(payload)
    req = urllib.request.Request(base + ("/health" if payload is None else "/command"),
                                 data=body, method="GET" if body is None else "POST",
                                 headers={"Content-Type": "application/json; charset=utf-8", "Accept": "application/json"})
    # Loopback must never inherit enterprise/system proxy settings or follow redirects.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(req, timeout=timeout) as response:
            require(response.status == 200, "unexpected_http_status")
            require(response.headers.get_content_type() == "application/json", "json_content_type_required")
            require(response.headers.get("Content-Encoding", "identity") == "identity", "encoded_response_forbidden")
            data = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        exc.close()
        raise BridgeError(f"http_error_{exc.code}") from exc
    except (urllib.error.URLError, OSError, TimeoutError, http.client.HTTPException) as exc:
        raise BridgeError("bridge_unreachable_or_timeout") from exc
    decode(data)
    return data


def validate_health(value: dict, expected: str) -> None:
    require(value.get("ok") is True and value.get("service") == "CodexTestBridge", "bridge_health_failed")
    require(value.get("metadataName") == expected, "test_configuration_mismatch")


def build_payload(operation: str, *, sections: list[str] | None = None,
                  kind: str = "", name: str = "", text: str = "", params: dict | None = None,
                  limit: int = 100) -> dict | None:
    if operation == "health":
        return None
    if operation == "metadata":
        selected = sections if sections is not None else sorted(SECTIONS)
        require(bool(selected) and all(section in SECTIONS for section in selected), "unsupported_metadata_section")
        return {"command": "Metadata", "sections": selected}
    if operation == "describe":
        require(kind in {"catalog", "document", "enum"} and bool(re.fullmatch(r"[^\W\d]\w*", name)),
                "invalid_metadata_object")
        return {"command": "Describe", "kind": kind, "name": name}
    if operation == "query":
        require(isinstance(text, str) and 0 < len(text) <= 100_000 and text.strip(), "query_text_required")
        require(isinstance(params, (dict, type(None))), "query_params_object_required")
        require(type(limit) is int and 1 <= limit <= 1000, "query_limit_out_of_range")
        return {"command": "Query", "text": text, "params": params or {}, "limit": limit}
    raise BridgeError("operation_not_read_only")


def validate_response(operation: str, value: dict, payload: dict | None, expected: str) -> dict:
    require(value.get("ok") is True, "bridge_command_failed")
    if operation == "health":
        validate_health(value, expected)
    elif operation == "metadata":
        require(value.get("metadataName") == expected, "test_configuration_mismatch")
        require(all(isinstance(value.get(section), list) for section in payload["sections"]), "invalid_metadata_response")
    elif operation == "describe":
        require(isinstance(value.get("object"), dict) and isinstance(value.get("attributes"), list)
                and isinstance(value.get("tableParts"), list), "invalid_describe_response")
    elif operation == "query":
        rows = value.get("rows")
        require(isinstance(rows, list) and all(isinstance(row, dict) for row in rows), "invalid_query_rows")
        require(type(value.get("count")) is int and value["count"] == len(rows) <= payload["limit"],
                "invalid_query_count")
        return {"returned_rows": len(rows), "limit_reached": len(rows) == payload["limit"],
                "population_complete": False,
                "reason": "query_scope_and_population_require_independent_reconciliation"}
    else:
        raise BridgeError("operation_not_read_only")
    return {"population_complete": False, "reason": "metadata_or_health_is_not_business_validation"}


def capture(*, base_url: str, expected_metadata_name: str, test_contour: bool, operation: str,
            payload: dict | None, case_id: str, evidence_ids: list[str], analytic_key: str,
            output: Path, timeout: float = 10) -> dict:
    base = normalize_url(base_url)
    require(test_contour is True, "explicit_test_contour_required")
    require(bool(expected_metadata_name.strip()) and bool(case_id.strip()) and bool(analytic_key.strip())
            and bool(evidence_ids) and all(isinstance(item, str) and item.strip() for item in evidence_ids),
            "case_and_contour_identity_required")
    require(math.isfinite(timeout) and 0 < timeout <= 60, "invalid_timeout")
    # Rebuild the allowlisted request even for direct library callers; arbitrary command bodies are forbidden.
    arguments = {} if payload is None else {key: value for key, value in payload.items() if key != "command"}
    require(build_payload(operation, **arguments) == payload, "request_contract_mismatch")
    require(not output.exists() and not output.is_symlink(), "new_output_directory_required")
    output.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    health_raw = request(base, None, timeout)
    validate_health(decode(health_raw), expected_metadata_name)
    response_raw = health_raw if operation == "health" else request(base, payload, timeout)
    coverage = validate_response(operation, decode(response_raw), payload, expected_metadata_name)
    request_record = {"method": "GET" if payload is None else "POST", "base_url": base,
                      "operation": operation, "payload": payload}
    artifacts = {"request.json": encode(request_record), "health.json": health_raw, "response.json": response_raw}
    manifest = {
        "schema_version": 1, "status": "captured", "run_id": str(uuid.uuid4()),
        "case_id": case_id, "evidence_ids": evidence_ids, "analytic_key": analytic_key,
        "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(),
        "test_contour_declared": True, "expected_metadata_name": expected_metadata_name,
        "protocol_reference": {"repository": REVIEWED_SOURCE, "reviewed_commit": REVIEWED_COMMIT,
                               "installed_bridge_commit": "not_attested_by_health"},
        "adapter_sha256": sha256(Path(__file__).read_bytes()), "coverage": coverage,
        "files": {name: {"sha256": sha256(data), "bytes": len(data)} for name, data in artifacts.items()},
        "limitations": ["Health identifies configuration name, not a unique infobase or immutable data snapshot.",
                        "Capture integrity is not proof of business correctness or ERP causality.",
                        "Query limit bounds returned rows, not server execution time or memory."],
    }
    for name, data in artifacts.items():
        (output / name).write_bytes(data)
    # Manifest is written last: an incomplete directory is never a successful capture.
    (output / "manifest.json").write_bytes(encode(manifest))
    return manifest


def verify(bundle: Path, *, case_id: str, evidence_ids: list[str], analytic_key: str) -> dict:
    """Offline integrity/context check. Does not attest freshness or authenticate a server."""
    require(bundle.is_dir() and not bundle.is_symlink(), "invalid_bundle_directory")

    def read(name):
        path = bundle / name
        require(path.is_file() and not path.is_symlink(), "missing_or_linked_bundle_file")
        with path.open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
        require(len(data) <= MAX_BYTES, "response_too_large")
        return data

    manifest = decode(read("manifest.json"))
    require(manifest.get("schema_version") == 1 and manifest.get("status") == "captured"
            and manifest.get("test_contour_declared") is True, "invalid_manifest")
    require(manifest.get("case_id") == case_id and manifest.get("evidence_ids") == evidence_ids
            and manifest.get("analytic_key") == analytic_key, "evidence_context_mismatch")
    require(isinstance(manifest.get("files"), dict)
            and set(manifest["files"]) == {"request.json", "health.json", "response.json"}, "invalid_bundle_files")
    artifacts = {}
    for name, identity in manifest["files"].items():
        data = read(name)
        require(identity == {"sha256": sha256(data), "bytes": len(data)}, "artifact_hash_mismatch")
        artifacts[name] = decode(data)
    expected = manifest.get("expected_metadata_name")
    require(isinstance(expected, str) and bool(expected.strip()), "invalid_contour_identity")
    validate_health(artifacts["health.json"], expected)
    recorded = artifacts["request.json"]
    require(normalize_url(recorded["base_url"]) == recorded["base_url"], "invalid_recorded_endpoint")
    operation, payload = recorded["operation"], recorded["payload"]
    require(payload is None or isinstance(payload, dict), "invalid_recorded_payload")
    arguments = {} if payload is None else {key: value for key, value in payload.items() if key != "command"}
    require(build_payload(operation, **arguments) == payload, "request_contract_mismatch")
    require(recorded["method"] == ("GET" if payload is None else "POST"), "invalid_recorded_method")
    require(manifest["coverage"] == validate_response(operation, artifacts["response.json"], payload, expected),
            "coverage_mismatch")
    return {"status": "integrity_verified", "run_id": manifest["run_id"], "freshness": "not_verified",
            "population_complete": False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    read = sub.add_parser("capture")
    read.add_argument("operation", choices=["health", "metadata", "describe", "query"])
    read.add_argument("--base-url", required=True)
    read.add_argument("--expected-metadata-name", required=True)
    read.add_argument("--test-contour", action="store_true", required=True)
    read.add_argument("--output", required=True, type=Path)
    read.add_argument("--timeout", type=float, default=10)
    read.add_argument("--sections", nargs="+", choices=sorted(SECTIONS))
    read.add_argument("--kind", choices=["catalog", "document", "enum"], default="")
    read.add_argument("--name", default="")
    read.add_argument("--query-file", type=Path)
    read.add_argument("--params-file", type=Path)
    read.add_argument("--limit", type=int, default=100)
    check = sub.add_parser("verify")
    check.add_argument("--bundle", required=True, type=Path)
    for command in (read, check):
        command.add_argument("--case-id", required=True)
        command.add_argument("--evidence-id", action="append", required=True)
        command.add_argument("--analytic-key", required=True)
    args = parser.parse_args(argv)
    try:
        context = dict(case_id=args.case_id, evidence_ids=args.evidence_id, analytic_key=args.analytic_key)
        if args.mode == "verify":
            result = verify(args.bundle, **context)
        else:
            require(args.operation == "query" or not (args.query_file or args.params_file), "query_options_out_of_scope")
            text = args.query_file.read_text(encoding="utf-8-sig") if args.query_file else ""
            params = decode(args.params_file.read_bytes()) if args.params_file else None
            payload = build_payload(args.operation, sections=args.sections, kind=args.kind, name=args.name,
                                    text=text, params=params, limit=args.limit)
            manifest = capture(base_url=args.base_url, expected_metadata_name=args.expected_metadata_name,
                               test_contour=args.test_contour, operation=args.operation, payload=payload,
                               output=args.output, timeout=args.timeout, **context)
            result = {"status": manifest["status"], "run_id": manifest["run_id"], "coverage": manifest["coverage"]}
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (BridgeError, OSError, ValueError, TypeError, KeyError) as exc:
        reason = str(exc) if isinstance(exc, BridgeError) else "invalid_input_or_bundle"
        print(json.dumps({"status": "failed", "reason": reason}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
