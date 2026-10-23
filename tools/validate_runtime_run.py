#!/usr/bin/env python3
"""Strictly validate a complete clean-session plugin evaluation run."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from update_skill_lock import canonical_file_bytes
from validate_evals import load_suite, validate_result
from validate_runtime_log import inspect_runtime_log

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
    "installed_plugin_tree_sha256",
    "expectations_visible_to_runner",
    "web_search",
    "working_directory_isolated",
    "runner_tool_policy",
}
RESULT_ENTRY_KEYS = {"case_id", "file", "sha256", "log_file", "log_sha256"}
RUNNER_TOOL_POLICY = "no-tools"


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


def current_source_commit(errors: list[str]) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    value = completed.stdout.strip()
    if completed.returncode != 0 or not COMMIT.fullmatch(value):
        add(errors, str(ROOT), "cannot resolve current Git HEAD")
        return ""
    return value


def require_clean_worktree(errors: list[str]) -> None:
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        add(errors, str(ROOT), "cannot verify Git worktree cleanliness")
    elif completed.stdout.strip():
        add(errors, str(ROOT), "Git worktree must be clean for runtime acceptance")


def plugin_tree_sha256(plugin_root: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(
        path
        for path in plugin_root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix.casefold() != ".pyc"
    )
    for path in files:
        relative = path.relative_to(plugin_root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(canonical_file_bytes(path))
        digest.update(b"\0")
    return digest.hexdigest()


def current_plugin_tree_sha256() -> str:
    return plugin_tree_sha256(PLUGIN_MANIFEST.parent.parent)


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
    expected_commit = current_source_commit(errors)
    expected_plugin_tree = current_plugin_tree_sha256()
    require_clean_worktree(errors)

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

    if manifest.get("schema_version") != 2:
        add(errors, "run.json", "schema_version must be 2")
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
    elif source_commit != expected_commit:
        add(errors, "run.json", f"source_commit must match current Git HEAD {expected_commit!r}")
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
    installed_tree = environment.get("installed_plugin_tree_sha256")
    if installed_tree != expected_plugin_tree:
        add(
            errors,
            "run.json.environment",
            "installed_plugin_tree_sha256 must match the current packaged plugin tree",
        )
    if environment.get("expectations_visible_to_runner") is not False:
        add(
            errors,
            "run.json.environment",
            "expectations_visible_to_runner must be false",
        )
    if environment.get("web_search") != "disabled":
        add(errors, "run.json.environment", "web_search must be 'disabled'")
    if environment.get("working_directory_isolated") is not True:
        add(errors, "run.json.environment", "working_directory_isolated must be true")
    if environment.get("runner_tool_policy") != RUNNER_TOOL_POLICY:
        add(
            errors,
            "run.json.environment",
            f"runner_tool_policy must be {RUNNER_TOOL_POLICY!r}",
        )

    entries = manifest.get("results")
    if not isinstance(entries, list):
        add(errors, "run.json", "results must be a list")
        entries = []

    run_root = run_dir.resolve()
    seen: set[str] = set()
    referenced_files: set[Path] = set()
    referenced_logs: set[Path] = set()
    seen_session_ids: set[str] = set()
    seen_workdirs: set[str] = set()
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
        if relative_file != f"{case_id}.result.json":
            add(errors, location, f"file must be {case_id}.result.json")
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

        relative_log = entry.get("log_file")
        if not nonempty_text(relative_log):
            add(errors, location, "log_file must be a non-empty relative path")
            continue
        if relative_log != f"{case_id}.log":
            add(errors, location, f"log_file must be {case_id}.log")
        log_path = (run_dir / str(relative_log)).resolve()
        try:
            log_path.relative_to(run_root)
        except ValueError:
            add(errors, location, "log file escapes the run directory")
            continue
        if log_path in referenced_logs:
            add(errors, location, f"log file is referenced more than once: {relative_log}")
        referenced_logs.add(log_path)
        if not log_path.is_file():
            add(errors, location, f"log file is missing: {relative_log}")
            continue
        if log_path.suffix.casefold() != ".log":
            add(errors, location, "log filename must end with .log")

        expected_log_hash = entry.get("log_sha256")
        if not isinstance(expected_log_hash, str) or not SHA256.fullmatch(expected_log_hash):
            add(errors, location, "log_sha256 must be 64 lower-case hexadecimal characters")
        elif expected_log_hash == "0" * 64:
            add(errors, location, "log_sha256 cannot be the all-zero placeholder")
        else:
            actual_log_hash = hashlib.sha256(log_path.read_bytes()).hexdigest()
            if actual_log_hash != expected_log_hash:
                add(errors, location, f"SHA-256 mismatch for {relative_log}")
        log_errors, log_metadata, logged_result = inspect_runtime_log(log_path, case_id)
        errors.extend(log_errors)
        session_id = log_metadata.get("session_id")
        if session_id:
            if session_id in seen_session_ids:
                add(errors, location, f"clean-session id is reused: {session_id}")
            seen_session_ids.add(session_id)
        workdir = log_metadata.get("workdir")
        if workdir:
            workdir_key = str(Path(workdir).resolve()).casefold()
            if workdir_key in seen_workdirs:
                add(errors, location, f"isolated workdir is reused: {workdir}")
            seen_workdirs.add(workdir_key)
            try:
                Path(workdir).resolve().relative_to(ROOT.resolve())
            except ValueError:
                pass
            else:
                add(errors, location, "runtime workdir must be outside the repository")
        if logged_result is not None and logged_result != result:
            add(errors, location, "final JSON in the Codex log does not match the result file")

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
    unreferenced_logs = sorted(
        str(path.relative_to(run_root))
        for path in run_dir.glob("*.log")
        if path.resolve() not in referenced_logs
    )
    if unreferenced_logs:
        add(errors, "run.json", "unreferenced log files: " + ", ".join(unreferenced_logs))

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
