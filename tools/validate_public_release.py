from __future__ import annotations

import json
import re
import struct
import sys
import zlib
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
    ROOT / "SKILLS.lock.json",
    ROOT / "templates" / "case" / "STATE.md",
    ROOT / "docs" / "ARCHITECTURE.md",
    ROOT / "docs" / "OPEN_SOURCE_INTEGRATIONS.md",
    ROOT / "docs" / "RUNTIME_ACCEPTANCE.md",
    ROOT / "docs" / "SKILL_AUTHORING_STANDARD.md",
    ROOT / "docs" / "TOOLCHAIN_DISCOVERY.md",
    ROOT / "checklists" / "code-artifacts.md",
    ROOT / "checklists" / "sonarqube-bsl.md",
    ROOT / "evals" / "suite.json",
    ROOT / "evals" / "README.md",
    ROOT / "evals" / "result.schema.json",
    ROOT / "evals" / "run.schema.json",
    ROOT / "tests" / "test_evals.py",
    ROOT / "tests" / "test_skill_governance.py",
    ROOT / "tools" / "validate_evals.py",
    ROOT / "tools" / "validate_runtime_run.py",
    ROOT / "tools" / "validate_publication_history.py",
    ROOT / "tools" / "validate_skills.py",
    ROOT / "tools" / "update_skill_lock.py",
    ROOT / "tools" / "unpack_1c_artifact.py",
    MANIFEST,
    MARKETPLACE,
]

REQUIRED_DYNAMIC_SKILLS = {
    "one-c-erp-capability-discovery",
    "one-c-erp-dynamic-plan",
    "one-c-erp-companion-plugins",
    "one-c-erp-evidence-synthesis",
    "one-c-erp-risk-control",
    "one-c-erp-artifact-extraction",
    "one-c-erp-release-difference",
    "one-c-erp-open-source-intake",
    "one-c-erp-local-static-analysis",
}

