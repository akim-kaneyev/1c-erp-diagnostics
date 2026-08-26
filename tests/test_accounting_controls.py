from __future__ import annotations

import copy
import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from decimal import Decimal, Inexact, ROUND_UP, getcontext
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


ACCOUNTING = load_module(
    "accounting_invariants",
    "plugins/one-c-erp-diagnostics/skills/one-c-erp-diagnose-core/scripts/accounting_invariants.py",
)
CASE_STATE = load_module(
    "validate_case_state",
    "plugins/one-c-erp-diagnostics/skills/one-c-erp-case-state/scripts/validate_case_state.py",
)


def allocation_rows(a: str, b: str, residual: str = "0") -> dict:
    return {
        "by_analytic": [
            {"analytic_key": "A", "amount": a},
            {"analytic_key": "B", "amount": b},
        ],
        "residual": residual,
    }


def row(
    row_id: str,
    source: str,
    kind: str,
    analytic: str,
    fact: str,
    plan: str,
) -> dict:
    return {
        "row_id": row_id,
        "group_key": "G-1",
        "source": source,
        "kind": kind,
        "analytic_key": analytic,
        "fact": fact,
        "plan": plan,
        "quantity_fact": "0",
        "quantity_plan": "0",
        "included": True,
        "exclusion_reason": "",
        "exclusion_evidence_ids": [],
    }


def six_rows(*, after: bool = False) -> dict:
    fallback_fact = "0" if after else "100"
    fallback_plan = "0" if after else "100"
    rows = [
        row("R-PLAN-A", "plan", "plan", "A", "0", "100"),
        row("R-PLAN-B", "plan", "plan", "B", "0", "900"),
        row("R-FALLBACK-A", "fallback", "fallback", "A", fallback_fact, fallback_plan),
        row("R-FALLBACK-B", "fallback", "fallback", "B", "0", "0"),
        row("R-FACT-A", "fact", "fact", "A", "100", "0"),
        row("R-FACT-B", "fact", "fact", "B", "900", "0"),
    ]
    return {
        "schema_version": 1,
        "dataset_id": "after" if after else "before",
        "evidence_ids": [],
        "expected_row_ids": [item["row_id"] for item in rows],
        "rounding_scale": 2,
        "rows": rows,
        "observed_allocation": allocation_rows("11", "99")
        if after
        else allocation_rows("20", "90"),
    }


def empty_state() -> dict:
    return {
        "schema_version": 1,
        "case_id": "CASE-SYNTHETIC",
        "evidence": [],
        "runs": [],
        "claims": [],
        "documents": [],
        "gates": [
            {"id": str(index), "status": "pending", "claim_ids": []}
            for index in range(11)
        ],
        "active_index": {"run_id": None, "claim_ids": [], "document_ids": []},
    }


def evidence(evidence_id: str, *, status: str = "active", derived_from=None, run_id=None) -> dict:
    parents = list(derived_from or [])
    return {
        "id": evidence_id,
        "status": status,
        "derived_from": parents,
        "run_id": run_id,
        "artifact_hash": "a" * 64,
        "transformation": "synthetic transformation" if parents else None,
        "tool": "synthetic-tool" if parents and run_id is None else None,
        "tool_version": "synthetic-ref" if parents and run_id is None else None,
        "limitations": [],
        "superseded_by": None,
        "invalidates_ids": [],
    }


def claim(claim_id: str, evidence_ids: list[str], *, status: str = "УСТАНОВЛЕНО") -> dict:
    return {
        "id": claim_id,
        "status": status,
        "evidence_ids": evidence_ids,
        "depends_on_claim_ids": [],
        "document_ids": [],
        "historical_document_ids": [],
        "superseded_by": None,
        "invalidates_ids": [],
    }


def run_record(
    run_id: str,
    input_evidence_id: str,
    *,
    input_hash: str = "a" * 64,
    status: str = "current",
    started_at: str = "2026-01-01T00:00:00Z",
    completed_at: str = "2026-01-01T00:01:00Z",
) -> dict:
    return {
        "id": run_id,
        "case_id": "CASE-SYNTHETIC",
        "status": status,
        "input_evidence_ids": [input_evidence_id],
        "input_hashes": [input_hash],
        "release": "synthetic-release",
        "extension_set": [],
        "period": "synthetic-period",
        "tool": "synthetic-tool",
        "tool_version": "synthetic-ref",
        "operation": "synthetic-operation",
        "limitations": [],
        "started_at": started_at,
        "completed_at": completed_at,
        "superseded_by": None,
        "invalidates_ids": [],
    }


