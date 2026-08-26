#!/usr/bin/env python3
"""Generate or verify the deterministic SHA-256 lock for runtime skill surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK_NAME = "SKILLS.lock.json"

EXPLICIT_FILES = (
    "AGENTS.md",
    "SKILL.md",
    ".agents/skills/one-c-erp-diagnostics/SKILL.md",
    "skills/one-c-erp-diagnostics/SKILL.md",
    "templates/case/STATE.md",
)
RECURSIVE_ROOTS = (
    "plugins/one-c-erp-diagnostics/skills",
    "playbooks",
    "checklists",
)
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}
IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache"}


def _inside_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def discover_runtime_files(root: Path) -> list[Path]:
    """Return the deterministic set of files that define runtime behavior."""
    root = root.resolve()
    found: dict[str, Path] = {}

    for relative in EXPLICIT_FILES:
        path = root / relative
        if path.is_file():
            found[path.relative_to(root).as_posix()] = path

    for relative in RECURSIVE_ROOTS:
        directory = root / relative
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if not path.is_file() or path.name in IGNORED_NAMES:
                continue
            if any(part in IGNORED_PARTS for part in path.parts):
                continue
            if not _inside_root(path, root):
                raise ValueError(f"Runtime path escapes repository root: {path}")
            found[path.relative_to(root).as_posix()] = path

    return [found[key] for key in sorted(found)]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_lock(root: Path) -> dict:
    root = root.resolve()
    files = []
    for path in discover_runtime_files(root):
        relative = path.relative_to(root).as_posix()
        files.append(
            {
                "path": relative,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )

    canonical_files = json.dumps(
        files,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema_version": 1,
        "algorithm": "sha256",
        "scope": "1C ERP Diagnostics runtime skill, playbook, checklist and state surfaces",
        "file_count": len(files),
        "manifest_sha256": hashlib.sha256(canonical_files).hexdigest(),
        "files": files,
    }


def serialize_lock(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_lock(path: Path, data: dict) -> None:
    """Write the canonical manifest with stable LF endings on every platform."""
    path.write_text(serialize_lock(data), encoding="utf-8", newline="\n")


def load_lock(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Lock root must be a JSON object")
    return value


def check_lock(root: Path, lock_path: Path) -> list[str]:
    errors: list[str] = []
    if not lock_path.is_file():
        return [f"Missing skill lock: {lock_path}"]
    try:
        actual = load_lock(lock_path)
    except Exception as exc:  # noqa: BLE001 - report malformed lock deterministically
        return [f"Invalid skill lock {lock_path}: {exc}"]

    expected = build_lock(root)
    if actual != expected:
        actual_files = {
            item.get("path"): item
            for item in actual.get("files", [])
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        }
        expected_files = {item["path"]: item for item in expected["files"]}
        for path in sorted(set(expected_files) - set(actual_files)):
            errors.append(f"Skill lock is missing runtime file: {path}")
        for path in sorted(set(actual_files) - set(expected_files)):
            errors.append(f"Skill lock contains removed runtime file: {path}")
        for path in sorted(set(actual_files) & set(expected_files)):
            if actual_files[path] != expected_files[path]:
                errors.append(f"Skill lock drift: {path}")
        if not errors:
            errors.append("Skill lock metadata or manifest digest is stale")
        errors.append("Run: python tools/update_skill_lock.py --write")
    return errors


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--output", type=Path, default=None)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write the canonical lock")
    mode.add_argument("--check", action="store_true", help="Verify the tracked lock (default)")
    mode.add_argument("--print", dest="print_lock", action="store_true", help="Print canonical JSON")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    output = (args.output or (root / DEFAULT_LOCK_NAME)).resolve()
    data = build_lock(root)

    if args.print_lock:
        print(serialize_lock(data), end="")
        return 0
    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        write_lock(output, data)
        print(f"Wrote {output}")
        print(f"Locked runtime files: {data['file_count']}")
        print(f"Manifest SHA-256: {data['manifest_sha256']}")
        return 0

    errors = check_lock(root, output)
    if errors:
        print("SKILL LOCK VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("SKILL LOCK VALIDATION: PASS")
    print(f"Locked runtime files: {data['file_count']}")
    print(f"Manifest SHA-256: {data['manifest_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
