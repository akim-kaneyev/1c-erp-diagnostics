"""Bounded deterministic checks, never an accounting diagnosis."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from fractions import Fraction
import json

from workbench_common import ACCOUNTING, exact, public_json, require, text

LIMITATIONS = ["Результат относится только к переданным строкам и аналитическим ключам.",
               "Полнота выгрузки и экономический смысл требуют независимой сверки. Причина инцидента не установлена."]


def decimal(value):
    require(type(value) in (str, int), "decimal_string_required")
    require(len(str(value)) <= 80, "invalid_decimal")
    try:
        result = Decimal(str(value))
    except InvalidOperation:
        require(False, "invalid_decimal")
    require(result.is_finite(), "invalid_decimal")
    # Bound both magnitude and scale before Fraction can allocate a huge power of ten.
    require(-80 <= result.as_tuple().exponent <= 80 and result.copy_abs() <= Decimal("1e20"), "invalid_decimal")
    return Fraction(result)


def fields(value):
    require(isinstance(value, list) and 1 <= len(value) <= 12, "invalid_fields")
    result = [text(item, 80) for item in value]
    require(len(result) == len(set(result)), "duplicate_field")
    return result


def rows(value, keys, required=()):
    require(isinstance(value, list) and len(value) <= 1000, "row_limit")
    result = {}
    for row in value:
        require(isinstance(row, dict) and set(keys) | set(required) <= set(row) and len(row) <= 30, "invalid_row")
        require(all(item is None or type(item) in (str, int, bool) for item in row.values()), "scalar_rows_required")
        require(all(not isinstance(item, str) or len(item) <= 500 for item in row.values()), "cell_limit")
        require(all(row[key] is not None and str(row[key]).strip() for key in keys), "analytic_key_required")
        identity = json.dumps([row[key] for key in keys], ensure_ascii=False, separators=(",", ":"))
        require(identity not in result, "ambiguous_duplicate_key")
        result[identity] = row
    return result


def compare(payload):
    exact(payload, {"key_fields", "value_fields", "left", "right"}, {"numeric_fields"})
    keys, values = fields(payload["key_fields"]), fields(payload["value_fields"])
    require(not set(keys) & set(values), "key_value_overlap")
    numeric = payload.get("numeric_fields", [])
    require(isinstance(numeric, list) and set(numeric) <= set(values) and len(set(numeric)) == len(numeric), "invalid_numeric_fields")
    left, right = rows(payload["left"], keys, values), rows(payload["right"], keys, values)
    changes = []
    total = 0
    for key in sorted(set(left) | set(right)):
        if key not in left or key not in right:
            items = [{"key": json.loads(key), "kind": "added" if key not in left else "removed"}]
        else:
            items = []
            for field in values:
                a, b = left[key][field], right[key][field]
                different = decimal(a) != decimal(b) if field in numeric else type(a) is not type(b) or a != b
                if different:
                    items.append({"key": json.loads(key), "kind": "changed", "field": field, "left": a, "right": b})
        total += len(items)
        changes.extend(items[:max(0, 2000 - len(changes))])
    return {"validation_status": "PASS", "observation": "differences_found" if total else "no_differences_in_supplied_rows",
            "left_rows": len(left), "right_rows": len(right), "difference_count": total,
            "differences": changes, "truncated": total > len(changes), "limitations": list(LIMITATIONS)}


def negative_stock(payload):
    exact(payload, {"key_fields", "rows"})
    keys = fields(payload["key_fields"])
    source = rows(payload["rows"], keys, ["quantity"])
    negative = [row for row in source.values() if decimal(row["quantity"]) < 0]
    return {"validation_status": "PASS", "observation": "negative_rows_found" if negative else "no_negative_rows_in_supplied_data",
            "checked_rows": len(source), "negative_count": len(negative), "negative_rows": negative, "limitations": list(LIMITATIONS)}


def allocation(payload):
    exact(payload, {"dataset", "allocation_input"})
    require(isinstance(payload["dataset"], dict) and isinstance(payload["dataset"].get("rows"), list)
            and len(payload["dataset"]["rows"]) <= 1000, "row_limit")
    decimal(payload["allocation_input"])
    dataset = payload["dataset"]
    for row in dataset["rows"]:
        require(isinstance(row, dict), "invalid_row")
        for field in ACCOUNTING.DECIMAL_FIELDS:
            if field in row:
                decimal(row[field])
    observed = dataset.get("observed_allocation")
    if isinstance(observed, dict):
        if "residual" in observed:
            decimal(observed["residual"])
        observed_rows = observed.get("by_analytic", [])
        require(isinstance(observed_rows, list) and len(observed_rows) <= 1000, "row_limit")
        for row in observed_rows:
            require(isinstance(row, dict), "invalid_row")
            if "amount" in row:
                decimal(row["amount"])
    result = ACCOUNTING.analyze_dataset(payload["dataset"], Decimal(str(payload["allocation_input"])))
    return {"validation_status": result["status"], "observation": "arithmetic_only",
            "accounting_invariants": result, "limitations": list(LIMITATIONS)}


SCENARIOS = {"compare": compare, "negative-stock": negative_stock, "allocation": allocation}


def execute(scenario, payload):
    require(scenario in SCENARIOS, "unknown_scenario")
    public_json(payload)
    result = SCENARIOS[scenario](payload)
    public_json(result)
    return result


def examples():
    dataset = {"schema_version": 1, "dataset_id": "synthetic-allocation", "evidence_ids": [],
               "expected_row_ids": ["R-A", "R-B"], "rounding_scale": 2,
               "rows": [{"row_id": "R-" + key, "group_key": "G", "source": "synthetic", "kind": "fact_plan",
                         "analytic_key": key, "fact": amount, "plan": amount, "quantity_fact": "0", "quantity_plan": "0",
                         "included": True, "exclusion_reason": "", "exclusion_evidence_ids": []} for key, amount in (("A", "100"), ("B", "900"))],
               "observed_allocation": {"by_analytic": [{"analytic_key": "A", "amount": "11"}, {"analytic_key": "B", "amount": "99"}], "residual": "0"}}
    return {"compare": {"key_fields": ["item", "warehouse"], "value_fields": ["quantity"], "numeric_fields": ["quantity"],
                        "left": [{"item": "Учебный товар", "warehouse": "Учебный склад", "quantity": "10"}],
                        "right": [{"item": "Учебный товар", "warehouse": "Учебный склад", "quantity": "9"}]},
            "negative-stock": {"key_fields": ["item", "warehouse", "series"], "rows": [
                {"item": "Учебный товар", "warehouse": "Учебный склад", "series": "Серия 1", "quantity": "-2"}]},
            "allocation": {"dataset": dataset, "allocation_input": "110"}}