FORBIDDEN_SUFFIXES = {
    ".dt",
    ".1cd",
    ".bak",
    ".backup",
    ".key",
    ".pem",
    ".pfx",
    ".p12",
    ".jks",
    ".keystore",
    ".kdbx",
}
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:\b(password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret|"
    r"private[_-]?key|sonar[_-]?token)\b|sonar\.(?:token|login))\s*[:=]\s*"
    r"(?:[\"'][^\"'\r\n]{8,}[\"']|[A-Za-z0-9_./+=:-]{16,})"
)
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")
HTTPS_URL = re.compile(r"^https://[^\s]+$")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(errors, f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(errors, f"JSON root must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def parse_pyproject_version(errors: list[str]) -> str | None:
    path = ROOT / "pyproject.toml"
    if not path.exists():
        fail(errors, "Missing pyproject.toml")
        return None
    match = re.search(
        r'^version\s*=\s*"([^"]+)"',
        path.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    if not match:
        fail(errors, "pyproject.toml has no project version")
        return None
    return match.group(1)


def validate_skill(path: Path, errors: list[str]) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(errors, f"Skill has no YAML frontmatter: {path.relative_to(ROOT)}")
        return None
    closing = text.find("\n---\n", 4)
    if closing == -1:
        fail(errors, f"Skill frontmatter is not closed: {path.relative_to(ROOT)}")
        return None
    frontmatter = text[4:closing]
    name_match = re.search(r"(?m)^name:\s*(\S+)", frontmatter)
    description_match = re.search(r"(?m)^description:\s*\S+", frontmatter)
    if not name_match:
        fail(errors, f"Skill frontmatter has no name: {path.relative_to(ROOT)}")
    if not description_match:
        fail(errors, f"Skill frontmatter has no description: {path.relative_to(ROOT)}")
    return name_match.group(1) if name_match else None


def validate_png(path: Path, errors: list[str]) -> None:
    try:
        data = path.read_bytes()
    except OSError as exc:
        fail(errors, f"Cannot read PNG asset {path.relative_to(ROOT)}: {exc}")
        return
    if not data.startswith(PNG_SIGNATURE):
        fail(errors, f"Invalid PNG signature: {path.relative_to(ROOT)}")
        return

    offset = len(PNG_SIGNATURE)
    seen_ihdr = False
    seen_idat = False
    seen_iend = False
    width = height = 0

    while offset < len(data):
        if offset + 12 > len(data):
            fail(errors, f"Truncated PNG chunk header: {path.relative_to(ROOT)}")
            return
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            fail(errors, f"Truncated PNG chunk data: {path.relative_to(ROOT)}")
            return
        chunk_data = data[offset + 8 : offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length : chunk_end])[0]
        calculated_crc = zlib.crc32(chunk_type)
        calculated_crc = zlib.crc32(chunk_data, calculated_crc) & 0xFFFFFFFF
        if stored_crc != calculated_crc:
            label = chunk_type.decode("ascii", errors="replace")
            fail(errors, f"PNG CRC mismatch in {label}: {path.relative_to(ROOT)}")
            return

        if chunk_type == b"IHDR":
            if seen_ihdr or length != 13:
                fail(errors, f"Invalid IHDR chunk: {path.relative_to(ROOT)}")
                return
            seen_ihdr = True
            width, height = struct.unpack(">II", chunk_data[:8])
        elif chunk_type == b"IDAT":
            seen_idat = True
        elif chunk_type == b"IEND":
            if length != 0:
                fail(errors, f"Invalid IEND chunk: {path.relative_to(ROOT)}")
            seen_iend = True
            offset = chunk_end
            break
        offset = chunk_end

    if not (seen_ihdr and seen_idat and seen_iend):
        fail(errors, f"PNG is missing IHDR/IDAT/IEND: {path.relative_to(ROOT)}")
    if width < 64 or height < 64:
        fail(errors, f"PNG is too small ({width}x{height}): {path.relative_to(ROOT)}")
    if offset != len(data):
        fail(errors, f"PNG has trailing bytes after IEND: {path.relative_to(ROOT)}")


def validate_manifest_asset(interface: dict, field: str, errors: list[str]) -> None:
    value = interface.get(field)
    if not isinstance(value, str) or not value.startswith("./"):
        fail(errors, f"Manifest interface.{field} must be a relative ./ path")
        return
    asset = (PLUGIN_DIR / value).resolve()
    try:
        asset.relative_to(PLUGIN_DIR.resolve())
    except ValueError:
        fail(errors, f"Manifest {field} points outside the plugin directory")
        return
    if not asset.is_file():
        fail(errors, f"Manifest {field} asset does not exist: {value}")
        return
    if asset.suffix.lower() == ".png":
        validate_png(asset, errors)


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

    manifest_version = manifest.get("version")
    if not isinstance(manifest_version, str) or not SEMVER.fullmatch(manifest_version):
        fail(errors, "Manifest version must be strict semver")

    project_version = parse_pyproject_version(errors)
    if manifest_version and project_version and manifest_version != project_version:
        fail(errors, f"Version mismatch: plugin={manifest_version}, pyproject={project_version}")

    author = manifest.get("author") or {}
    if not isinstance(author, dict) or not author.get("name"):
        fail(errors, "Manifest author.name is required")
    for field in ("homepage", "repository"):
        value = manifest.get(field)
        if not isinstance(value, str) or not HTTPS_URL.fullmatch(value):
            fail(errors, f"Manifest {field} must be an absolute https:// URL")
    if manifest.get("license") != "MIT":
        fail(errors, "Manifest license must be MIT")
    if manifest.get("skills") != "./skills/":
        fail(errors, 'Manifest skills must be "./skills/"')

    interface = manifest.get("interface") or {}
    if not isinstance(interface, dict):
        fail(errors, "Manifest interface must be an object")
        interface = {}
    for field in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "composerIcon",
        "logo",
        "logoDark",
    ):
        if not interface.get(field):
            fail(errors, f"Manifest interface.{field} is required")
    for field in ("websiteURL", "privacyPolicyURL"):
        value = interface.get(field)
        if not isinstance(value, str) or not HTTPS_URL.fullmatch(value):
            fail(errors, f"Manifest interface.{field} must be an absolute https:// URL")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail(errors, "Manifest defaultPrompt must contain 1 to 3 strings")
    else:
        for index, prompt in enumerate(prompts, start=1):
            if not isinstance(prompt, str) or not prompt.strip():
                fail(errors, f"defaultPrompt[{index}] must be non-empty text")
            elif len(prompt) > 128:
                fail(errors, f"defaultPrompt[{index}] exceeds 128 characters")

    for field in ("composerIcon", "logo", "logoDark"):
        validate_manifest_asset(interface, field, errors)

    plugins = marketplace.get("plugins") if isinstance(marketplace, dict) else None
    if not isinstance(plugins, list) or not any(
        isinstance(item, dict) and item.get("name") == expected_name for item in plugins
    ):
        fail(errors, "Marketplace does not declare one-c-erp-diagnostics")

    skill_paths = sorted((PLUGIN_DIR / "skills").glob("*/SKILL.md"))
    skill_names = {name for path in skill_paths if (name := validate_skill(path, errors))}
    if len(skill_paths) < 32:
        fail(errors, f"Expected at least 32 packaged skills, found {len(skill_paths)}")
    missing_dynamic = sorted(REQUIRED_DYNAMIC_SKILLS - skill_names)
    if missing_dynamic:
        fail(errors, "Missing dynamic skills: " + ", ".join(missing_dynamic))

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
        lower_name = path.name.lower()
        if lower_name == ".env" or lower_name.startswith(".env."):
            fail(errors, f"Forbidden environment file tracked: {path.relative_to(ROOT)}")
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SECRET_ASSIGNMENT.search(text):
            fail(errors, f"Possible plaintext credential assignment: {path.relative_to(ROOT)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    for required_text in (
        "@one-c-erp-diagnostics",
        "$one-c-erp-diagnostics",
        "Gate 0–10",
        "Dynamic orchestration",
        "Optional companion",
        "Not affiliated",
        "sonarqube-bsl-local",
    ):
        if required_text not in readme:
            fail(errors, f"README is missing required public text: {required_text}")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    if ".scannerwork/" not in gitignore:
        fail(errors, ".gitignore must exclude SonarScanner .scannerwork directories")

    if errors:
        print("PUBLIC RELEASE VALIDATION: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("PUBLIC RELEASE VALIDATION: PASS")
    print(f"Packaged skills: {len(skill_paths)}")
    print(f"Plugin version: {manifest_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
