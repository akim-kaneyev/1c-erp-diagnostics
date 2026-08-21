#!/usr/bin/env python3
"""Strictly validate a complete clean-session plugin evaluation run."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from validate_evals import load_suite, validate_result

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = (
    ROOT / "plugins" / "one-c-erp-diagnostics" / ".codex-plugin" / "plugin.json"
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
RUN_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RUN_KEYS = {
    "schema_version",
    "run_id",
    "suite",
    "plugin_version",
    "source_commit",
    "executed_at",
    "environment",
    "results",
}
ENVIRONMENT_KEYS = {
    "surface",
    "host",
    "clean_session",
    "installed_plugin_version",
    "expectations_visible_to_runner",
}
RESULT_ENTRY_KEYS = {"case_id", "file", "sha256"}


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
    except Exception as exc:  # noqa: BLE001 - strict validator reports malformed evidence
        add(errors, str(path), f"invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        add(errors, str(path), "JSON root must be an object")
        return {}
    return value


def nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def current_plugin_version(errors: list[str]) -> str:
    manifest = load_object(PLUGIN_MANIFEST, errors)
    value = manifest.get("version")
    if not nonempty_text(value):
        add(errors, str(PLUGIN_MANIFEST), "manifest version is missing")
        return ""
    return str(value)


def parse_timestamp(value: Any, errors: list[str], location: str) -> None:
    if not nonempty_text(value):
        add(errors, location, "must be a non-empty ISO-8601 timestamp")
        return
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        add(errors, location, "must be a valid ISO-8601 timestamp")
        return
    if parsed.tzinfo is None:
        add(errors, location, "must include an explicit timezone")


def validate_runtime_run(run_dir: Path) -> list[str]:
    errors: list[str] = []
    suite, cases, suite_errors = load_suite()
    errors.extend(suite_errors)
    expected_version = current_plugin_version(errors)

    run_dir = run_dir.resolve()
    if not run_dir.is_dir():
        add(errors, str(run_dir), "runtime run directory does not exist")
        return errors
    manifest_path = run_dir / "run.json"
    if not manifest_path.is_file():
        add(errors, str(manifest_path), "run manifest is missing")
        return errors
    manifest = load_object(manifest_path, errors)
    check_exact_keys(manifest, RUN_KEYS, errors, "run.json")

    if manifest.get("schema_version") != 1:
        add(errors, "run.json", "schema_version must be 1")
    run_id = manifest.get("run_id")
    if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id):
        add(errors, "run.json", "run_id must be lower-case hyphen-case")
    if manifest.get("suite") != suite.get("name"):
        add(errors, "run.json", "suite must match evals/suite.json name")
    if manifest.get("plugin_version") != expected_version:
        add(
            errors,
            "run.json",
            f"plugin_version must match current manifest version {expected_version!r}",
        )
    source_commit = manifest.get("source_commit")
    if not isinstance(source_commit, str) or not COMMIT.fullmatch(source_commit):
        add(errors, "run.json", "source_commit must be a 40-character lower-case Git SHA")
    elif source_commit == "0" * 40:
        add(errors, "run.json", "source_commit cannot be the all-zero placeholder")
    parse_timestamp(manifest.get("executed_at"), errors, "run.json.executed_at")

    environment = manifest.get("environment")
    if not isinstance(environment, dict):
        add(errors, "run.json", "environment must be an object")
        environment = {}
    else:
        check_exact_keys(environment, ENVIRONMENT_KEYS, errors, "run.json.environment")
    for field in ("surface", "host", "installed_plugin_version"):
        if not nonempty_text(environment.get(field)):
            add(errors, "run.json.environment", f"{field} must be non-empty text")
    if environment.get("clean_session") is not True:
        add(errors, "run.json.environment", "clean_session must be true")
    if environment.get("installed_plugin_version") != expected_version:
        add(
            errors,
            "run.json.environment",
            f"installed_plugin_version must be {expected_version!r}",
        )
    if environment.get("expectations_visible_to_runner") is not False:
        add(
            errors,
            "run.json.environment",
            "expectations_visible_to_runner must be false",
        )

    entries = manifest.get("results")
    if not isinstance(entries, list):
        add(errors, "run.json", "results must be a list")
        entries = []

    run_root = run_dir.resolve()
    seen: set[str] = set()
    referenced_files: set[Path] = set()
    for index, entry in enumerate(entries):
        location = f"run.json.results[{index}]"
        if not isinstance(entry, dict):
            add(errors, location, "must be an object")
            continue
        check_exact_keys(entry, RESULT_ENTRY_KEYS, errors, location)
        case_id = entry.get("case_id")
        if not isinstance(case_id, str) or case_id not in cases:
            add(errors, location, f"unknown case_id {case_id!r}")
            continue
        if case_id in seen:
            add(errors, location, f"duplicate case_id {case_id!r}")
            continue
        seen.add(case_id)

        relative_file = entry.get("file")
        if not nonempty_text(relative_file):
            add(errors, location, "file must be a non-empty relative path")
            continue
        result_path = (run_dir / str(relative_file)).resolve()
        try:
            result_path.relative_to(run_root)
        except ValueError:
            add(errors, location, "result file escapes the run directory")
            continue
        if result_path in referenced_files:
            add(errors, location, f"result file is referenced more than once: {relative_file}")
        referenced_files.add(result_path)
        if not result_path.is_file():
            add(errors, location, f"result file is missing: {relative_file}")
            continue
        if not result_path.name.endswith(".result.json"):
            add(errors, location, "result filename must end with .result.json")

        expected_hash = entry.get("sha256")
        if not isinstance(expected_hash, str) or not SHA256.fullmatch(expected_hash):
            add(errors, location, "sha256 must be 64 lower-case hexadecimal characters")
        elif expected_hash == "0" * 64:
            add(errors, location, "sha256 cannot be the all-zero placeholder")
        else:
            actual_hash = hashlib.sha256(result_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                add(errors, location, f"SHA-256 mismatch for {relative_file}")

        result = load_object(result_path, errors)
        errors.extend(validate_result(result, cases[case_id], str(result_path)))

    missing = sorted(set(cases) - seen)
    if missing:
        add(errors, "run.json", "missing complete-suite results: " + ", ".join(missing))
    if len(entries) != len(cases):
        add(
            errors,
            "run.json",
            f"results must contain exactly {len(cases)} entries, found {len(entries)}",
        )

    unreferenced = sorted(
        str(path.relative_to(run_root))
        for path in run_dir.glob("*.result.json")
        if path.resolve() not in referenced_files
    )
    if unreferenced:
        add(errors, "run.json", "unreferenced result files: " + ", ".join(unreferenced))

    return errors


def main() -> int:
    configure_utf8_output()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Directory containing run.json and *.result.json")
    args = parser.parse_args()

    errors = validate_runtime_run(args.run_dir)
    if errors:
        print("RUNTIME ACCEPTANCE: BLOCKED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("RUNTIME ACCEPTANCE: PASS")
    print(f"Run: {args.run_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
