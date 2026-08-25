#!/usr/bin/env python3
"""Validate release archive identity and scan the complete Git history for unsafe residue."""

from __future__ import annotations

import io
import re
import subprocess
import sys
import tarfile
from pathlib import PurePosixPath

FORBIDDEN_SUFFIXES = {
    ".dt", ".1cd", ".bak", ".backup", ".key", ".pem", ".pfx", ".p12",
    ".jks", ".keystore", ".kdbx",
}
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:\b(password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret|"
    r"private[_-]?key|sonar[_-]?token)\b|sonar\.(?:token|login))\s*[:=]\s*"
    r"(?:[\"'][^\"'\r\n]{8,}[\"']|[A-Za-z0-9_./+=:-]{16,})"
)
ABSOLUTE_MACHINE_PATH = re.compile(
    r"(?:[A-Za-z]:\\" + "Users" + r"\\[^\\\s]+|/" + "Users" + r"/[^/\s]+|/" + "home" + r"/[^/\s]+)"
)
MAX_BLOB_BYTES = 2_000_000


def git(*args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout if binary else result.stdout.decode("utf-8", errors="replace")


def unsafe_path(path: str) -> str | None:
    normalized = path.replace("\\", "/")
    pure = PurePosixPath(normalized)
    lower_name = pure.name.lower()
    if pure.suffix.lower() in FORBIDDEN_SUFFIXES:
        return "forbidden artifact suffix"
    if lower_name == ".env" or lower_name.startswith(".env."):
        return "environment file"
    if normalized.startswith("cases/") and lower_name != ".gitkeep":
        return "case data"
    return None


def main() -> int:
    errors: list[str] = []

    try:
        if git("rev-parse", "--is-inside-work-tree").strip() != "true":
            errors.append("not inside a Git work tree")
        if git("rev-parse", "--is-shallow-repository").strip() != "false":
            errors.append("Git history is shallow; release history scan requires fetch-depth: 0")
    except subprocess.CalledProcessError as exc:
        print(f"PUBLICATION HISTORY VALIDATION: FAIL\n- Git unavailable: {exc}", file=sys.stderr)
        return 1

    tracked = sorted(line for line in git("ls-files").splitlines() if line)
    archive_bytes = git("archive", "--format=tar", "HEAD", binary=True)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
        archived = sorted(
            member.name.rstrip("/")
            for member in archive.getmembers()
            if member.isfile() or member.issym()
        )
    if tracked != archived:
        missing = sorted(set(tracked) - set(archived))
        extra = sorted(set(archived) - set(tracked))
        errors.append(f"git archive tree mismatch; missing={missing}, extra={extra}")

    history_paths = sorted(set(line for line in git("log", "--all", "--format=", "--name-only").splitlines() if line))
    for path in history_paths:
        reason = unsafe_path(path)
        if reason:
            errors.append(f"unsafe path exists in Git history ({reason}): {path}")

    object_lines = git("rev-list", "--objects", "--all").splitlines()
    seen: set[str] = set()
    for line in object_lines:
        if not line.strip():
            continue
        oid, _, path = line.partition(" ")
        if oid in seen or not path:
            continue
        seen.add(oid)
        try:
            obj_type = git("cat-file", "-t", oid).strip()
            if obj_type != "blob":
                continue
            size = int(git("cat-file", "-s", oid).strip())
            if size > MAX_BLOB_BYTES:
                continue
            data = git("cat-file", "-p", oid, binary=True)
        except (subprocess.CalledProcessError, ValueError):
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET_ASSIGNMENT.search(text):
            errors.append(f"possible plaintext credential exists in Git history: {path or oid}")
        if ABSOLUTE_MACHINE_PATH.search(text):
            errors.append(f"absolute user-machine path exists in Git history: {path or oid}")

    if errors:
        print("PUBLICATION HISTORY VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("PUBLICATION HISTORY VALIDATION: PASS")
    print(f"Tracked files: {len(tracked)}")
    print(f"Historical paths inspected: {len(history_paths)}")
    print(f"Unique small text/blob candidates inspected: {len(seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
