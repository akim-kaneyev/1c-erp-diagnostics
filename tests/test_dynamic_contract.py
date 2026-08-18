from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "one-c-erp-diagnostics"


def load_artifact_module():
    path = ROOT / "tools" / "unpack_1c_artifact.py"
    spec = importlib.util.spec_from_file_location("unpack_1c_artifact", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load artifact extraction module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DynamicContractTests(unittest.TestCase):
    def test_manifest_and_project_versions_match(self) -> None:
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertEqual(manifest["version"], "0.2.1")
        self.assertIn('version = "0.2.1"', pyproject)
        self.assertIn('v8unpack==1.2.6', pyproject)
        self.assertIn('opensandbox==0.1.14', pyproject)
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertIn("logoDark", manifest["interface"])
        self.assertEqual(
            manifest["interface"]["termsOfServiceURL"],
            "https://github.com/akim-kaneyev/1c-erp-diagnostics/blob/main/TERMS.md",
        )

    def test_master_contract_contains_dynamic_and_risk_gates(self) -> None:
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        packaged = (
            PLUGIN / "skills" / "one-c-erp-diagnostics" / "SKILL.md"
        ).read_text(encoding="utf-8")
        combined = root_skill + "\n" + packaged
        for required in (
            "Gate 0",
            "Gate 10",
            "capability",
            "Unica",
            "1C Skills",
            "R0",
            "R3",
            "adversarial",
        ):
            self.assertIn(required, combined)

    def test_scoped_closure_contract_is_explicit(self) -> None:
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        packaged = (
            PLUGIN / "skills" / "one-c-erp-diagnostics" / "SKILL.md"
        ).read_text(encoding="utf-8")
        final_review = (
            PLUGIN / "skills" / "one-c-erp-final-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        state = (ROOT / "templates" / "case" / "STATE.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("current goal/task scope", root_skill)
        self.assertIn("linked incident scope", root_skill)
        self.assertIn("Do not use decorated statuses such as `passed*`", root_skill)
        self.assertIn("Current goal status", final_review)
        self.assertIn("Linked incident status", final_review)
        self.assertIn("Current goal status:", state)
        self.assertIn("Linked incident status:", state)
        self.assertIn("not_required", packaged)
        self.assertIn("Never use `passed*`", packaged)

    def test_required_dynamic_skills_are_packaged(self) -> None:
        required = {
            "one-c-erp-capability-discovery",
            "one-c-erp-dynamic-plan",
            "one-c-erp-companion-plugins",
            "one-c-erp-evidence-synthesis",
            "one-c-erp-risk-control",
            "one-c-erp-artifact-extraction",
            "one-c-erp-release-difference",
            "one-c-erp-open-source-intake",
        }
        actual = {
            path.parent.name
            for path in (PLUGIN / "skills").glob("*/SKILL.md")
        }
        self.assertTrue(required.issubset(actual))

    def test_artifact_adapter_rejects_unsupported_and_nonempty_output(self) -> None:
        module = load_artifact_module()
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            unsupported = work / "sample.erf"
            unsupported.write_bytes(b"not-an-artifact")
            output = work / "out"
            with self.assertRaises(ValueError):
                module.validate_paths(unsupported, output, False)

            supported = work / "sample.epf"
            supported.write_bytes(b"sanitized-fixture")
            output.mkdir()
            (output / "existing.txt").write_text("occupied", encoding="utf-8")
            with self.assertRaises(ValueError):
                module.validate_paths(supported, output, False)


if __name__ == "__main__":
    unittest.main()
