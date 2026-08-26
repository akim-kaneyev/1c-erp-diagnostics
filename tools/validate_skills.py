#!/usr/bin/env python3
"""Validate packaged skills, routing boundaries, local links and lock consistency."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
PACKAGED_SKILLS = Path("plugins/one-c-erp-diagnostics/skills")
RECOMMENDED_HEADINGS = (
    "## When to use",
    "## When NOT to use",
    "## Required inputs",
    "## The framework",
    "## Workflow",
    "## Failure patterns",
    "## Output format",
    "## Reference files",
)
AUTHORITATIVE_SURFACES = (
    Path("SKILL.md"),
    Path("plugins/one-c-erp-diagnostics/skills/one-c-erp-diagnostics/SKILL.md"),
    Path("skills/one-c-erp-diagnostics/SKILL.md"),
)
AUTHORITATIVE_TOKENS = (
    "Gate 0",
    "Gate 10",
    "Gate 7",
    "EVAL_RESULT_JSON",
    "pending | passed | blocked | failed | stale | not_required",
    "R0",
    "R3",
)
REPOSITORY_SHIM = Path(".agents/skills/one-c-erp-diagnostics/SKILL.md")
REPOSITORY_SHIM_TOKENS = (
    "SKILL.md",
    "STATE.md",
    "unica",
    "1c-skills",
    "1c-skills-py",
    "blocked",
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    skill_count: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0] in {'"', "'"}:
        try:
            parsed = ast.literal_eval(value)
            return str(parsed)
        except (SyntaxError, ValueError):
            return value.strip('"\'')
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing or malformed YAML frontmatter")
    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#") or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        if key and not key.startswith((" ", "\t")):
            fields[key.strip()] = parse_scalar(value)
    return fields, text[match.end() :]


def _is_external_link(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "plugin://", "chatgpt-", "data:"))


def validate_local_links(path: Path, root: Path, report: ValidationReport) -> None:
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith("#") or _is_external_link(target):
            continue
        # Markdown permits an optional quoted title after the URL. Paths that
        # contain spaces should be percent-encoded or wrapped in angle brackets.
        target = target.split(maxsplit=1)[0]
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        candidate = (path.parent / target).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            report.fail(f"Local link escapes repository root: {path.relative_to(root)} -> {raw_target}")
            continue
        if not candidate.exists():
            report.fail(f"Broken local link: {path.relative_to(root)} -> {raw_target}")


def validate_skill_inventory(root: Path, report: ValidationReport) -> None:
    directory = root / PACKAGED_SKILLS
    if not directory.is_dir():
        report.fail(f"Missing packaged skills directory: {PACKAGED_SKILLS}")
        return

    skill_dirs = sorted(path for path in directory.iterdir() if path.is_dir())
    report.skill_count = len(skill_dirs)
    if len(skill_dirs) < 32:
        report.fail(f"Expected at least 32 packaged skills, found {len(skill_dirs)}")

    names: dict[str, Path] = {}
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        relative_dir = skill_dir.relative_to(root)
        folder_name = skill_dir.name
        if not folder_name.startswith("one-c-erp-"):
            report.fail(f"Foreign or unscoped packaged skill namespace: {relative_dir}")
        if not skill_md.is_file():
            report.fail(f"Packaged skill directory has no SKILL.md: {relative_dir}")
            continue

        relative = skill_md.relative_to(root)
        try:
            fields, body = parse_frontmatter(skill_md)
        except ValueError as exc:
            report.fail(f"{relative}: {exc}")
            continue

        name = fields.get("name", "")
        description = fields.get("description", "")
        if not name:
            report.fail(f"{relative}: frontmatter name is required")
        else:
            if name != folder_name:
                report.fail(f"{relative}: name {name!r} does not match folder {folder_name!r}")
            if name in names:
                report.fail(f"Duplicate packaged skill name {name!r}: {names[name].relative_to(root)} and {relative}")
            else:
                names[name] = skill_md
        if not description:
            report.fail(f"{relative}: frontmatter description is required")
        elif len(description) < 40:
            report.warn(f"short_description: {relative}")

        line_count = len(skill_md.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            report.fail(f"{relative}: SKILL.md exceeds 500 lines ({line_count})")
        elif line_count > 400:
            report.warn(f"large_skill: {relative} ({line_count} lines)")

        for heading in RECOMMENDED_HEADINGS:
            if heading not in body:
                report.warn(f"missing_heading:{heading}: {relative}")

        # Validate the owning SKILL.md and every Markdown reference shipped
        # beside it, so moving depth into references cannot bypass link checks.
        for markdown in sorted(skill_dir.rglob("*.md")):
            validate_local_links(markdown, root, report)


def validate_surface_sync(root: Path, report: ValidationReport) -> None:
    for relative in AUTHORITATIVE_SURFACES:
        path = root / relative
        if not path.is_file():
            report.fail(f"Missing synchronized runtime surface: {relative.as_posix()}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in AUTHORITATIVE_TOKENS:
            if token not in text:
                report.fail(f"Runtime surface {relative.as_posix()} is missing invariant: {token}")
        validate_local_links(path, root, report)

    shim = root / REPOSITORY_SHIM
    if not shim.is_file():
        report.fail(f"Missing repository skill shim: {REPOSITORY_SHIM.as_posix()}")
    else:
        text = shim.read_text(encoding="utf-8")
        for token in REPOSITORY_SHIM_TOKENS:
            if token not in text:
                report.fail(f"Repository skill shim is missing routing invariant: {token}")
        validate_local_links(shim, root, report)


def validate_external_boundaries(root: Path, report: ValidationReport) -> None:
    marketplace = root / ".agents/plugins/marketplace.json"
    if not marketplace.is_file():
        report.fail("Missing ecosystem marketplace")
        return
    text = marketplace.read_text(encoding="utf-8").lower()
    for forbidden in ("rampstack", "oxotka", "stacktechnologies1c"):
        if forbidden in text:
            report.fail(f"Discovery/methodology source must not be bundled in marketplace: {forbidden}")


def _load_lock_module(root: Path):
    path = root / "tools/update_skill_lock.py"
    spec = importlib.util.spec_from_file_location("update_skill_lock", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load tools/update_skill_lock.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_repository(root: Path, *, check_lock: bool = True) -> ValidationReport:
    root = root.resolve()
    report = ValidationReport()
    validate_skill_inventory(root, report)
    validate_surface_sync(root, report)
    validate_external_boundaries(root, report)
    if check_lock:
        try:
            module = _load_lock_module(root)
            report.errors.extend(module.check_lock(root, root / "SKILLS.lock.json"))
        except Exception as exc:  # noqa: BLE001 - validation must report loader failures
            report.fail(f"Cannot validate skill lock: {exc}")
    return report


def summarize_warnings(warnings: list[str]) -> list[str]:
    counts: Counter[str] = Counter()
    for warning in warnings:
        category = warning.split(":", 1)[0]
        counts[category] += 1
    return [f"{category}: {count}" for category, count in sorted(counts.items())]


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--skip-lock", action="store_true", help="Bootstrap only: skip tracked lock validation")
    parser.add_argument("--show-warnings", action="store_true", help="Print every advisory warning")
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    report = validate_repository(args.root, check_lock=not args.skip_lock)
    print(f"Packaged skills: {report.skill_count}")
    if args.show_warnings or args.warnings_as_errors:
        for warning in report.warnings:
            print(f"WARNING: {warning}")
    else:
        for summary in summarize_warnings(report.warnings):
            print(f"WARNING SUMMARY: {summary}")
    if report.errors or (args.warnings_as_errors and report.warnings):
        print("SKILL GOVERNANCE VALIDATION: FAIL", file=sys.stderr)
        for error in report.errors:
            print(f"- {error}", file=sys.stderr)
        if args.warnings_as_errors:
            for warning in report.warnings:
                print(f"- warning promoted to error: {warning}", file=sys.stderr)
        return 1
    print("SKILL GOVERNANCE VALIDATION: PASS")
    print(f"Advisory warnings: {len(report.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
