from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "one-c-erp-diagnostics"
PLUGIN_VERSION = "0.3.7"


def load_artifact_module():
    path = ROOT / "tools" / "unpack_1c_artifact.py"
    spec = importlib.util.spec_from_file_location("unpack_1c_artifact", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load artifact extraction module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_public_release_module():
    path = ROOT / "tools" / "validate_public_release.py"
    spec = importlib.util.spec_from_file_location("validate_public_release", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load public release validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DynamicContractTests(unittest.TestCase):
    def test_manifest_and_project_versions_match(self) -> None:
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertEqual(manifest["version"], PLUGIN_VERSION)
        self.assertIn(f'version = "{PLUGIN_VERSION}"', pyproject)
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
        self.assertIn("No decorated/noncanonical Gate statuses", root_skill)
        self.assertIn("Current goal status", final_review)
        self.assertIn("Linked incident status", final_review)
        self.assertIn("Current goal status:", state)
        self.assertIn("Linked incident status:", state)
        self.assertIn("not_required", packaged)
        self.assertIn("Never use `passed*`", packaged)
        self.assertIn("evidence-sufficiency", root_skill)
        self.assertIn("Current goal: closed; linked incident: blocked", final_review)

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
            "one-c-erp-local-static-analysis",
        }
        actual = {
            path.parent.name
            for path in (PLUGIN / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(len(actual), 32)
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

    def test_secret_assignment_detection_covers_quoted_and_unquoted_values(self) -> None:
        module = load_public_release_module()
        quoted = "api_" + 'key = "' + "abcdefghijklmnop" + '"'
        unquoted = "access-" + "token: " + "abcdefghijklmnop"
        sonar_env = "SONAR_" + "TOKEN=" + "abcdefghijklmnop"
        sonar_property = "sonar." + "token: " + "abcdefghijklmnop"
        legacy_property = "sonar." + "login=" + "abcdefghijklmnop"
        self.assertIsNotNone(module.SECRET_ASSIGNMENT.search(quoted))
        self.assertIsNotNone(module.SECRET_ASSIGNMENT.search(unquoted))
        self.assertIsNotNone(module.SECRET_ASSIGNMENT.search(sonar_env))
        self.assertIsNotNone(module.SECRET_ASSIGNMENT.search(sonar_property))
        self.assertIsNotNone(module.SECRET_ASSIGNMENT.search(legacy_property))
        self.assertIsNone(module.SECRET_ASSIGNMENT.search("secret scanning is enabled"))
        self.assertIsNone(module.SECRET_ASSIGNMENT.search("Use SONAR_TOKEN only in child process environment"))

    def test_local_static_analysis_contract_is_safe_and_non_causal(self) -> None:
        skill = (
            PLUGIN
            / "skills"
            / "one-c-erp-local-static-analysis"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        packaged = (
            PLUGIN / "skills" / "one-c-erp-diagnostics" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for required in (
            "sonarqube-bsl-local",
            "http://127.0.0.1:9000",
            "communitybsl",
            "SONAR_TOKEN",
            "R1",
            "R2",
            "R3",
            "report-task.txt",
            "sonar.qualitygate.timeout",
            "project analysis token",
            "reason",
            "complete=false",
            "hypothesis",
            "Gate 7",
            "dedicated SonarQube MCP server",
            "host_execution_confirmation_required",
            "actual read-only probes",
        ):
            self.assertIn(required, skill)
        self.assertIn("one-c-erp-local-static-analysis", root_skill)
        self.assertIn("one-c-erp-local-static-analysis", packaged)
        self.assertIn("SonarQube remains a host execution adapter", packaged)

    def test_harness_hardening_contracts_are_explicit(self) -> None:
        evidence = (
            PLUGIN / "skills" / "one-c-erp-evidence-intake" / "SKILL.md"
        ).read_text(encoding="utf-8")
        plan = (
            PLUGIN / "skills" / "one-c-erp-dynamic-plan" / "SKILL.md"
        ).read_text(encoding="utf-8")
        verify = (
            PLUGIN / "skills" / "one-c-erp-verify-conclusion" / "SKILL.md"
        ).read_text(encoding="utf-8")
        post = (
            PLUGIN / "skills" / "one-c-erp-post-change-validation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        state = (ROOT / "templates" / "case" / "STATE.md").read_text(
            encoding="utf-8"
        )
        architecture = (ROOT / "docs" / "ARCHITECTURE.md").read_text(
            encoding="utf-8"
        )
        methodology = (ROOT / "docs" / "upstream-methodology.md").read_text(
            encoding="utf-8"
        )

        for disposition in (
            "examined",
            "unreadable",
            "duplicate",
            "irrelevant_with_reason",
            "blocked",
        ):
            self.assertIn(disposition, evidence)
        self.assertIn("supplied-but-unexamined evidence", evidence)
        self.assertIn("expected-but-missing evidence", evidence)
        self.assertIn("Independent validation contract", plan)
        self.assertIn("business_accounting", plan)
        self.assertIn("A review label such as `critical`", verify)
        self.assertIn("Validation ladder", post)
        self.assertIn("Passing a lower validation level never substitutes", post)
        self.assertIn("## Evidence coverage", state)
        self.assertIn("## Independent verification plan", state)
        self.assertIn("## Escaped/missed finding feedback", state)
        self.assertIn("## Model/provider neutrality", architecture)
        self.assertIn("Regression feedback loop", architecture)
        self.assertIn("Earendil — What is a Harness?", methodology)
        self.assertIn("Infostart — seven-agent 1C delivery pipeline", methodology)

    def test_provenance_and_execution_identity_contracts_are_explicit(self) -> None:
        evidence_model = (ROOT / "docs" / "evidence-model.md").read_text(encoding="utf-8")
        intake = (PLUGIN / "skills" / "one-c-erp-evidence-intake" / "SKILL.md").read_text(encoding="utf-8")
        synthesis = (PLUGIN / "skills" / "one-c-erp-evidence-synthesis" / "SKILL.md").read_text(encoding="utf-8")
        sandbox = (PLUGIN / "skills" / "one-c-erp-sandbox-execution" / "SKILL.md").read_text(encoding="utf-8")
        verify = (PLUGIN / "skills" / "one-c-erp-verify-conclusion" / "SKILL.md").read_text(encoding="utf-8")
        state = (ROOT / "templates" / "case" / "STATE.md").read_text(encoding="utf-8")

        for token in ("derived_from", "run_id", "input_hashes", "output_hash", "Provenance closure"):
            self.assertIn(token, evidence_model)
        self.assertIn("Artifact-anchor and derivation contract", intake)
        self.assertIn("Provenance closure contract", synthesis)
        self.assertIn("Execution identity contract", sandbox)
        self.assertIn("mismatched execution identity", verify)
        self.assertIn("## Execution records", state)
        self.assertIn("Provenance closure", state)
        self.assertIn("directly evidenced limitation", synthesis)

    def test_strict_eval_result_contract_is_explicit(self) -> None:
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        packaged = (PLUGIN / "skills" / "one-c-erp-diagnostics" / "SKILL.md").read_text(encoding="utf-8")
        portable = (ROOT / "skills" / "one-c-erp-diagnostics" / "SKILL.md").read_text(encoding="utf-8")
        final_review = (PLUGIN / "skills" / "one-c-erp-final-review" / "SKILL.md").read_text(encoding="utf-8")
        risk_control = (PLUGIN / "skills" / "one-c-erp-risk-control" / "SKILL.md").read_text(encoding="utf-8")
        action_decision = (PLUGIN / "skills" / "one-c-erp-action-decision" / "SKILL.md").read_text(encoding="utf-8")
        capability_discovery = (PLUGIN / "skills" / "one-c-erp-capability-discovery" / "SKILL.md").read_text(encoding="utf-8")

        for skill in (root_skill, packaged, portable, final_review):
            self.assertIn("EVAL_RESULT_JSON", skill)
            self.assertIn("causal_chain.complete", skill)
            self.assertIn("EVIDENCE_REQUIRED", skill)
            self.assertIn("actions", skill)
        for skill in (root_skill, packaged, portable):
            self.assertIn("{id, status, text, evidence_ids, falsifier}", skill)
            self.assertIn("read-only", skill)
            self.assertIn("R0", skill)
            self.assertIn("NO-GO", skill)
            self.assertIn("capabilities: []", skill)
        self.assertIn("exactly one JSON object", root_skill)
        self.assertIn("exactly one JSON object", final_review)
        self.assertIn("Risk classifies the blast radius", risk_control)
        self.assertIn("R0 + EVIDENCE_REQUIRED", action_decision)
        self.assertIn("not_in_scope", final_review)
        self.assertIn("synthetic case capability snapshot", capability_discovery)
        self.assertIn("Internal reasoning steps", capability_discovery)

    def test_capability_inventory_contract_is_explicit(self) -> None:
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        packaged = (PLUGIN / "skills" / "one-c-erp-diagnostics" / "SKILL.md").read_text(encoding="utf-8")
        portable = (ROOT / "skills" / "one-c-erp-diagnostics" / "SKILL.md").read_text(encoding="utf-8")
        final_review = (PLUGIN / "skills" / "one-c-erp-final-review" / "SKILL.md").read_text(encoding="utf-8")
        capability = (PLUGIN / "skills" / "one-c-erp-capability-discovery" / "SKILL.md").read_text(encoding="utf-8")
        combined = "\n".join((root_skill, packaged, portable, final_review, capability))

        for required in (
            "capability-inventory",
            "final_status = ТРЕБУЕТ ПРОВЕРКИ",
            "Gate 0",
            "Gate 10",
            "claims: []",
            "simulated",
            "evidence_id",
            "evidence_ids_used",
        ):
            self.assertIn(required, combined)
        self.assertIn("{name, status, simulated}", root_skill)
        self.assertIn("{name, status, simulated}", packaged)
        self.assertIn("{name, status, simulated}", capability)
        self.assertIn("Gate 10 cannot be `not_required`", final_review)
        self.assertIn("complete causal chain", portable)

    def test_visual_explanation_is_a_post_verification_presentation_sidecar(self) -> None:
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        packaged = (
            PLUGIN / "skills" / "one-c-erp-diagnostics" / "SKILL.md"
        ).read_text(encoding="utf-8")
        portable = (
            ROOT / "skills" / "one-c-erp-diagnostics" / "SKILL.md"
        ).read_text(encoding="utf-8")
        final_review = (
            PLUGIN / "skills" / "one-c-erp-final-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        capability = (
            PLUGIN / "skills" / "one-c-erp-capability-discovery" / "SKILL.md"
        ).read_text(encoding="utf-8")
        architecture = (ROOT / "docs" / "ARCHITECTURE.md").read_text(
            encoding="utf-8"
        )
        evidence_model = (ROOT / "docs" / "evidence-model.md").read_text(
            encoding="utf-8"
        )

        for surface in (root_skill, packaged, portable, final_review):
            for token in (
                "Visual Explanation",
                "`diagram`",
                "`sticky`",
                "Gate 6",
                "Gate 7",
                "Presentation only — not evidence",
                "EVAL_RESULT_JSON",
            ):
                self.assertIn(token, surface)
            self.assertIn(
                "Supported modes are exactly `diagram` and `sticky`; no third mode is allowed.",
                surface,
            )
            self.assertIn(
                "Prerequisite: Gate 6 is passed and Gate 7 is passed.",
                surface,
            )

        for surface in (root_skill, packaged, portable):
            self.assertIn("runtime capability", surface)
            self.assertIn("Evidence ID", surface)
            self.assertIn("provenance closure", surface)

        self.assertIn("not runtime capabilities", capability)
        self.assertIn("never appear in Gate 0", architecture)
        self.assertIn("receives no Evidence ID", architecture)
        self.assertIn("не получает Evidence ID", evidence_model)

        quickstart = (ROOT / "docs" / "QUICKSTART.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("C-2 [ТРЕБУЕТ ПРОВЕРКИ; E-GAP-1]", quickstart)
        self.assertIn("C-3 [ТРЕБУЕТ ПРОВЕРКИ; E-GAP-2]", quickstart)
        self.assertNotIn("record/register → consuming mechanism", quickstart)
        self.assertNotIn("[NEXT]", quickstart)
        self.assertEqual(
            len(list((PLUGIN / "skills").glob("*/SKILL.md"))),
            32,
        )


if __name__ == "__main__":
    unittest.main()
