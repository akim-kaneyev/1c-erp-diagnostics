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


def observed_v035_stale_shape() -> dict[str, Any]:
    """Reproduce the exact stale-result contract failures observed in v0.3.5."""
    result = canonical_stale_result()
    result["linked_incident_status"] = "not_in_scope"
    result["gates"].update(
        {
            "1": "not_required",
            "2": "not_required",
            "3": "not_required",
            "4": "not_required",
            "5": "passed",
            "6": "not_required",
            "7": "not_required",
            "8": "not_required",
            "9": "not_required",
            "10": "passed",
        }
    )
    result["claims"] = [
        {
            "claim_id": "C-1",
            "status": "УСТАНОВЛЕНО",
            "statement": "Текущий вход имеет идентификатор INPUT-CURRENT.",
            "evidence_ids": ["E-RUN-1"],
        },
        {
            "claim_id": "C-2",
            "status": "УСТАНОВЛЕНО",
            "statement": "R-OLD получен для INPUT-OLD.",
            "evidence_ids": ["E-RUN-2"],
        },
        {
            "claim_id": "C-3",
            "status": "УСТАНОВЛЕНО",
            "statement": "R-OLD не доказывает INPUT-CURRENT.",
            "evidence_ids": ["E-RUN-1", "E-RUN-2"],
        },
        {
            "claim_id": "C-4",
            "status": "ТРЕБУЕТ ПРОВЕРКИ",
            "statement": "Текущий результат не установлен.",
            "evidence_ids": ["E-RUN-1", "E-RUN-2"],
        },
    ]
    result["causal_chain"] = {
        "complete": False,
        "links": [
            {
                "from": "INPUT-OLD",
                "to": "RUN-OLD",
                "relation": "analyzed_by",
                "evidence_ids": ["E-RUN-2"],
            }
        ],
    }
    result["requested_evidence"] = [
        {
            "evidence_type": "current_execution_result",
            "description": "Новый результат для INPUT-CURRENT.",
        }
    ]
    result["actions"] = [
        {
            "action_id": "A-1",
            "type": "evidence_control",
            "description": "Не использовать R-OLD.",
            "risk": "R0",
            "status": "required",
        }
    ]
    return result


def canonical_provenance_result() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": "provenance-closure-broken",
        "final_status": "ТРЕБУЕТ ПРОВЕРКИ",
        "risk": "R0",
        "decision": "EVIDENCE_REQUIRED",
        "current_goal_status": "closed",
        "linked_incident_status": "blocked",
        "gates": {
            "0": "passed",
            "1": "passed",
            "2": "passed",
            "3": "not_required",
            "4": "not_required",
            "5": "not_required",
            "6": "passed",
            "7": "passed",
            "8": "passed",
            "9": "not_required",
            "10": "passed",
        },
        "capabilities": [],
        "evidence_ids_used": ["E-PROV-1", "E-PROV-2"],
        "claims": [
            {
                "id": "C-PROV-1",
                "status": "УСТАНОВЛЕНО",
                "text": (
                    "У D-1 отсутствуют заявленные parent/derivation/run/output "
                    "идентификаторы, поэтому provenance closure не закрыта."
                ),
                "evidence_ids": ["E-PROV-2"],
                "falsifier": (
                    "Проверяемая lineage-запись связывает S-1 и D-1 через "
                    "документированную трансформацию и выходной идентификатор."
                ),
            },
            {
                "id": "C-PROV-2",
                "status": "ТРЕБУЕТ ПРОВЕРКИ",
                "text": (
                    "Значение из D-1 не доказывает наличие того же значения в S-1 "
                    "и не устанавливает причинную связь с симптомом."
                ),
                "evidence_ids": ["E-PROV-1", "E-PROV-2"],
                "falsifier": (
                    "Значение непосредственно найдено в идентифицированном S-1 "
                    "либо D-1 воспроизводимо получена из S-1 с совпадающим hash."
                ),
            },
        ],
        "causal_chain": {"complete": False, "links": []},
        "requested_evidence": [
            "Проверяемая lineage-запись и непосредственное подтверждение спорного "
            "значения в идентифицированном S-1."
        ],
        "actions": [],
        "summary": (
            "Оценка доказательности завершена: отсутствие lineage установлено, "
            "но источник значения и причинность остаются blocked."
        ),
    }


