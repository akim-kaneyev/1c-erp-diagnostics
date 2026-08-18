from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main(case_dir: str) -> None:
    root = Path(case_dir).resolve()
    if not root.exists():
        raise SystemExit(f"Case directory not found: {root}")

    input_dir = root / "input"
    files = []
    if input_dir.exists():
        for p in sorted(input_dir.rglob("*")):
            if p.is_file() and p.name != ".gitkeep":
                files.append({
                    "path": str(p.relative_to(root)),
                    "name": p.name,
                    "extension": p.suffix.lower(),
                    "size_bytes": p.stat().st_size,
                    "sha256": sha256(p),
                })

    manifest = {
        "case": root.name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }
    out = root / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Indexed {len(files)} files")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/index_case.py cases/<case-id>")
    main(sys.argv[1])