class AccountingInvariantTests(unittest.TestCase):
    def test_six_rows_balance_and_allocate_20_90(self) -> None:
        result = ACCOUNTING.analyze_dataset(six_rows(), Decimal("110"))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["totals"]["fact"], "1100")
        self.assertEqual(result["totals"]["plan"], "1100")
        self.assertEqual(result["totals"]["sum_share"], "1")
        self.assertEqual(
            {item["analytic_key"]: item["rounded_allocated"] for item in result["allocation"]},
            {"A": "20", "B": "90"},
        )
        self.assertEqual(result["totals"]["observed_residual"], "0")

    def test_missing_fact_row_fails_with_row_id_and_1000_1100(self) -> None:
        payload = six_rows()
        payload["rows"] = [item for item in payload["rows"] if item["row_id"] != "R-FACT-A"]
        result = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["totals"]["fact"], "1000")
        self.assertEqual(result["totals"]["plan"], "1100")
        missing = [item for item in result["errors"] if item["code"] == "missing_expected_row"]
        self.assertEqual(missing[0]["row_ids"], ["R-FACT-A"])

    def test_patch_changes_proportion_not_completeness(self) -> None:
        result = ACCOUNTING.compare_datasets(six_rows(), six_rows(after=True), Decimal("110"))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["after"]["totals"]["fact"], "1000")
        self.assertEqual(result["after"]["totals"]["plan"], "1000")
        self.assertEqual(
            {item["analytic_key"]: item["rounded_allocated"] for item in result["after"]["allocation"]},
            {"A": "11", "B": "99"},
        )
        self.assertEqual(
            result["effect"],
            {
                "completeness_changed": False,
                "allocation_proportion_changed": True,
                "analytic_key_changed": False,
                "cardinality_changed": False,
                "no_material_change": False,
                "business_basis_required": True,
                "changed_metrics": ["allocation_proportion", "totals"],
            },
        )

    def test_repeating_thirds_use_deterministic_rounding_without_false_residual(self) -> None:
        rows = [row(f"R-{key}", "source", "fact_plan", key, "1", "1") for key in "ABC"]
        payload = {
            "schema_version": 1,
            "dataset_id": "thirds",
            "evidence_ids": [],
            "expected_row_ids": [item["row_id"] for item in rows],
            "rounding_scale": 2,
            "rows": rows,
            "observed_allocation": {
                "by_analytic": [
                    {"analytic_key": "A", "amount": "33.33"},
                    {"analytic_key": "B", "amount": "33.33"},
                    {"analytic_key": "C", "amount": "33.34"},
                ],
                "residual": "0",
            },
        }
        result = ACCOUNTING.analyze_dataset(payload, Decimal("100"))
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["totals"]["distributed_fraction"], "100/1")
        self.assertEqual(result["totals"]["residual_fraction"], "0/1")

    def test_fraction_rendering_ignores_ambient_decimal_context_and_traps(self) -> None:
        original = getcontext().copy()
        try:
            getcontext().prec = 2
            getcontext().rounding = ROUND_UP
            getcontext().traps[Inexact] = True
            self.test_repeating_thirds_use_deterministic_rounding_without_false_residual()
        finally:
            getcontext().prec = original.prec
            getcontext().rounding = original.rounding
            getcontext().traps = original.traps.copy()

    def test_wrong_observed_proportion_fails_even_when_total_closes(self) -> None:
        payload = six_rows()
        payload["observed_allocation"] = allocation_rows("0", "110")
        result = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(
            sum(item["code"] == "observed_allocation_mismatch" for item in result["errors"]),
            2,
        )

    def test_missing_observed_allocation_is_unavailable_not_synthetic_zero(self) -> None:
        payload = six_rows()
        del payload["observed_allocation"]
        result = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["observed_allocation"]["status"], "unavailable")
        self.assertEqual(result["observed_allocation"]["by_analytic"], [])
        self.assertIsNone(result["observed_allocation"]["residual"])
        self.assertIsNone(result["totals"]["observed_distributed"])
        self.assertIsNone(result["totals"]["observed_residual"])
        self.assertNotIn(
            "observed-balance",
            {item["formula_id"] for item in result["formula_trace"]},
        )

    def test_excluded_row_requires_reason_and_evidence(self) -> None:
        payload = six_rows()
        payload["rows"][0]["included"] = False
        result = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        self.assertTrue(any(item["code"] == "unexplained_exclusion" for item in result["errors"]))

    def test_exclusion_evidence_must_exist_in_dataset_manifest(self) -> None:
        payload = six_rows(after=True)
        excluded = payload["rows"][2]
        excluded["included"] = False
        excluded["exclusion_reason"] = "synthetic exclusion"
        excluded["exclusion_evidence_ids"] = ["E-MISSING"]
        result = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "unknown_exclusion_evidence",
            {item["code"] for item in result["errors"]},
        )

        payload["evidence_ids"] = ["E-MISSING"]
        self.assertEqual(
            ACCOUNTING.analyze_dataset(payload, Decimal("110"))["status"],
            "PASS",
        )

    def test_float_and_unknown_inclusion_are_rejected(self) -> None:
        payload = six_rows()
        payload["rows"][0]["fact"] = 1.0
        payload["rows"][1]["included"] = "unknown"
        result = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        codes = {item["code"] for item in result["errors"]}
        self.assertIn("invalid_decimal", codes)
        self.assertIn("unknown_inclusion", codes)

    def test_zero_denominator_and_duplicate_row_id_fail(self) -> None:
        payload = six_rows()
        for item in payload["rows"]:
            item["fact"] = "0"
            item["plan"] = "0"
        payload["observed_allocation"] = allocation_rows("0", "0", "110")
        payload["rows"].append(copy.deepcopy(payload["rows"][0]))
        result = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        codes = {item["code"] for item in result["errors"]}
        self.assertIn("zero_plan", codes)
        self.assertIn("duplicate_row_id", codes)

    def test_large_integer_delta_is_not_lost_to_decimal_context(self) -> None:
        payload = {
            "schema_version": 1,
            "dataset_id": "large-exact-delta",
            "evidence_ids": [],
            "expected_row_ids": ["R-LARGE"],
            "rounding_scale": 2,
            "rows": [
                row(
                    "R-LARGE",
                    "source",
                    "fact_plan",
                    "A",
                    "10000000000000000000000000001",
                    "10000000000000000000000000000",
                )
            ],
            "observed_allocation": {
                "by_analytic": [{"analytic_key": "A", "amount": "1"}],
                "residual": "0",
            },
        }
        result = ACCOUNTING.analyze_dataset(payload, Decimal("1"))
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["totals"]["amount_delta"], "1")
        self.assertNotEqual(result["totals"]["fact"], result["totals"]["plan"])

    def test_row_analytic_swap_is_material_even_when_totals_and_shares_match(self) -> None:
        before_rows = [
            row("R-A", "source", "fact_plan", "A", "50", "50"),
            row("R-B", "source", "fact_plan", "B", "50", "50"),
        ]
        after_rows = copy.deepcopy(before_rows)
        after_rows[0]["analytic_key"] = "B"
        after_rows[1]["analytic_key"] = "A"

        def dataset(dataset_id: str, rows: list[dict]) -> dict:
            return {
                "schema_version": 1,
                "dataset_id": dataset_id,
                "evidence_ids": [],
                "expected_row_ids": [item["row_id"] for item in rows],
                "rounding_scale": 2,
                "rows": rows,
                "observed_allocation": allocation_rows("50", "50"),
            }

        result = ACCOUNTING.compare_datasets(
            dataset("before-swap", before_rows),
            dataset("after-swap", after_rows),
            Decimal("100"),
        )
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["effect"]["analytic_key_changed"])
        self.assertFalse(result["effect"]["no_material_change"])
        self.assertTrue(result["effect"]["business_basis_required"])

    def test_request_hash_includes_input_and_ignores_row_transport_order(self) -> None:
        payload = six_rows()
        payload["evidence_ids"] = ["E-2", "E-1"]
        excluded = next(item for item in payload["rows"] if item["row_id"] == "R-FALLBACK-B")
        excluded["included"] = False
        excluded["exclusion_reason"] = "synthetic zero-row exclusion"
        excluded["exclusion_evidence_ids"] = ["E-2", "E-1"]
        first = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        reordered = copy.deepcopy(payload)
        reordered["evidence_ids"].reverse()
        reordered["rows"].reverse()
        reordered["expected_row_ids"].reverse()
        reordered["observed_allocation"]["by_analytic"].reverse()
        next(
            item for item in reordered["rows"] if item["row_id"] == "R-FALLBACK-B"
        )["exclusion_evidence_ids"].reverse()
        second = ACCOUNTING.analyze_dataset(reordered, Decimal("110"))
        spaced_ids = copy.deepcopy(payload)
        spaced_ids["evidence_ids"] = [" E-2 ", "E-1"]
        next(
            item for item in spaced_ids["rows"] if item["row_id"] == "R-FALLBACK-B"
        )["exclusion_evidence_ids"] = [" E-2 ", "E-1"]
        fourth = ACCOUNTING.analyze_dataset(spaced_ids, Decimal("110"))
        numeric_transport = copy.deepcopy(payload)
        numeric_transport["rows"][0]["fact"] = 0
        numeric_transport["rows"][0]["plan"] = " 100.00 "
        numeric_transport["rows"][0]["quantity_fact"] = " 0.000 "
        numeric_transport["observed_allocation"]["by_analytic"][0]["amount"] = " 20.0 "
        fifth = ACCOUNTING.analyze_dataset(numeric_transport, Decimal("110"))
        changed_input = copy.deepcopy(payload)
        changed_input["observed_allocation"] = allocation_rows("24", "96")
        third = ACCOUNTING.analyze_dataset(changed_input, Decimal("120"))
        self.assertEqual(first["input_sha256"], second["input_sha256"])
        self.assertEqual(first["input_sha256"], fourth["input_sha256"])
        self.assertEqual(first["input_sha256"], fifth["input_sha256"])
        self.assertNotEqual(first["input_sha256"], third["input_sha256"])
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, sort_keys=True),
            json.dumps(second, ensure_ascii=False, sort_keys=True),
        )
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, sort_keys=True),
            json.dumps(fourth, ensure_ascii=False, sort_keys=True),
        )
        self.assertEqual(
            json.dumps(first, ensure_ascii=False, sort_keys=True),
            json.dumps(fifth, ensure_ascii=False, sort_keys=True),
        )

    def test_invalid_raw_values_have_distinct_non_secret_request_hashes(self) -> None:
        markers = (
            "synthetic-invalid-fact-bad-one",
            "synthetic-invalid-fact-bad-two",
        )
        results = []
        for marker in markers:
            payload = six_rows()
            payload["rows"][0]["fact"] = marker
            results.append(ACCOUNTING.analyze_dataset(payload, Decimal("110")))

        self.assertTrue(all(result["status"] == "FAIL" for result in results))
        self.assertNotEqual(results[0]["input_sha256"], results[1]["input_sha256"])
        rendered = json.dumps(results, ensure_ascii=False, sort_keys=True)
        for marker in markers:
            self.assertNotIn(marker, rendered)

    def test_invalid_input_fingerprint_is_type_safe_and_non_secret(self) -> None:
        marker = "synthetic-invalid-nested-value"
        raw_values = [True, 1.5, {"nested": [marker]}]
        results = []
        for raw_value in raw_values:
            payload = six_rows()
            payload["rows"][0]["fact"] = raw_value
            results.append(ACCOUNTING.analyze_dataset(payload, Decimal("110")))

        self.assertTrue(all(result["status"] == "FAIL" for result in results))
        self.assertEqual(
            len({result["input_sha256"] for result in results}),
            len(results),
        )
        self.assertNotIn(
            marker,
            json.dumps(results, ensure_ascii=False, sort_keys=True),
        )

    def test_csv_and_json_inputs_have_equivalent_accounting_result(self) -> None:
        payload = six_rows()
        expected = ACCOUNTING.analyze_dataset(payload, Decimal("110"))
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            csv_path = work / "before.csv"
            fieldnames = list(payload["rows"][0])
            with csv_path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fieldnames)
                writer.writeheader()
                for source_row in payload["rows"]:
                    csv_row = dict(source_row)
                    csv_row["exclusion_evidence_ids"] = ""
                    writer.writerow(csv_row)
            manifest = work / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "evidence_ids": payload["evidence_ids"],
                        "expected_row_ids": payload["expected_row_ids"],
                        "rounding_scale": payload["rounding_scale"],
                        "observed_allocation": payload["observed_allocation"],
                    }
                ),
                encoding="utf-8",
            )
            actual = ACCOUNTING.analyze_dataset(
                ACCOUNTING.load_dataset(csv_path, manifest), Decimal("110")
            )
        self.assertEqual(actual["status"], "PASS")
        self.assertEqual(actual["totals"], expected["totals"])
        self.assertEqual(actual["allocation"], expected["allocation"])

    def test_csv_with_unnamed_extra_column_returns_controlled_fail(self) -> None:
        payload = six_rows()
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            csv_path = work / "malformed.csv"
            headers = list(payload["rows"][0])
            csv_path.write_text(
                ",".join(headers) + "\n" + ",".join(["x"] * (len(headers) + 1)) + "\n",
                encoding="utf-8",
            )
            manifest = work / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "evidence_ids": [],
                        "expected_row_ids": payload["expected_row_ids"],
                        "rounding_scale": 2,
                        "observed_allocation": payload["observed_allocation"],
                    }
                ),
                encoding="utf-8",
            )
            result = ACCOUNTING.analyze_dataset(
                ACCOUNTING.load_dataset(csv_path, manifest), Decimal("110")
            )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("invalid_row", {item["code"] for item in result["errors"]})


