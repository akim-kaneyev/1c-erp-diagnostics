#!/usr/bin/env python3
"""Validate the pinned multi-plugin marketplace and publication policy files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
MANIFEST = ROOT / "plugins" / "one-c-erp-diagnostics" / ".codex-plugin" / "plugin.json"

MARKETPLACE_ID = "one-c-erp-diagnostics-marketplace"
EXPECTED_VERSION = "0.3.8"
EXPECTED_ORDER = ["one-c-erp-diagnostics", "unica", "1c-skills", "1c-skills-py"]
EXPECTED_SOURCES = {
    "one-c-erp-diagnostics": {"source": "local", "path": "./plugins/one-c-erp-diagnostics"},
    "unica": {
        "source": "git-subdir",
        "url": "https://github.com/IngvarConsulting/unica-marketplace.git",
        "path": "plugins/unica",
        "sha": "aefc880f9bab606a5c55ed11af563b740054a549",
    },
    "1c-skills": {
        "source": "url",
        "url": "https://github.com/Nikolay-Shirokov/cc-1c-skills.git",
        "sha": "8cb7868145281d8e353831512cc1ffa72f1b5c89",
    },
    "1c-skills-py": {
        "source": "url",
        "url": "https://github.com/Nikolay-Shirokov/cc-1c-skills.git",
        "sha": "c1f79f5ac9f31c620b8508f75464f8c42c559ae4",
    },
}
REQUIRED_FILES = [
    ROOT / "TERMS.md",
    ROOT / "docs" / "ECOSYSTEM_MARKETPLACE.md",
    ROOT / "docs" / "OPEN_SOURCE_INTEGRATIONS.md",
    ROOT / "docs" / f"RELEASE_NOTES_v{EXPECTED_VERSION}.md",
    ROOT / "docs" / f"PLUGIN_AUDIT_v{EXPECTED_VERSION}.md",
]
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"Missing required ecosystem/publication file: {path.relative_to(ROOT)}")

    try:
        marketplace = load_json(MARKETPLACE)
    except Exception as exc:
        errors.append(f"Invalid marketplace JSON: {exc}")
        marketplace = {}
    try:
        manifest = load_json(MANIFEST)
    except Exception as exc:
        errors.append(f"Invalid plugin manifest JSON: {exc}")
        manifest = {}

    if marketplace.get("name") != MARKETPLACE_ID:
        errors.append("Unexpected marketplace name; installation identity must remain stable")
    if (marketplace.get("interface") or {}).get("displayName") != "1C ERP Diagnostics Ecosystem":
        errors.append("Unexpected marketplace displayName")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        errors.append("marketplace.plugins must be a list")
        plugins = []
    names = [item.get("name") for item in plugins if isinstance(item, dict)]
    if names != EXPECTED_ORDER:
        errors.append(f"Unexpected plugin order/content: {names!r}")
    if len(names) != len(set(names)):
        errors.append("Duplicate marketplace plugin names")

    by_name = {item.get("name"): item for item in plugins if isinstance(item, dict) and isinstance(item.get("name"), str)}
    for name, expected_source in EXPECTED_SOURCES.items():
        item = by_name.get(name)
        if not item:
            errors.append(f"Missing marketplace plugin: {name}")
            continue
        if item.get("source") != expected_source:
            errors.append(f"Unexpected source for {name}: {item.get('source')!r}")
        policy = item.get("policy") or {}
        if policy.get("installation") != "AVAILABLE":
            errors.append(f"{name} must require explicit installation")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append(f"{name} must declare ON_INSTALL authentication timing")

    for name in ("unica", "1c-skills", "1c-skills-py"):
        source = by_name.get(name, {}).get("source") or {}
        sha = source.get("sha", "")
        if not SHA40.fullmatch(sha):
            errors.append(f"{name} must use an immutable 40-character SHA selector")
        if "ref" in source:
            errors.append(f"{name} must use the verified `sha` field, not `ref`, for a commit pin")

    interface = manifest.get("interface") or {}
    if manifest.get("version") != EXPECTED_VERSION:
        errors.append(f"Plugin manifest version must be {EXPECTED_VERSION}")
    if interface.get("termsOfServiceURL") != "https://github.com/akim-kaneyev/1c-erp-diagnostics/blob/main/TERMS.md":
        errors.append("Manifest termsOfServiceURL is missing or unexpected")
    if "единая экосистема" not in str(interface.get("shortDescription", "")):
        errors.append("Short description does not identify the unified ecosystem")

    if errors:
        print("ECOSYSTEM MARKETPLACE VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ECOSYSTEM MARKETPLACE VALIDATION: PASS")
    print("Marketplace ID: " + MARKETPLACE_ID)
    print("Plugins: " + ", ".join(EXPECTED_ORDER))
    print("Plugin version: " + EXPECTED_VERSION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
