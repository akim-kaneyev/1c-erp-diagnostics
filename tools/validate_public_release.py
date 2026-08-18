from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "one-c-erp-diagnostics"
MANIFEST = PLUGIN_DIR / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "PRIVACY.md",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    ROOT / "NOTICE.md",
    ROOT / "CHANGELOG.md",
    ROOT / "AGENTS.md",
    ROOT / "SKILL.md",
    ROOT / "templates" / "case" / "STATE.md",
    MANIFEST,
    MARKETPLACE,
]

FORBIDDEN_SUFFIXES = {
    ".dt",
    ".1cd",
    ".bak",
    ".backup",
    ".key",
    ".pem",
}

SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)\b"
    r"\s*[:=]\s*[\"'][^\"']{8,}[\"']"
)

TEXT_SUFFIXES_FOR_SECRET_CHECK = {
    ".py",
    ".json",
    ".toml",
    ".yml",
    ".yaml",
    ".sh",
    ".ps1",
    ".env",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validator must report malformed files
        fail(errors, f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
        return {}


def parse_pyproject_version(errors: list[str]) -> str | None:
    path = ROOT / "pyproject.toml"
    if not path.exists():
        fail(errors, "Missing pyproject.toml")
        return None

    text = path.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, flags=re.MULTILINE)
    if not match:
        fail(errors, "pyproject.toml has no project version")
        return None
    return match.group(1)


def validate_skill(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(errors, f"Skill has no YAML frontmatter: {path.relative_to(ROOT)}")
        return

    closing = text.find("\n---\n", 4)
    if closing == -1:
        fail(errors, f"Skill frontmatter is not closed: {path.relative_to(ROOT)}")
        return

    frontmatter = text[4:closing]
    if not re.search(r"(?m)^name:\s*\S+", frontmatter):
        fail(errors, f"Skill frontmatter has no name: {path.relative_to(ROOT)}")
    if not re.search(r"(?m)^description:\s*\S+", frontmatter):
        fail(errors, f"Skill frontmatter has no description: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            fail(errors, f"Missing required file: {path.relative_to(ROOT)}")

    manifest = load_json(MANIFEST, errors) if MANIFEST.exists() else {}
    marketplace = load_json(MARKETPLACE, errors) if MARKETPLACE.exists() else {}

    expected_name = "one-c-erp-diagnostics"
    if manifest.get("name") != expected_name:
        fail(errors, f"Manifest name must be {expected_name!r}")

    interface = manifest.get("interface") or {}
    for field in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "composerIcon",
        "logo",
    ):
        if not interface.get(field):
            fail(errors, f"Manifest interface.{field} is required")

    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        if value:
            asset = (PLUGIN_DIR / value).resolve()
            try:
                asset.relative_to(PLUGIN_DIR.resolve())
            except ValueError:
                fail(errors, f"Manifest {field} points outside the plugin directory")
            else:
                if not asset.is_file():
                    fail(errors, f"Manifest {field} asset does not exist: {value}")

    manifest_version = manifest.get("version")
    project_version = parse_pyproject_version(errors)
    if manifest_version and project_version and manifest_version != project_version:
        fail(
            errors,
            f"Version mismatch: plugin={manifest_version}, pyproject={project_version}",
        )

    plugins = marketplace.get("plugins") if isinstance(marketplace, dict) else None
    if not isinstance(plugins, list) or not any(
        isinstance(item, dict) and item.get("name") == expected_name for item in plugins
    ):
        fail(errors, "Marketplace does not declare one-c-erp-diagnostics")

    skills = sorted((PLUGIN_DIR / "skills").glob("*/SKILL.md"))
    if len(skills) < 10:
        fail(errors, f"Expected at least 10 packaged skills, found {len(skills)}")
    for skill in skills:
        validate_skill(skill, errors)

    case_files = [
        path
        for path in (ROOT / "cases").rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    if case_files:
        fail(
            errors,
            "Public candidate contains case files: "
            + ", ".join(str(path.relative_to(ROOT)) for path in case_files),
        )

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(errors, f"Forbidden artifact tracked: {path.relative_to(ROOT)}")
        if path.suffix.lower() in TEXT_SUFFIXES_FOR_SECRET_CHECK:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if SECRET_ASSIGNMENT.search(text):
                fail(errors, f"Possible plaintext credential assignment: {path.relative_to(ROOT)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    for required_text in (
        "@one-c-erp-diagnostics",
        "$one-c-erp-diagnostics",
        "Gate 1–10",
        "Not affiliated",
    ):
        if required_text not in readme:
            fail(errors, f"README is missing required public text: {required_text}")

    if errors:
        print("PUBLIC RELEASE VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("PUBLIC RELEASE VALIDATION: PASS")
    print(f"Packaged skills: {len(skills)}")
    print(f"Plugin version: {manifest_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