class CaseStateTests(unittest.TestCase):
    def test_tracked_state_template_is_valid(self) -> None:
        state = json.loads((ROOT / "templates/case/STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(CASE_STATE.validate_state(state)["status"], "PASS")

    def test_duplicate_and_cross_entity_ids_fail(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("X"), evidence("X")]
        state["claims"] = [claim("X", []), claim("X", [])]
        result = CASE_STATE.validate_state(state)
        codes = {item["code"] for item in result["errors"]}
        self.assertIn("duplicate_id", codes)
        self.assertIn("cross_entity_duplicate_id", codes)
        duplicate_locations = {
            item["location"]
            for item in result["errors"]
            if item["code"] == "duplicate_id"
        }
        self.assertEqual(duplicate_locations, {"evidence[1].id", "claims[1].id"})

    def test_stale_source_propagates_through_derived_claim_document_and_gates(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-SOURCE", status="stale"),
            evidence("E-DERIVED", derived_from=["E-SOURCE"]),
        ]
        state["claims"] = [claim("C-ROOT", ["E-DERIVED"])]
        state["documents"] = [
            {
                "id": "D-REPORT",
                "status": "current",
                "claim_ids": ["C-ROOT"],
                "superseded_by": None,
                "invalidates_ids": [],
            }
        ]
        for gate in state["gates"]:
            if int(gate["id"]) >= 6:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-ROOT"] if gate["id"] == "6" else []
        state["active_index"]["claim_ids"] = ["C-ROOT"]
        state["active_index"]["document_ids"] = ["D-REPORT"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["invalidated_evidence_ids"], ["E-DERIVED", "E-SOURCE"])
        self.assertEqual(result["invalidated_claim_ids"], ["C-ROOT"])
        self.assertEqual(result["invalidated_document_ids"], ["D-REPORT"])
        self.assertEqual(result["invalidated_gate_ids"], ["6", "7", "8", "9", "10"])

    def test_global_invalidation_can_target_derived_evidence(self) -> None:
        state = empty_state()
        old = evidence("E-DERIVED")
        new = evidence("E-PRIMARY")
        new["invalidates_ids"] = ["E-DERIVED"]
        state["evidence"] = [old, new]
        state["claims"] = [claim("C-OLD", ["E-DERIVED"])]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("E-DERIVED", result["invalidated_evidence_ids"])
        self.assertIn("C-OLD", result["invalidated_claim_ids"])

    def test_unknown_reference_and_temporal_self_cycle_fail(self) -> None:
        state = empty_state()
        item = evidence("E-ONE")
        item["derived_from"] = ["E-MISSING"]
        item["invalidates_ids"] = ["E-ONE"]
        state["evidence"] = [item]
        result = CASE_STATE.validate_state(state)
        codes = {error["code"] for error in result["errors"]}
        self.assertIn("unknown_reference", codes)
        self.assertIn("reference_cycle", codes)

    def test_reference_cycle_projects_to_claims_and_gates(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-1", derived_from=["E-2"]),
            evidence("E-2", derived_from=["E-1"]),
        ]
        state["claims"] = [claim("C-1", ["E-1"])]
        state["active_index"]["claim_ids"] = ["C-1"]
        for gate in state["gates"]:
            if int(gate["id"]) >= 6:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-1"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("reference_cycle", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_evidence_ids"], ["E-1", "E-2"])
        self.assertEqual(result["invalidated_claim_ids"], ["C-1"])
        self.assertEqual(result["invalidated_gate_ids"], ["6", "7", "8", "9", "10"])

    def test_exact_entity_schema_failure_projects_invalidation(self) -> None:
        state = empty_state()
        source = evidence("E-1")
        del source["transformation"]
        state["evidence"] = [source]
        state["claims"] = [claim("C-1", ["E-1"])]
        state["active_index"]["claim_ids"] = ["C-1"]
        for gate in state["gates"]:
            if int(gate["id"]) >= 6:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-1"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("missing_fields", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_evidence_ids"], ["E-1"])
        self.assertEqual(result["invalidated_claim_ids"], ["C-1"])
        self.assertEqual(result["invalidated_gate_ids"], ["6", "7", "8", "9", "10"])

    def test_stale_run_input_propagates_to_output(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-INPUT", status="stale"),
            evidence("E-OUTPUT", derived_from=["E-INPUT"], run_id="RUN-1"),
        ]
        state["runs"] = [
            {
                "id": "RUN-1",
                "case_id": state["case_id"],
                "status": "current",
                "input_evidence_ids": ["E-INPUT"],
                "input_hashes": ["a" * 64],
                "release": "synthetic-release",
                "extension_set": [],
                "period": "synthetic-period",
                "tool": "synthetic-tool",
                "tool_version": "synthetic-ref",
                "operation": "synthetic-operation",
                "limitations": [],
                "started_at": "2026-01-01T00:00:00Z",
                "completed_at": "2026-01-01T00:01:00Z",
                "superseded_by": None,
                "invalidates_ids": [],
            }
        ]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["invalidated_run_ids"], ["RUN-1"])
        self.assertEqual(result["invalidated_evidence_ids"], ["E-INPUT", "E-OUTPUT"])

    def test_run_input_hash_must_match_referenced_evidence(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-INPUT"),
            evidence("E-OUTPUT", derived_from=["E-INPUT"], run_id="RUN-1"),
        ]
        state["runs"] = [run_record("RUN-1", "E-INPUT", input_hash="b" * 64)]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("run_input_hash_mismatch", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_run_ids"], ["RUN-1"])
        self.assertIn("E-OUTPUT", result["invalidated_evidence_ids"])

    def test_distinct_inputs_may_have_the_same_artifact_hash(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-1"),
            evidence("E-2"),
            evidence("E-OUT", derived_from=["E-1", "E-2"], run_id="RUN-1"),
        ]
        run = run_record("RUN-1", "E-1")
        run["input_evidence_ids"] = ["E-1", "E-2"]
        run["input_hashes"] = ["a" * 64, "a" * 64]
        state["runs"] = [run]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "PASS", result["errors"])

    def test_duplicate_run_input_id_invalidates_run_and_output(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-INPUT"),
            evidence("E-OUTPUT", derived_from=["E-INPUT"], run_id="RUN-1"),
        ]
        run = run_record("RUN-1", "E-INPUT")
        run["input_evidence_ids"] = ["E-INPUT", "E-INPUT"]
        run["input_hashes"] = ["a" * 64, "a" * 64]
        state["runs"] = [run]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("duplicate_reference", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_run_ids"], ["RUN-1"])
        self.assertIn("E-OUTPUT", result["invalidated_evidence_ids"])

    def test_duplicate_output_lineage_invalidates_downstream_projection(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-INPUT"),
            evidence(
                "E-OUTPUT",
                derived_from=["E-INPUT", "E-INPUT"],
                run_id="RUN-1",
            ),
        ]
        state["runs"] = [run_record("RUN-1", "E-INPUT")]
        state["claims"] = [claim("C-1", ["E-OUTPUT"])]
        state["active_index"]["run_id"] = "RUN-1"
        state["active_index"]["claim_ids"] = ["C-1"]
        for gate in state["gates"]:
            if int(gate["id"]) >= 6:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-1"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("duplicate_reference", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_run_ids"], ["RUN-1"])
        self.assertIn("E-OUTPUT", result["invalidated_evidence_ids"])
        self.assertIn("C-1", result["invalidated_claim_ids"])
        self.assertTrue(
            {"6", "7", "8", "9", "10"}.issubset(result["invalidated_gate_ids"])
        )

    def test_execution_and_derivation_identity_are_machine_required(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-INPUT"),
            evidence("E-OUTPUT", derived_from=["E-INPUT"], run_id="RUN-1"),
        ]
        run = run_record("RUN-1", "E-INPUT")
        del run["tool_version"]
        state["runs"] = [run]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("RUN-1", result["invalidated_run_ids"])
        self.assertIn("E-OUTPUT", result["invalidated_evidence_ids"])

        no_output = empty_state()
        no_output["evidence"] = [evidence("E-INPUT")]
        no_output["runs"] = [run_record("RUN-1", "E-INPUT")]
        no_output["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(no_output)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("run_identity_incomplete", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_run_ids"], ["RUN-1"])

        untracked_derivation = empty_state()
        derived = evidence("E-DERIVED", derived_from=["E-SOURCE"])
        derived["tool"] = None
        derived["tool_version"] = None
        untracked_derivation["evidence"] = [evidence("E-SOURCE"), derived]
        result = CASE_STATE.validate_state(untracked_derivation)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "derivation_identity_incomplete",
            {item["code"] for item in result["errors"]},
        )
        self.assertIn("E-DERIVED", result["invalidated_evidence_ids"])

    def test_material_claim_without_evidence_cannot_pass_downstream_gates(self) -> None:
        state = empty_state()
        state["claims"] = [claim("C-ROOT", [])]
        state["active_index"]["claim_ids"] = ["C-ROOT"]
        for gate in state["gates"]:
            if int(gate["id"]) < 6:
                gate["status"] = "not_required"
            else:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-ROOT"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "claim_evidence_incomplete",
            {item["code"] for item in result["errors"]},
        )
        self.assertEqual(result["invalidated_claim_ids"], ["C-ROOT"])
        self.assertEqual(result["invalidated_gate_ids"], ["6", "7", "8", "9", "10"])

    def test_passed_gates_must_cover_every_active_material_claim(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-1"), evidence("E-2")]
        state["claims"] = [claim("C-1", ["E-1"]), claim("C-2", ["E-2"])]
        state["active_index"]["claim_ids"] = ["C-1", "C-2"]
        for gate in state["gates"]:
            if int(gate["id"]) < 6:
                gate["status"] = "not_required"
            else:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-1"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("unmapped_passed_gate", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_gate_ids"], ["6", "7", "8", "9", "10"])

    def test_run_cannot_use_its_own_output_as_input(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-LOOP", run_id="RUN-1")]
        state["runs"] = [run_record("RUN-1", "E-LOOP")]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        codes = {item["code"] for item in result["errors"]}
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("run_output_is_input", codes)
        self.assertIn("run_output_lineage_mismatch", codes)
        self.assertEqual(result["invalidated_run_ids"], ["RUN-1"])
        self.assertEqual(result["invalidated_evidence_ids"], ["E-LOOP"])

    def test_run_output_lineage_must_match_run_inputs(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-A"),
            evidence("E-B"),
            evidence("E-OUT", derived_from=["E-A"], run_id="RUN-1"),
        ]
        state["runs"] = [run_record("RUN-1", "E-B")]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "run_output_lineage_mismatch",
            {item["code"] for item in result["errors"]},
        )
        self.assertEqual(result["invalidated_run_ids"], ["RUN-1"])
        self.assertIn("E-OUT", result["invalidated_evidence_ids"])

    def test_run_case_mismatch_invalidates_output_claim_and_downstream_gates(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-INPUT"),
            evidence("E-OUTPUT", derived_from=["E-INPUT"], run_id="RUN-1"),
        ]
        mismatched = run_record("RUN-1", "E-INPUT")
        mismatched["case_id"] = "CASE-OTHER"
        state["runs"] = [mismatched]
        state["claims"] = [claim("C-OUTPUT", ["E-OUTPUT"])]
        state["active_index"]["run_id"] = "RUN-1"
        state["active_index"]["claim_ids"] = ["C-OUTPUT"]
        for gate in state["gates"]:
            if int(gate["id"]) >= 6:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-OUTPUT"]

        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("RUN-1", result["invalidated_run_ids"])
        self.assertIn("E-OUTPUT", result["invalidated_evidence_ids"])
        self.assertIn("C-OUTPUT", result["invalidated_claim_ids"])
        self.assertEqual(result["invalidated_gate_ids"], ["5", "6", "7", "8", "9", "10"])

    def test_stale_gate_invalidates_every_required_downstream_gate(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-1")]
        state["claims"] = [claim("C-1", ["E-1"])]
        state["active_index"]["claim_ids"] = ["C-1"]
        for gate in state["gates"]:
            if gate["id"] == "5":
                gate["status"] = "stale"
            elif int(gate["id"]) >= 6:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-1"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["invalidated_gate_ids"], ["5", "6", "7", "8", "9", "10"])

    def test_claim_side_document_link_propagates_stale_status(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-STALE", status="stale"),
            evidence("E-ACTIVE"),
        ]
        stale_claim = claim("C-STALE", ["E-STALE"], status="stale")
        stale_claim["document_ids"] = ["D-REPORT"]
        state["claims"] = [stale_claim, claim("C-ACTIVE", ["E-ACTIVE"])]
        state["documents"] = [
            {
                "id": "D-REPORT",
                "status": "current",
                "claim_ids": [],
                "superseded_by": None,
                "invalidates_ids": [],
            }
        ]
        state["active_index"]["claim_ids"] = ["C-ACTIVE"]
        state["active_index"]["document_ids"] = ["D-REPORT"]
        for gate in state["gates"]:
            if int(gate["id"]) >= 6:
                gate["status"] = "passed"
                gate["claim_ids"] = ["C-ACTIVE"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("D-REPORT", result["invalidated_document_ids"])
        self.assertEqual(result["invalidated_gate_ids"], ["6", "7", "8", "9", "10"])

    def test_superseding_run_cannot_predate_superseded_completion(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-INPUT")]
        older = run_record(
            "RUN-OLD",
            "E-INPUT",
            status="superseded",
            started_at="2026-01-02T00:00:00Z",
            completed_at="2026-01-02T00:10:00Z",
        )
        older["superseded_by"] = "RUN-NEW"
        newer = run_record(
            "RUN-NEW",
            "E-INPUT",
            started_at="2026-01-01T00:00:00Z",
            completed_at="2026-01-01T00:10:00Z",
        )
        state["runs"] = [older, newer]
        state["active_index"]["run_id"] = "RUN-NEW"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "invalid_supersession_chronology",
            {item["code"] for item in result["errors"]},
        )
        self.assertIn("RUN-NEW", result["invalidated_run_ids"])

    def test_only_active_run_id_may_remain_current(self) -> None:
        state = empty_state()
        state["evidence"] = [
            evidence("E-INPUT"),
            evidence("E-OLD", derived_from=["E-INPUT"], run_id="RUN-OLD"),
            evidence("E-NEW", derived_from=["E-INPUT"], run_id="RUN-NEW"),
        ]
        state["runs"] = [
            run_record("RUN-OLD", "E-INPUT"),
            run_record(
                "RUN-NEW",
                "E-INPUT",
                started_at="2026-01-01T00:02:00Z",
                completed_at="2026-01-01T00:03:00Z",
            ),
        ]
        state["claims"] = [claim("C-MIXED", ["E-OLD", "E-NEW"])]
        state["active_index"]["run_id"] = "RUN-NEW"
        state["active_index"]["claim_ids"] = ["C-MIXED"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("RUN-OLD", result["invalidated_run_ids"])
        self.assertIn("C-MIXED", result["invalidated_claim_ids"])

    def test_malformed_run_lists_return_fail_without_exception(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-INPUT")]
        malformed = run_record("RUN-1", "E-INPUT")
        malformed["extension_set"] = None
        state["runs"] = [malformed]
        state["active_index"]["run_id"] = "RUN-1"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("invalid_list", {item["code"] for item in result["errors"]})

    def test_historical_document_cannot_be_current_source_or_active(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-1")]
        current_claim = claim("C-1", ["E-1"])
        current_claim["document_ids"] = ["D-HISTORY"]
        state["claims"] = [current_claim]
        state["documents"] = [
            {
                "id": "D-HISTORY",
                "status": "historical",
                "claim_ids": [],
                "superseded_by": None,
                "invalidates_ids": [],
            }
        ]
        state["active_index"]["claim_ids"] = ["C-1"]
        state["active_index"]["document_ids"] = ["D-HISTORY"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        codes = {item["code"] for item in result["errors"]}
        self.assertIn("superseded_current_source", codes)
        self.assertIn("invalid_active_document", codes)

    def test_passed_downstream_gates_cannot_omit_active_claim_mapping(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-STALE", status="stale")]
        state["claims"] = [claim("C-STALE", ["E-STALE"], status="stale")]
        for gate in state["gates"]:
            if int(gate["id"]) >= 6:
                gate["status"] = "passed"
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("unmapped_passed_gate", {item["code"] for item in result["errors"]})
        self.assertEqual(result["invalidated_gate_ids"], ["6", "7", "8", "9", "10"])

    def test_dependency_and_supersession_edges_do_not_form_false_cycle(self) -> None:
        state = empty_state()
        old = evidence("E-OLD", status="superseded")
        old["superseded_by"] = "E-NEW"
        new = evidence("E-NEW", derived_from=["E-OLD"])
        state["evidence"] = [old, new]
        result = CASE_STATE.validate_state(state)
        self.assertFalse(any(item["code"] == "reference_cycle" for item in result["errors"]))

    def test_superseded_document_is_allowed_only_as_historical_reference(self) -> None:
        state = empty_state()
        state["evidence"] = [evidence("E-NEW")]
        old_claim = claim("C-OLD", [], status="superseded")
        old_claim["superseded_by"] = "C-NEW"
        new_claim = claim("C-NEW", ["E-NEW"])
        new_claim["historical_document_ids"] = ["D-OLD"]
        state["claims"] = [old_claim, new_claim]
        state["documents"] = [
            {
                "id": "D-OLD",
                "status": "historical",
                "claim_ids": ["C-OLD"],
                "superseded_by": None,
                "invalidates_ids": [],
            }
        ]
        state["active_index"]["claim_ids"] = ["C-NEW"]
        self.assertEqual(CASE_STATE.validate_state(state)["status"], "PASS")

        state["claims"][1]["historical_document_ids"] = []
        state["claims"][1]["document_ids"] = ["D-OLD"]
        result = CASE_STATE.validate_state(state)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any(item["code"] == "superseded_current_source" for item in result["errors"]))


if __name__ == "__main__":
    unittest.main()
