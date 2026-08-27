#!/usr/bin/env python3
"""Validate release archive identity and scan the complete Git history for unsafe residue."""

from __future__ import annotations

import io
import codecs
import re
import subprocess
import sys
import tarfile
from pathlib import PurePosixPath

FORBIDDEN_SUFFIXES = {
    ".dt", ".1cd", ".bak", ".backup", ".key", ".pem", ".pfx", ".p12", ".ppk",
    ".jks", ".keystore", ".kdbx", ".xlsx", ".xlsm", ".xltx", ".xltm",
    ".xls", ".docx", ".docm", ".doc", ".pptx", ".pptm", ".ppt", ".zip",
}
FORBIDDEN_CONTAINER_SIGNATURES = (
    b"PK\x03\x04",
    b"PK\x05\x06",
    b"PK\x07\x08",
    b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",  # OLE/CFBF, including encrypted Office packages.
)
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
ABSOLUTE_MACHINE_PATH = re.compile(
    r"(?:file:/+(?:[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+|"
    r"(?:Users|home)/[^/\s]+)|"
    r"(?<![A-Za-z0-9._:/-])[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+|"
    r"(?<![A-Za-z0-9._:/-])/(?:Users|home)/[^/\s]+)",
    re.IGNORECASE,
)
SCAN_TAIL_CHARS = 2048
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
    if pure.is_absolute() or ".." in pure.parts or re.match(r"^[A-Za-z]:/", normalized):
        return "absolute or traversal path"
    lower_name = pure.name.lower()
    if pure.suffix.lower() in FORBIDDEN_SUFFIXES:
        return "forbidden artifact suffix"
    if lower_name == ".env" or lower_name.startswith(".env."):
        return "environment file"
    if normalized.casefold().startswith("cases/") and lower_name != ".gitkeep":
        return "case data"
    has_secret, has_machine_path = text_findings(path)
    if has_secret:
        return "credential-like path"
    if has_machine_path:
        return "user-machine path"
    return None


def unsafe_link_target(target: str) -> str | None:
    normalized = target.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if (
        pure.is_absolute()
        or ".." in pure.parts
        or re.match(r"^[A-Za-z]:/", normalized)
        or normalized.startswith("//")
    ):
        return "absolute or traversal link target"
    if ABSOLUTE_MACHINE_PATH.search(target):
        return "user-machine path in link target"
    return None


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


def text_findings(value: str) -> tuple[bool, bool]:
    normalized, unresolved_escape = normalize_security_text(value)
    upper = normalized.upper()
    has_secret = (
        unresolved_escape
        or SECRET_ASSIGNMENT.search(normalized) is not None
        or BEARER_AUTHORIZATION.search(normalized) is not None
        or PRIVATE_KEY_HEADER.search(normalized) is not None
        or PUTTY_PRIVATE_KEY_HEADER.search(normalized) is not None
        or SSH2_PRIVATE_KEY_HEADER.search(normalized) is not None
        or any(marker in upper for marker in PRIVATE_KEY_MARKERS)
    )
    has_machine_path = (
        ABSOLUTE_MACHINE_PATH.search(value) is not None
        or ABSOLUTE_MACHINE_PATH.search(normalized) is not None
    )
    return has_secret, has_machine_path


def safe_path_label(path: str) -> str:
    has_secret, has_machine_path = text_findings(path)
    return "[REDACTED_PATH]" if has_secret or has_machine_path else path


def stream_text_findings(stream) -> tuple[bool, bool, bool]:
    """Scan all bytes incrementally; values are never returned or logged."""
    states = [
        [codecs.getincrementaldecoder(encoding)(errors="ignore"), ""]
        for encoding in ("utf-8", "utf-16-le", "utf-16-be", "utf-32-le", "utf-32-be")
    ]
    has_secret = False
    has_machine_path = False
    has_forbidden_container = False
    binary_tail = b""
    max_signature_length = max(len(signature) for signature in FORBIDDEN_CONTAINER_SIGNATURES)
    while True:
        chunk = stream.read(1024 * 1024)
        if not chunk:
            break
        binary_window = binary_tail + chunk
        has_forbidden_container = has_forbidden_container or any(
            signature in binary_window for signature in FORBIDDEN_CONTAINER_SIGNATURES
        )
        binary_tail = binary_window[-(max_signature_length - 1):]
        for state in states:
            decoder, tail = state
            text = str(tail) + decoder.decode(chunk)
            found_secret, found_path = text_findings(text)
            has_secret = has_secret or found_secret
            has_machine_path = has_machine_path or found_path
            state[1] = text[-SCAN_TAIL_CHARS:]
    for decoder, tail in states:
        final = str(tail) + decoder.decode(b"", final=True)
        found_secret, found_path = text_findings(final)
        has_secret = has_secret or found_secret
        has_machine_path = has_machine_path or found_path
    return has_secret, has_machine_path, has_forbidden_container


