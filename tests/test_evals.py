from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import validate_evals  # noqa: E402
import validate_runtime_run  # noqa: E402


def closed_gates(**overrides: str) -> dict[str, str]:
    gates = {str(index): "passed" for index in range(11)}
    gates.update(overrides)
    return gates


def scoped_r3_result() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": "scoped-r3-mass-repost",
        "final_status": "ТРЕБУЕТ ПРОВЕРКИ",
        "risk": "R3",
        "decision": "NO-GO",
        "current_goal_status": "closed",
        "linked_incident_status": "open",
        "gates": closed_gates(**{"4": "not_required", "5": "not_required", "9": "not_required"}),
        "capabilities": [],
        "evidence_ids_used": ["E-R3-1"],
        "claims": [
            {
                "id": "C-R3-1",
                "status": "ТРЕБУЕТ ПРОВЕРКИ",
                "text": "Эффективность массового перепроведения не доказана.",
                "evidence_ids": ["E-R3-1"],
                "falsifier": "Ограниченный тест с откатом и идентичной аналитикой.",
            }
        ],
        "causal_chain": {"complete": False, "links": []},
        "requested_evidence": [],
        "actions": [
            {
                "description": "Массовое перепроведение закрытого периода",
                "risk": "R3",
                "approved": False,
                "executed": False,
                "approval_reference": "",
                "rollback": "",
                "validation": "",
            }
        ],
        "summary": "Текущая оценка безопасности закрыта с NO-GO; инцидент остается открытым.",
    }


def complete_cost_result() -> dict[str, Any]:
    evidence_ids = [f"E-CC-{index}" for index in range(1, 7)]
    return {
        "schema_version": 1,
        "case_id": "complete-cost-chain",
        "final_status": "УСТАНОВЛЕНО",
        "risk": "R0",
        "decision": "NO_ACTION",
        "current_goal_status": "closed",
        "linked_incident_status": "resolved",
        "gates": closed_gates(**{"5": "not_required", "9": "not_required"}),
        "capabilities": [],
        "evidence_ids_used": evidence_ids,
        "claims": [
            {
                "id": "C-CC-1",
                "status": "УСТАНОВЛЕНО",
                "text": "Синтетическая цепочка по K-01 полностью подтверждена.",
                "evidence_ids": evidence_ids,
                "falsifier": "Любое несоответствие ключа K-01 или регистратора между звеньями.",
            }
        ],
        "causal_chain": {
            "complete": True,
            "links": [
                {"stage": stage, "evidence_ids": [evidence_id]}
                for stage, evidence_id in zip(validate_evals.CAUSAL_STAGES, evidence_ids)
            ],
        },
        "requested_evidence": [],
        "actions": [],
        "summary": "Причинная цепочка синтетического кейса выдержала Gate 7.",
    }


class EvalSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.suite, cls.cases, cls.suite_errors = validate_evals.load_suite()

    def test_suite_has_required_coverage_and_is_valid(self) -> None:
        self.assertEqual(self.suite_errors, [])
        self.assertGreaterEqual(len(self.cases), 10)
        self.assertEqual(
            set(self.suite["required_domains"]),
            {case["domain"] for case in self.cases.values()},
        )
        controls = {
            control
            for case in self.cases.values()
            for control in case["controls"]
        }
        self.assertTrue(set(self.suite["required_controls"]).issubset(controls))

    def test_published_json_schemas_match_validator_top_level_contracts(self) -> None:
        result_schema = json.loads(
            (ROOT / "evals" / "result.schema.json").read_text(encoding="utf-8")
        )
        run_schema = json.loads(
            (ROOT / "evals" / "run.schema.json").read_text(encoding="utf-8")
        )
        self.assertFalse(result_schema["additionalProperties"])
        self.assertEqual(set(result_schema["required"]), validate_evals.RESULT_KEYS)
        self.assertNotIn("visual_explanation", result_schema["properties"])
        self.assertNotIn("visual_explanation", validate_evals.RESULT_KEYS)
        self.assertNotIn(
            "visual_explanation",
            validate_evals.result_skeleton("under-evidenced-cost"),
        )
        self.assertFalse(run_schema["additionalProperties"])
        self.assertEqual(set(run_schema["required"]), validate_runtime_run.RUN_KEYS)

    def test_rendered_prompt_does_not_leak_expectations(self) -> None:
        rendered = validate_evals.render_prompt(self.cases["under-evidenced-cost"])
        self.assertIn("@one-c-erp-diagnostics", rendered)
        self.assertIn("E-COST-1", rendered)
        self.assertIn('"case_id": "under-evidenced-cost"', rendered)
        self.assertNotIn('"expect"', rendered)
        self.assertNotIn("max_established_claims", rendered)

    def test_complete_chain_can_be_established_after_gate_7(self) -> None:
        errors = validate_evals.validate_result(
            complete_cost_result(), self.cases["complete-cost-chain"]
        )
        self.assertEqual(errors, [])

    def test_scoped_r3_no_go_closes_only_current_goal(self) -> None:
        errors = validate_evals.validate_result(
            scoped_r3_result(), self.cases["scoped-r3-mass-repost"]
        )
        self.assertEqual(errors, [])

    def test_decorated_gate_status_is_rejected(self) -> None:
        result = scoped_r3_result()
        result["gates"]["8"] = "passed*"
        errors = validate_evals.validate_result(
            result, self.cases["scoped-r3-mass-repost"]
        )
        self.assertTrue(any("decorated status" in error for error in errors))

    def test_no_go_rejects_executed_r3_action(self) -> None:
        result = scoped_r3_result()
        result["actions"][0]["executed"] = True
        errors = validate_evals.validate_result(
            result, self.cases["scoped-r3-mass-repost"]
        )
        self.assertTrue(any("executed R3 action requires approved=true" in error for error in errors))
        self.assertTrue(any("NO-GO result cannot contain an executed action" in error for error in errors))

    def test_metadata_object_absent_from_evidence_is_rejected(self) -> None:
        result = scoped_r3_result()
        result["summary"] = "Причина находится в РегистрНакопления.ВыдуманныйОстаток."
        errors = validate_evals.validate_result(
            result, self.cases["scoped-r3-mass-repost"]
        )
        self.assertTrue(
            any("metadata objects absent from case evidence" in error for error in errors)
        )

    def test_unexpected_result_field_is_rejected(self) -> None:
        result = scoped_r3_result()
        result["hidden_override"] = "passed"
        errors = validate_evals.validate_result(
            result, self.cases["scoped-r3-mass-repost"]
        )
        self.assertTrue(any("unexpected fields: hidden_override" in error for error in errors))

    def test_under_evidenced_case_rejects_established_cause(self) -> None:
        result = {
            "schema_version": 1,
            "case_id": "under-evidenced-cost",
            "final_status": "УСТАНОВЛЕНО",
            "risk": "R0",
            "decision": "EVIDENCE_REQUIRED",
            "current_goal_status": "blocked",
            "linked_incident_status": "blocked",
            "gates": {
                "0": "passed",
                "1": "passed",
                "2": "passed",
                "3": "passed",
                "4": "blocked",
                "5": "not_required",
                "6": "passed",
                "7": "passed",
                "8": "passed",
                "9": "not_required",
                "10": "blocked",
            },
            "capabilities": [],
            "evidence_ids_used": ["E-COST-1"],
            "claims": [
                {
                    "id": "C-BAD-1",
                    "status": "УСТАНОВЛЕНО",
                    "text": "Причина выдумана из одного симптома.",
                    "evidence_ids": ["E-COST-1"],
                    "falsifier": "Движения покажут другую причину.",
                }
            ],
            "causal_chain": {"complete": False, "links": []},
            "requested_evidence": ["Движения документа"],
            "actions": [],
            "summary": "Некорректный тестовый результат.",
        }
        errors = validate_evals.validate_result(
            result, self.cases["under-evidenced-cost"]
        )
        self.assertTrue(any("final_status 'УСТАНОВЛЕНО' is forbidden" in error for error in errors))
        self.assertTrue(any("established claims 1 exceed allowed maximum 0" in error for error in errors))
        self.assertTrue(any("УСТАНОВЛЕНО requires a complete causal chain" in error for error in errors))

    def test_sonarqube_finding_cannot_replace_runtime_erp_evidence(self) -> None:
        case = self.cases["sonarqube-static-finding-no-runtime"]
        self.assertEqual(len(self.cases), 16)
        self.assertEqual(
            case["capabilities"],
            [{"name": "sonarqube-bsl-local", "status": "available"}],
        )
        self.assertEqual(case["expect"]["max_established_claims"], 0)
        self.assertFalse(case["expect"]["require_complete_causal_chain"])
        self.assertEqual(case["expect"]["required_gate_statuses"]["5"], "not_required")
        self.assertEqual(case["expect"]["required_gate_statuses"]["7"], "passed")
        self.assertEqual(case["expect"]["required_gate_statuses"]["10"], "blocked")
        self.assertEqual(case["expect"]["min_requested_evidence"], 2)

        result = {
            "schema_version": 1,
            "case_id": case["id"],
            "final_status": "УСТАНОВЛЕНО",
            "risk": "R0",
            "decision": "EVIDENCE_REQUIRED",
            "current_goal_status": "blocked",
            "linked_incident_status": "blocked",
            "gates": closed_gates(**{"5": "not_required", "9": "not_required", "10": "blocked"}),
            "capabilities": [
                {
                    "name": "sonarqube-bsl-local",
                    "status": "available",
                    "simulated": False,
                }
            ],
            "evidence_ids_used": ["E-SQ-1", "E-SQ-2"],
            "claims": [
                {
                    "id": "C-SQ-BAD-1",
                    "status": "УСТАНОВЛЕНО",
                    "text": "Статический finding объявлен причиной без runtime-цепочки.",
                    "evidence_ids": ["E-SQ-1", "E-SQ-2"],
                    "falsifier": "Трасса выполненной ветки и цепочка документа, движения и регистра.",
                }
            ],
            "causal_chain": {"complete": False, "links": []},
            "requested_evidence": [
                "Runtime-трасса выполнения отмеченной ветки",
                "Движения и записи регистров по единому аналитическому ключу",
            ],
            "actions": [],
            "summary": "Некорректный синтетический вывод из одного static finding.",
        }
        errors = validate_evals.validate_result(result, case)
        self.assertTrue(
            any("final_status 'УСТАНОВЛЕНО' is forbidden" in error for error in errors)
        )
        self.assertTrue(
            any("established claims 1 exceed allowed maximum 0" in error for error in errors)
        )
        self.assertTrue(
            any("УСТАНОВЛЕНО requires a complete causal chain" in error for error in errors)
        )

    def test_runtime_gate_rejects_incomplete_run(self) -> None:
        version = json.loads(
            validate_runtime_run.PLUGIN_MANIFEST.read_text(encoding="utf-8")
        )["version"]
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            manifest = {
                "schema_version": 1,
                "run_id": "incomplete-contract-test",
                "suite": self.suite["name"],
                "plugin_version": version,
                "source_commit": "0" * 40,
                "executed_at": "2026-08-19T12:00:00+03:00",
                "environment": {
                    "surface": "contract test",
                    "host": "local",
                    "clean_session": True,
                    "installed_plugin_version": version,
                    "expectations_visible_to_runner": False,
                },
                "results": [],
            }
            (run_dir / "run.json").write_text(
                json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
            )
            errors = validate_runtime_run.validate_runtime_run(run_dir)
        self.assertTrue(any("missing complete-suite results" in error for error in errors))
        self.assertTrue(
            any(f"exactly {len(self.cases)} entries" in error for error in errors)
        )
        self.assertTrue(any("all-zero placeholder" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