def observed_v033_provenance_shape() -> dict[str, Any]:
    """Reproduce the scope/capability errors seen after the first v0.3.3 retest."""
    result = canonical_provenance_result()
    result["linked_incident_status"] = "not_in_scope"
    result["capabilities"] = [
        {
            "name": "analysis_of_supplied_evidence_descriptions",
            "status": "available",
            "simulated": False,
        },
        {
            "name": "read_only_claim_and_provenance_synthesis",
            "status": "available",
            "simulated": False,
        },
        {
            "name": "adversarial_review_of_claims_and_lineage",
            "status": "available",
            "simulated": False,
        },
    ]
    return result


def canonical_capability_inventory_result() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "case_id": "capability-inventory",
        "final_status": "ТРЕБУЕТ ПРОВЕРКИ",
        "risk": "R0",
        "decision": "NO_ACTION",
        "current_goal_status": "closed",
        "linked_incident_status": "not_in_scope",
        "gates": {
            "0": "passed",
            "1": "not_required",
            "2": "not_required",
            "3": "not_required",
            "4": "not_required",
            "5": "not_required",
            "6": "not_required",
            "7": "not_required",
            "8": "not_required",
            "9": "not_required",
            "10": "passed",
        },
        "capabilities": [
            {"name": "unica", "status": "unavailable", "simulated": False},
            {
                "name": "1c-skills",
                "status": "confirmation_required",
                "simulated": False,
            },
            {"name": "1c-skills-py", "status": "available", "simulated": False},
            {"name": "opensandbox", "status": "prohibited", "simulated": False},
        ],
        "evidence_ids_used": ["E-CAP-1"],
        "claims": [],
        "causal_chain": {"complete": False, "links": []},
        "requested_evidence": [],
        "actions": [],
        "summary": (
            "Инвентаризация Gate 0 завершена по переданному синтетическому "
            "snapshot; вывод о состоянии или причине 1С не устанавливался."
        ),
    }


def observed_v034_capability_inventory_shape() -> dict[str, Any]:
    """Reproduce the exact contract failures observed in the v0.3.4 clean session."""
    result = canonical_capability_inventory_result()
    result["final_status"] = "УСТАНОВЛЕНО"
    result["gates"]["10"] = "not_required"
    result["capabilities"] = [
        {
            "name": "unica",
            "status": "unavailable",
            "evidence_id": "E-CAP-1",
        },
        {
            "name": "1c-skills",
            "status": "confirmation_required",
            "evidence_id": "E-CAP-1",
        },
        {
            "name": "1c-skills-py",
            "status": "available",
            "evidence_id": "E-CAP-1",
        },
        {
            "name": "opensandbox",
            "status": "prohibited",
            "evidence_id": "E-CAP-1",
        },
    ]
    result["claims"] = [
        {
            "claim": f"Inventory observation {index}",
            "status": "УСТАНОВЛЕНО",
            "evidence_ids": ["E-CAP-1"],
        }
        for index in range(1, 7)
    ]
    return result


class RuntimeEvalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.suite, cls.cases, cls.suite_errors = validate_evals.load_suite()
        cls.stale_case = cls.cases["stale-execution-result"]
        cls.provenance_case = cls.cases["provenance-closure-broken"]
        cls.capability_case = cls.cases["capability-inventory"]

    def test_canonical_stale_result_passes_validator(self) -> None:
        self.assertEqual(self.suite_errors, [])
        self.assertEqual(
            validate_evals.validate_result(canonical_stale_result(), self.stale_case),
            [],
        )

    def test_observed_v032_result_shape_is_rejected(self) -> None:
        errors = validate_evals.validate_result(observed_v032_shape(), self.stale_case)
        joined = "\n".join(errors)
        self.assertIn("risk must be R0", joined)
        self.assertIn("decision must be EVIDENCE_REQUIRED", joined)
        self.assertIn("linked_incident_status 'not_in_scope' is forbidden", joined)
        self.assertIn("missing fields: falsifier, id, text", joined)
        self.assertIn("unexpected fields: claim", joined)
        self.assertIn("causal_chain.complete must be false", joined)
        self.assertIn("must be an object", joined)


    def test_observed_v035_stale_shape_is_rejected(self) -> None:
        errors = validate_evals.validate_result(
            observed_v035_stale_shape(), self.stale_case
        )
        joined = "\n".join(errors)
        self.assertIn("linked_incident_status 'not_in_scope' is forbidden", joined)
        self.assertIn("Gate 5 must be 'stale', got 'passed'", joined)
        self.assertIn("Gate 7 must be 'passed', got 'not_required'", joined)
        self.assertIn("Gate 10 must be 'blocked', got 'passed'", joined)
        self.assertIn("Gate 10 passed requires current_goal_status closed", joined)
        self.assertIn("missing fields: falsifier, id, text", joined)
        self.assertIn("unexpected fields: claim_id, statement", joined)
        self.assertIn("established claims 3 exceed allowed maximum 0", joined)
        self.assertIn("missing fields: stage", joined)
        self.assertIn("unexpected fields: from, relation, to", joined)
        self.assertIn("requested_evidence must be a text list", joined)
        self.assertIn(
            "missing fields: approval_reference, approved, executed, rollback, validation",
            joined,
        )
        self.assertIn("unexpected fields: action_id, status, type", joined)


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
                errors = validate_evals.validate_result(result, self.stale_case)
                self.assertTrue(
                    any(expected_fragments[field] in error for error in errors),
                    errors,
                )

    def test_canonical_provenance_assessment_closes_only_current_goal(self) -> None:
        self.assertEqual(
            validate_evals.validate_result(
                canonical_provenance_result(), self.provenance_case
            ),
            [],
        )

    def test_observed_v033_provenance_scope_and_capabilities_are_rejected(self) -> None:
        errors = validate_evals.validate_result(
            observed_v033_provenance_shape(), self.provenance_case
        )
        joined = "\n".join(errors)
        self.assertIn("linked_incident_status 'not_in_scope' is forbidden", joined)
        self.assertIn(
            "result reports capabilities absent from the synthetic case snapshot",
            joined,
        )
        self.assertIn("analysis_of_supplied_evidence_descriptions", joined)

    def test_empty_capability_snapshot_rejects_an_invented_capability(self) -> None:
        result = canonical_stale_result()
        result["capabilities"] = [
            {
                "name": "internal_reasoning_role",
                "status": "available",
                "simulated": False,
            }
        ]
        errors = validate_evals.validate_result(result, self.stale_case)
        self.assertTrue(
            any("absent from the synthetic case snapshot" in error for error in errors),
            errors,
        )

    def test_canonical_capability_inventory_result_passes_validator(self) -> None:
        self.assertEqual(
            validate_evals.validate_result(
                canonical_capability_inventory_result(), self.capability_case
            ),
            [],
        )

    def test_observed_v034_capability_inventory_shape_is_rejected(self) -> None:
        errors = validate_evals.validate_result(
            observed_v034_capability_inventory_shape(), self.capability_case
        )
        joined = "\n".join(errors)
        self.assertIn(
            "final_status 'УСТАНОВЛЕНО' is forbidden for this case", joined
        )
        self.assertIn("Gate 10 must be 'passed', got 'not_required'", joined)
        self.assertIn("closed current goal requires Gate 10 passed", joined)
        self.assertIn("missing fields: simulated", joined)
        self.assertIn("unexpected fields: evidence_id", joined)
        self.assertIn("simulated must be false", joined)
        self.assertIn("missing fields: falsifier, id, text", joined)
        self.assertIn("unexpected fields: claim", joined)
        self.assertIn("established claims 6 exceed allowed maximum 0", joined)
        self.assertIn("УСТАНОВЛЕНО requires Gate 7 passed", joined)
        self.assertIn("УСТАНОВЛЕНО requires a complete causal chain", joined)
        self.assertIn(
            "УСТАНОВЛЕНО requires closed goal and Gate 10 passed", joined
        )

    def test_rendered_prompt_contains_exact_machine_and_capability_contract(self) -> None:
        rendered = validate_evals.render_prompt(self.stale_case)
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
        self.assertIn("верни capabilities: []", rendered)
        self.assertIn("Gate 5=stale", rendered)
        self.assertIn("Gate 7=passed", rendered)
        self.assertIn("Gate 10=blocked", rendered)
        self.assertIn("actions=[]", rendered)
        self.assertIn("ровно одну строку", rendered)
        self.assertNotIn('"expect"', rendered)

    def test_rendered_capability_prompt_contains_inventory_only_contract(self) -> None:
        rendered = validate_evals.render_prompt(self.capability_case)
        self.assertIn("final_status=ТРЕБУЕТ ПРОВЕРКИ", rendered)
        self.assertIn("Gate 0 и Gate 10=passed", rendered)
        self.assertIn("Gates 1–9=not_required", rendered)
        self.assertIn("ровно name, status, simulated", rendered)
        self.assertIn("claims=[]", rendered)
        self.assertIn("E-CAP-1 укажи только в evidence_ids_used", rendered)
        self.assertNotIn('"expect"', rendered)


if __name__ == "__main__":
    unittest.main()