def inspect_git_object(oid: str, object_type: str) -> tuple[bool, bool, bool]:
    process = subprocess.Popen(
        ["git", "cat-file", object_type, oid],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.stdout is None:
        raise subprocess.CalledProcessError(1, process.args)
    findings = stream_text_findings(process.stdout)
    _, stderr = process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, process.args, stderr=stderr)
    return findings


def inspect_reachable_objects(
    object_lines, read_type, inspect_object
) -> tuple[dict[str, int], list[str], set[str]]:
    """Scan reachable content objects, including pathless blobs and commit/tag metadata."""
    seen: set[str] = set()
    counts = {"blob": 0, "commit": 0, "tag": 0}
    errors: list[str] = []
    tree_ids: set[str] = set()
    for line in object_lines:
        if not line.strip():
            continue
        oid, _, path = line.partition(" ")
        if oid in seen:
            continue
        try:
            object_type = read_type(oid).strip()
            if object_type == "tree":
                seen.add(oid)
                tree_ids.add(oid)
                continue
            if object_type not in counts:
                seen.add(oid)
                continue
            has_secret, has_machine_path, has_forbidden_container = inspect_object(
                oid, object_type
            )
        except subprocess.CalledProcessError:
            continue
        seen.add(oid)
        counts[object_type] += 1
        label = (
            safe_path_label(path)
            if path
            else f"[PATHLESS_GIT_{object_type.upper()}:{oid[:12]}]"
        )
        path_reason = unsafe_path(path) if path else None
        if path_reason:
            errors.append(
                f"unsafe path exists in Git history ({path_reason}): {label}"
            )
        if has_secret:
            errors.append(
                "possible plaintext credential exists in Git history object: " + label
            )
        if has_machine_path:
            errors.append(
                "absolute user-machine path exists in Git history object: " + label
            )
        if has_forbidden_container:
            errors.append(
                "nested ZIP/Office container exists in Git history object: " + label
            )
    return counts, errors, tree_ids


def inspect_archive(archive_bytes: bytes) -> tuple[list[str], list[str]]:
    """Inspect the actual release tar without returning matched secret values."""
    archived: list[str] = []
    errors: list[str] = []
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
        for member in archive.getmembers():
            if not (member.isfile() or member.issym() or member.islnk()):
                continue
            path = member.name.rstrip("/")
            archived.append(path)
            safe_path = safe_path_label(path)
            reason = unsafe_path(path)
            if reason:
                errors.append(f"unsafe path exists in release archive ({reason}): {safe_path}")
            if member.issym() or member.islnk():
                link_reason = unsafe_link_target(member.linkname)
                if link_reason:
                    errors.append(f"unsafe archive link target ({link_reason}): {safe_path}")
                continue
            if not member.isfile():
                continue
            stream = archive.extractfile(member)
            if stream is None:
                continue
            has_secret, has_machine_path, has_forbidden_container = stream_text_findings(stream)
            if has_secret:
                errors.append(f"possible plaintext credential exists in release archive: {safe_path}")
            if has_machine_path:
                errors.append(f"absolute user-machine path exists in release archive: {safe_path}")
            if has_forbidden_container:
                errors.append(f"nested ZIP/Office container exists in release archive: {safe_path}")
    return sorted(archived), errors


