from __future__ import annotations

import importlib.util
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
    PLUGIN_DIR / "skills" / "one-c-erp-case-state" / "assets" / "STATE.json",
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
    PLUGIN_DIR / "skills" / "one-c-erp-artifact-extraction" / "scripts" / "unpack_1c_artifact.py",
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
    ".ppk",
    ".jks",
    ".keystore",
    ".kdbx",
    ".xlsx",
    ".xlsm",
    ".xltx",
    ".xltm",
    ".xls",
    ".docx",
    ".docm",
    ".doc",
    ".pptx",
    ".pptm",
    ".ppt",
    ".zip",
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
PYTHON_CACHE_NAME = re.compile(
    r"^(?P<stem>.+)\.(?:cpython|pypy)-\d+(?:\.[^.]+)?\.py[co]$"
)
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")
HTTPS_URL = re.compile(r"^https://[^\s]+$")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


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


def safe_path_label(value: str) -> str:
    has_secret, has_machine_path = text_findings(value)
    return "[REDACTED_PATH]" if has_secret or has_machine_path else value


def is_root_case_path(path: str) -> bool:
    parts = [part for part in path.replace("\\", "/").split("/") if part]
    return (
        len(parts) >= 2
        and parts[0].casefold() == "cases"
        and parts[-1].casefold() != ".gitkeep"
    )


def is_forbidden_container(payload: bytes) -> bool:
    return any(signature in payload for signature in FORBIDDEN_CONTAINER_SIGNATURES)


def is_verified_generated_python_cache(path: Path) -> bool:
    if path.parent.name != "__pycache__":
        return False
    match = PYTHON_CACHE_NAME.fullmatch(path.name)
    if match is None:
        return False
    source = path.parent.parent / f"{match.group('stem')}.py"
    if not source.is_file():
        return False
    try:
        header = path.read_bytes()[: len(importlib.util.MAGIC_NUMBER)]
    except OSError:
        return False
    return header == importlib.util.MAGIC_NUMBER


def content_findings(payload: bytes) -> tuple[bool, bool]:
    has_secret = False
    has_machine_path = False
    for encoding in ("utf-8", "utf-16-le", "utf-16-be", "utf-32-le", "utf-32-be"):
        text = payload.decode(encoding, errors="ignore")
        found_secret, found_path = text_findings(text)
        has_secret = has_secret or found_secret
        has_machine_path = has_machine_path or found_path
    return has_secret, has_machine_path


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
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and is_root_case_path(str(path.relative_to(ROOT)))
    ]
    if case_files:
        fail(
            errors,
            "Public candidate contains case files: "
            + ", ".join(
                safe_path_label(str(path.relative_to(ROOT))) for path in case_files
            ),
        )

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if is_verified_generated_python_cache(path):
            continue
        relative_path = str(path.relative_to(ROOT))
        safe_relative_path = safe_path_label(relative_path)
        path_secret, path_machine = text_findings(relative_path)
        if path_secret:
            fail(errors, f"Credential-like tracked path: {safe_relative_path}")
        if path_machine:
            fail(errors, f"User-machine tracked path: {safe_relative_path}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(errors, f"Forbidden artifact tracked: {safe_relative_path}")
        lower_name = path.name.lower()
        if lower_name == ".env" or lower_name.startswith(".env."):
            fail(errors, f"Forbidden environment file tracked: {safe_relative_path}")
        try:
            payload = path.read_bytes()
        except OSError:
            continue
        if is_forbidden_container(payload):
            fail(errors, f"Nested ZIP/Office container is forbidden: {safe_relative_path}")
        has_secret, has_machine_path = content_findings(payload)
        if has_secret:
            fail(errors, f"Possible plaintext credential assignment: {safe_relative_path}")
        if has_machine_path:
            fail(errors, f"Absolute user-machine path: {safe_relative_path}")

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
