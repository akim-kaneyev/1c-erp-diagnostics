from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def transform(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() == ".png":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text = text.replace("akimka-jpg", "akim-kaneyev")
        text = text.replace("akim266@gmail.com", "[private-email-removed]")
        path.write_text(text, encoding="utf-8")

    license_path = root / "LICENSE"
    license_path.write_text(
        license_path.read_text(encoding="utf-8").replace(
            "Copyright (c) 2026 akim-kaneyev",
            "Copyright (c) 2026 Akim Kaneev",
        ),
        encoding="utf-8",
    )

    manifest_path = root / "plugins/one-c-erp-diagnostics/.codex-plugin/plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["repository"] = "https://github.com/akim-kaneyev/1c-erp-diagnostics"
    manifest["interface"]["developerName"] = "Akim Kaneev"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    marketplace_path = root / ".agents/plugins/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    marketplace["name"] = "one-c-erp-diagnostics-marketplace"
    marketplace["interface"]["displayName"] = "1C ERP Diagnostics"
    marketplace_path.write_text(
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    checklist_path = root / "docs/PUBLIC_RELEASE_CHECKLIST.md"
    checklist = checklist_path.read_text(encoding="utf-8")
    checklist = checklist.replace(
        "- [ ] Decide whether to keep `akim-kaneyev` or rename before the first public release.",
        "- [x] Final GitHub username confirmed: `akim-kaneyev`.",
    )
    checklist = checklist.replace(
        "- [ ] If renaming, update repository URLs, plugin manifest, marketplace source, documentation and local remotes before publication.",
        "- [x] Repository URLs, plugin manifest, marketplace metadata and documentation updated to `akim-kaneyev`.",
    )
    checklist = checklist.replace(
        "- [ ] Create public profile repository matching the final username and place `README.md` in its root.",
        "- [ ] Create public profile repository `akim-kaneyev/akim-kaneyev` and place `README.md` in its root.",
    )
    checklist_path.write_text(checklist, encoding="utf-8")

    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    badges = """
<p align="center">
  <a href="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml"><img alt="Validation" src="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml/badge.svg" /></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-gold.svg" /></a>
  <img alt="Version 0.1.2" src="https://img.shields.io/badge/version-0.1.2-0D1B2A.svg" />
  <img alt="1C ERP" src="https://img.shields.io/badge/domain-1C%3AERP-F5B800.svg" />
</p>
"""
    anchor = '<h1 align="center">1C ERP Diagnostics</h1>\n'
    if "actions/workflows/validate.yml/badge.svg" not in readme:
        readme = readme.replace(anchor, anchor + badges)
    readme = readme.replace(
        "Current package version: **0.1.2 — public-ready candidate**.",
        "Current package version: **0.1.2 — Public Preview candidate**.",
    )
    readme = readme.replace(
        "Local marketplace import has been validated. Public release still requires the final clean-session smoke test and repository visibility/publishing steps in `docs/PUBLIC_RELEASE_CHECKLIST.md`.",
        "This repository is prepared from a clean public snapshot with privacy-safe commit identity. Local marketplace import has been validated; the remaining launch gates are the clean-session plugin smoke test, public visibility, tag/release creation and Plugin Directory submission described in `docs/PUBLIC_RELEASE_CHECKLIST.md`.",
    )
    readme_path.write_text(readme, encoding="utf-8")

    changelog_path = root / "CHANGELOG.md"
    changelog_path.write_text(
        changelog_path.read_text(encoding="utf-8").replace(
            "public developer identity set to `akim-kaneyev`;",
            "public developer identity migrated to `akim-kaneyev`;",
        ),
        encoding="utf-8",
    )

    for cache in root.rglob("__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache)
    for pyc in root.rglob("*.pyc"):
        pyc.unlink(missing_ok=True)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: bootstrap_public_snapshot.py <snapshot-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"Snapshot directory not found: {root}", file=sys.stderr)
        return 2
    transform(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