def inspect_historical_symlink_entries(tree_bytes: bytes, read_blob) -> tuple[int, list[str]]:
    """Inspect every reachable tree path and each symlink target.

    Object traversal may report one path only for a blob shared by several trees.
    Path policy therefore belongs to tree entries, while blob content can remain
    deduplicated by object ID in ``inspect_reachable_objects``.
    """
    inspected = 0
    errors: list[str] = []
    for raw_entry in tree_bytes.split(b"\0"):
        if not raw_entry or b"\t" not in raw_entry:
            continue
        metadata, raw_path = raw_entry.split(b"\t", 1)
        path = raw_path.decode("utf-8", errors="replace")
        path_reason = unsafe_path(path)
        if path_reason:
            errors.append(
                f"unsafe path exists in Git history ({path_reason}): "
                f"{safe_path_label(path)}"
            )
        fields = metadata.split(b" ", 2)
        if len(fields) != 3 or fields[0] != b"120000" or fields[1] != b"blob":
            continue
        inspected += 1
        oid = fields[2].decode("ascii", errors="ignore")
        target = read_blob(oid).decode("utf-8", errors="ignore")
        reason = unsafe_link_target(target)
        if reason:
            errors.append(
                f"unsafe historical link target ({reason}): {safe_path_label(path)}"
            )
    return inspected, errors


def commit_root_tree_ids(object_lines, read_type, read_commit) -> set[str]:
    """Return root trees of every reachable commit without promoting nested trees."""
    roots: set[str] = set()
    seen: set[str] = set()
    for line in object_lines:
        oid, _, _path = line.partition(" ")
        if not oid or oid in seen:
            continue
        seen.add(oid)
        try:
            if read_type(oid).strip() != "commit":
                continue
            commit_bytes = read_commit(oid)
        except subprocess.CalledProcessError:
            continue
        first_line = commit_bytes.partition(b"\n")[0]
        if first_line.startswith(b"tree "):
            tree_id = first_line[5:].decode("ascii", errors="ignore").strip()
            if tree_id:
                roots.add(tree_id)
    return roots


def referenced_root_tree_ids(ref_names, resolve_tree) -> set[str]:
    """Return tree roots peeled directly from refs, including standalone tree tags."""
    roots: set[str] = set()
    for ref_name in ref_names:
        ref_name = ref_name.strip()
        if not ref_name:
            continue
        try:
            tree_id = resolve_tree(ref_name).strip()
        except subprocess.CalledProcessError:
            continue
        if tree_id:
            roots.add(tree_id)
    return roots


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
    archived, archive_errors = inspect_archive(archive_bytes)
    errors.extend(archive_errors)
    if tracked != archived:
        missing = [safe_path_label(path) for path in sorted(set(tracked) - set(archived))]
        extra = [safe_path_label(path) for path in sorted(set(archived) - set(tracked))]
        errors.append(f"git archive tree mismatch; missing={missing}, extra={extra}")

    history_paths = sorted(set(line for line in git("log", "--all", "--format=", "--name-only").splitlines() if line))
    for path in history_paths:
        reason = unsafe_path(path)
        if reason:
            errors.append(
                f"unsafe path exists in Git history ({reason}): {safe_path_label(path)}"
            )

    object_lines = git("rev-list", "--objects", "--all").splitlines()
    object_counts, object_errors, _tree_ids = inspect_reachable_objects(
        object_lines,
        lambda oid: git("cat-file", "-t", oid),
        inspect_git_object,
    )
    errors.extend(object_errors)

    root_tree_ids = commit_root_tree_ids(
        object_lines,
        lambda oid: git("cat-file", "-t", oid),
        lambda oid: git("cat-file", "commit", oid, binary=True),
    )
    ref_names = git("for-each-ref", "--format=%(refname)").splitlines()
    root_tree_ids.update(
        referenced_root_tree_ids(
            ref_names,
            lambda ref_name: git("rev-parse", "--verify", f"{ref_name}^{{tree}}"),
        )
    )

    historical_symlinks = 0
    historical_symlink_errors: set[str] = set()
    for tree_id in root_tree_ids:
        tree_bytes = git("ls-tree", "-rz", "--full-tree", tree_id, binary=True)
        inspected, link_errors = inspect_historical_symlink_entries(
            tree_bytes,
            lambda oid: git("cat-file", "-p", oid, binary=True),
        )
        historical_symlinks += inspected
        historical_symlink_errors.update(link_errors)
    errors.extend(sorted(historical_symlink_errors))

    errors = sorted(set(errors))
    if errors:
        print("PUBLICATION HISTORY VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("PUBLICATION HISTORY VALIDATION: PASS")
    print(f"Tracked files: {len(tracked)}")
    print(f"Historical paths inspected: {len(history_paths)}")
    print(f"Historical root trees inspected: {len(root_tree_ids)}")
    print(f"Historical symlink entries inspected: {historical_symlinks}")
    print(
        "Unique Git objects inspected: "
        f"blobs={object_counts['blob']}, commits={object_counts['commit']}, tags={object_counts['tag']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
