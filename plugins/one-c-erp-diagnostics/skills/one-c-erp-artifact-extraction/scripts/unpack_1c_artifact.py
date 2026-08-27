#!/usr/bin/env python3
"""Safely extract a sanitized 1C CF/CFE/EPF and write a provenance manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

SUPPORTED_SUFFIXES = {".cf", ".cfe", ".epf"}
EXPECTED_VERSION = "1.2.6"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_paths(source: Path, output: Path, replace: bool) -> None:
    if not source.is_file():
        raise ValueError(f"Source is not a file: {source}")
    if source.suffix.lower() not in SUPPORTED_SUFFIXES:
        allowed = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise ValueError(f"Unsupported or unverified artifact type: {source.suffix or '<none>'}; allowed: {allowed}")
    if source.resolve() == output.resolve():
        raise ValueError("Source and output paths must differ")
    if output.exists() and not output.is_dir():
        raise ValueError(f"Output is not a directory: {output}")
    if output.exists() and any(output.iterdir()):
        if not replace:
            raise ValueError(f"Output directory is not empty: {output}; use --replace explicitly")
        shutil.rmtree(output)


def build_manifest(source: Path, output: Path, detected_version: str) -> dict:
    files = [path for path in output.rglob("*") if path.is_file()]
    suffixes = Counter(path.suffix.lower() or "<none>" for path in files)
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "read-only extraction; extracted 1C code was not executed",
        "source": {
            "name": source.name,
            "size_bytes": source.stat().st_size,
            "sha256": sha256_file(source),
        },
        "tool": {
            "name": "v8unpack",
            "version": detected_version,
            "expected_version": EXPECTED_VERSION,
        },
        "output": {
            "directory": str(output.resolve()),
            "file_count": len(files),
            "suffix_counts": dict(sorted(suffixes.items())),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--processes", type=int, default=None)
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    try:
        validate_paths(source, output, args.replace)
        try:
            detected_version = version("v8unpack")
        except PackageNotFoundError as exc:
            raise RuntimeError("Install the optional artifact dependency: pip install -e '.[artifacts]'") from exc
        if detected_version != EXPECTED_VERSION:
            raise RuntimeError(f"v8unpack {detected_version} is installed; expected {EXPECTED_VERSION}")

        import v8unpack  # type: ignore[import-not-found]

        output.mkdir(parents=True, exist_ok=True)
        v8unpack.extract(str(source), str(output), processes=args.processes)
        manifest = build_manifest(source, output, detected_version)
        manifest_path = output / "_extraction_manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(manifest_path)
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI returns a controlled diagnostic
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
