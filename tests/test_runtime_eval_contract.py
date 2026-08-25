from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import validate_evals  # noqa: E402


def canonical_stale_result() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": "stale-execution-result",
        "final_status": "ТРЕБУЕТ ПРОВЕРКИ",
        "risk": "R0",
        "decision": "EVIDENCE_REQUIRED",
        "current_goal_status": "blocked",
        "linked_incident_status": "blocked",
        "gates": {
            "0": "passed",
            "1": "passed",
            "2": "passed",
            "3": "passed",
            "4": "passed",
            "5": "stale",
            "6": "passed",
            "7": "passed",
            "8": "passed",
            "9": "not_required",
            "10": "blocked",
        },
        "capabilities": [],
        "evidence_ids_used": ["E-RUN-1", "E-RUN-2"],
        "claims": [
            {
                "id": "C-RUN-1",
                "status": "ТРЕБУЕТ ПРОВЕРКИ",
                "text": (
                    "R-OLD подтверждает только результат RUN-OLD для INPUT-OLD "
                    "и не устанавливает текущее состояние INPUT-CURRENT."
                ),
                "evidence_ids": ["E-RUN-1", "E-RUN-2"],
                "falsifier": (
                    "Новый запуск для INPUT-CURRENT либо доказательство "
                    "детерминированной эквивалентности INPUT-OLD и INPUT-CURRENT."
                ),
            }
        ],
        "causal_chain": {"complete": False, "links": []},
        "requested_evidence": [
            "Актуальный результат анализа INPUT-CURRENT или доказательство "
            "эквивалентности INPUT-OLD и INPUT-CURRENT."
        ],
        "actions": [],
        "summary": (
            "R-OLD является stale для INPUT-CURRENT; текущее состояние требует "
            "актуального доказательства."
        ),
    }


def observed_v032_shape() -> dict[str, Any]:
    """Reproduce the material schema/semantic errors seen in the v0.3.2 smoke test."""
    result = canonical_stale_result()
    result["risk"] = "R3"
    result["decision"] = "NO-GO"
    result["linked_incident_status"] = "not_in_scope"
    result["claims"] = [
        {
            "claim": "R-OLD доказывает текущее состояние INPUT-CURRENT.",
            "status": "ТРЕБУЕТ ПРОВЕРКИ",
            "evidence_ids": [],
        }
    ]
    result["causal_chain"] = {
        "complete": True,
        "links": [
            "R-OLD относится к RUN-OLD.",
            "RUN-OLD анализировал INPUT-OLD.",
            "INPUT-CURRENT имеет другую идентичность.",
        ],
    }
    result["actions"] = [
        "Не использовать R-OLD как доказательство состояния INPUT-CURRENT."
    ]
    return result


class RuntimeEvalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.suite, cls.cases, cls.suite_errors = validate_evals.load_suite()
        cls.case = cls.cases["stale-execution-result"]

    def test_canonical_stale_result_passes_validator(self) -> None:
        self.assertEqual(self.suite_errors, [])
        self.assertEqual(
            validate_evals.validate_result(canonical_stale_result(), self.case),
            [],
        )

    def test_observed_v032_result_shape_is_rejected(self) -> None:
        errors = validate_evals.validate_result(observed_v032_shape(), self.case)
        joined = "\n".join(errors)
        self.assertIn("risk must be R0", joined)
        self.assertIn("decision must be EVIDENCE_REQUIRED", joined)
        self.assertIn("linked_incident_status 'not_in_scope' is forbidden", joined)
        self.assertIn("missing fields: falsifier, id, text", joined)
        self.assertIn("unexpected fields: claim", joined)
        self.assertIn("causal_chain.complete must be false", joined)
        self.assertIn("must be an object", joined)

    def test_each_reproduced_semantic_misclassification_fails_independently(self) -> None:
        mutations = {
            "risk": "R3",
            "decision": "NO-GO",
            "linked_incident_status": "not_in_scope",
        }
        expected_fragments = {
            "risk": "risk must be R0",
            "decision": "decision must be EVIDENCE_REQUIRED",
            "linked_incident_status": "linked_incident_status 'not_in_scope' is forbidden",
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                result = canonical_stale_result()
                result[field] = value
                errors = validate_evals.validate_result(result, self.case)
                self.assertTrue(
                    any(expected_fragments[field] in error for error in errors),
                    errors,
                )

    def test_rendered_prompt_contains_exact_machine_contract(self) -> None:
        rendered = validate_evals.render_prompt(self.case)
        self.assertIn("Верни только один JSON-объект без Markdown", rendered)
        self.assertIn('"risk": "<R0|R1|R2|R3>"', rendered)
        self.assertIn(
            '"decision": "<GO|NO-GO|NO_ACTION|EVIDENCE_REQUIRED>"',
            rendered,
        )
        self.assertIn('"gates": {', rendered)
        self.assertIn('"5": "<pending|passed|blocked|failed|stale|not_required>"', rendered)
        self.assertIn('"claims": []', rendered)
        self.assertIn('"causal_chain": {', rendered)
        self.assertIn('"actions": []', rendered)
        self.assertNotIn('"expect"', rendered)


if __name__ == "__main__":
    unittest.main()
