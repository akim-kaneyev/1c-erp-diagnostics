from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


LOCK = load_module("update_skill_lock", "tools/update_skill_lock.py")
VALIDATE = load_module("validate_skills", "tools/validate_skills.py")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def skill_text(name: str, body: str = "") -> str:
    return (
        "---\n"
        f"name: {name}\n"
        "description: A sufficiently explicit description for deterministic governance tests.\n"
        "---\n\n"
        f"# {name}\n\n{body}\n"
    )


class SkillGovernanceTests(unittest.TestCase):
    def test_current_repository_governance_and_lock_pass(self) -> None:
        report = VALIDATE.validate_repository(ROOT)
        self.assertEqual(report.errors, [])
        self.assertGreaterEqual(report.skill_count, 32)

        expected = LOCK.build_lock(ROOT)
        actual = LOCK.load_lock(ROOT / "SKILLS.lock.json")
        self.assertEqual(actual, expected)
        self.assertEqual(actual["file_count"], 52)
        self.assertEqual(
            actual["manifest_sha256"],
            "55b1b4c843f181f8674b130afecb38601f8251619051956434dc536f1536053e",
        )

    def test_reviewed_sources_and_boundaries_are_recorded(self) -> None:
        authoring = (ROOT / "docs" / "SKILL_AUTHORING_STANDARD.md").read_text(encoding="utf-8")
        discovery = (ROOT / "docs" / "TOOLCHAIN_DISCOVERY.md").read_text(encoding="utf-8")
        integrations = (ROOT / "docs" / "OPEN_SOURCE_INTEGRATIONS.md").read_text(encoding="utf-8")
        notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        combined = "\n".join((authoring, discovery, integrations, notice))

        for token in (
            "0479242522549dfdb389bb9b7807ad4d6016ffb7",
            "82a7b4c16f0dab0264ddd664b741019ce60aba81",
            "https://infostart.ru/1c/articles/2772307/",
            "not copied",
            "not bundled",
            "R0–R3",
        ):
            self.assertIn(token, combined)

        marketplace = (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8").lower()
        self.assertNotIn("rampstack", marketplace)
        self.assertNotIn("stacktechnologies1c", marketplace)

    def test_lock_is_deterministic_and_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "SKILL.md", "root\n")
            write(root / "AGENTS.md", "agents\n")
            write(root / "plugins/one-c-erp-diagnostics/skills/one-c-erp-demo/SKILL.md", skill_text("one-c-erp-demo"))
            first = LOCK.build_lock(root)
            second = LOCK.build_lock(root)
            self.assertEqual(first, second)
            lock_path = root / "SKILLS.lock.json"
            lock_path.write_text(LOCK.serialize_lock(first), encoding="utf-8")
            self.assertEqual(LOCK.check_lock(root, lock_path), [])
            write(root / "plugins/one-c-erp-diagnostics/skills/one-c-erp-demo/SKILL.md", skill_text("one-c-erp-demo", "changed"))
            errors = LOCK.check_lock(root, lock_path)
            self.assertTrue(any("Skill lock drift" in item for item in errors))

    def test_duplicate_skill_name_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / "plugins/one-c-erp-diagnostics/skills"
            write(base / "one-c-erp-a/SKILL.md", skill_text("one-c-erp-a"))
            write(base / "one-c-erp-b/SKILL.md", skill_text("one-c-erp-a"))
            report = VALIDATE.ValidationReport()
            VALIDATE.validate_skill_inventory(root, report)
            self.assertTrue(any("does not match folder" in item or "Duplicate" in item for item in report.errors))

    def test_broken_local_link_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "plugins/one-c-erp-diagnostics/skills/one-c-erp-a/SKILL.md"
            write(path, skill_text("one-c-erp-a", "[missing](references/nope.md)"))
            report = VALIDATE.ValidationReport()
            VALIDATE.validate_local_links(path, root, report)
            self.assertTrue(any("Broken local link" in item for item in report.errors))

    def test_discovery_sources_cannot_enter_marketplace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / ".agents/plugins/marketplace.json", json.dumps({"plugins": [{"name": "rampstack"}]}))
            report = VALIDATE.ValidationReport()
            VALIDATE.validate_external_boundaries(root, report)
            self.assertTrue(any("must not be bundled" in item for item in report.errors))


if __name__ == "__main__":
    unittest.main()
