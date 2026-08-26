#!/usr/bin/env python3
"""Deterministically validate allocation arithmetic from synthetic/sanitized rows."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1
DATASET_KEYS = {
    "schema_version",
    "dataset_id",
    "evidence_ids",
    "expected_row_ids",
    "rows",
    "observed_allocation",
    "rounding_scale",
}
OBSERVED_KEYS = {"by_analytic", "residual"}
OBSERVED_ROW_KEYS = {"analytic_key", "amount"}
ROW_KEYS = {
    "row_id",
    "group_key",
    "source",
    "kind",
    "analytic_key",
    "fact",
    "plan",
    "quantity_fact",
    "quantity_plan",
    "included",
    "exclusion_reason",
    "exclusion_evidence_ids",
}
DECIMAL_FIELDS = ("fact", "plan", "quantity_fact", "quantity_plan")


@dataclass(frozen=True)
class Row:
    row_id: str
    group_key: str
    source: str
    kind: str
    analytic_key: str
    fact: Decimal
    plan: Decimal
    quantity_fact: Decimal
    quantity_plan: Decimal
    included: bool
    exclusion_reason: str
    exclusion_evidence_ids: tuple[str, ...]


def decimal_text(value: Decimal | Fraction | int) -> str:
    if isinstance(value, Fraction):
        numerator = value.numerator
        denominator = value.denominator
        if denominator == 1:
            return str(numerator)
        twos = 0
        fives = 0
        remaining = denominator
        while remaining % 2 == 0:
            twos += 1
            remaining //= 2
        while remaining % 5 == 0:
            fives += 1
            remaining //= 5
        if remaining != 1:
            return fraction_text(value)
        scale = max(twos, fives)
        scaled = numerator * (2 ** (scale - twos)) * (5 ** (scale - fives))
        sign = "-" if scaled < 0 else ""
        digits = str(abs(scaled)).rjust(scale + 1, "0")
        rendered = digits if scale == 0 else f"{digits[:-scale]}.{digits[-scale:]}"
        rendered = rendered.rstrip("0").rstrip(".")
        return sign + (rendered or "0")
    if isinstance(value, int):
        return str(value)
    if value == 0:
        return "0"
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered


def fraction_text(value: Fraction) -> str:
    """Render an exact rational as a deterministic decimal for human review."""
    return decimal_text(round_fraction(value, 34))


def rational_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def fraction_sum(values: Iterable[Decimal | Fraction | int]) -> Fraction:
    return sum((Fraction(value) for value in values), Fraction(0))


def round_fraction(value: Fraction, scale: int) -> Fraction:
    """Round an exact rational using half-even without ambient Decimal context."""
    factor = 10**scale
    scaled = value * factor
    sign = -1 if scaled < 0 else 1
    quotient, remainder = divmod(abs(scaled.numerator), scaled.denominator)
    doubled = remainder * 2
    if doubled > scaled.denominator or (
        doubled == scaled.denominator and quotient % 2 == 1
    ):
        quotient += 1
    return Fraction(sign * quotient, factor)


def canonical_hash(value: Any) -> str:
    def safe_keys(item: Any) -> Any:
        if isinstance(item, dict):
            return {
                key
                if isinstance(key, str)
                else f"__non_text_key__:{type(key).__name__}:{key!r}": safe_keys(nested)
                for key, nested in item.items()
            }
        if isinstance(item, list):
            return [safe_keys(nested) for nested in item]
        return item

    payload = json.dumps(
        safe_keys(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def invalid_input_fingerprint(value: Any) -> str:
    """Hash malformed raw input without exposing it or conflating Python types."""

    def typed(item: Any, active: set[int]) -> Any:
        item_type = type(item)
        if item is None:
            return {"type": "null"}
        if item_type is bool:
            return {"type": "bool", "value": item}
        if item_type is int:
            return {"type": "int", "value": str(item)}
        if item_type is float:
            return {"type": "float", "value": item.hex()}
        if item_type is str:
            return {"type": "str", "value": item}
        if item_type is Decimal:
            return {"type": "decimal", "value": str(item)}
        if item_type in {bytes, bytearray}:
            raw = bytes(item)
            return {
                "type": item_type.__name__,
                "length": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }

        marker = id(item)
        if item_type in {dict, list, tuple, set, frozenset}:
            if marker in active:
                return {"type": "cycle", "container": item_type.__name__}
            active.add(marker)
            try:
                if item_type is dict:
                    entries = [
                        {"key": typed(key, active), "value": typed(nested, active)}
                        for key, nested in item.items()
                    ]
                    entries.sort(key=canonical_hash)
                    return {"type": "dict", "items": entries}
                values = [typed(nested, active) for nested in item]
                if item_type in {set, frozenset}:
                    values.sort(key=canonical_hash)
                return {"type": item_type.__name__, "items": values}
            finally:
                active.remove(marker)

        python_type = f"{item_type.__module__}.{item_type.__qualname__}"
        try:
            representation = repr(item)
        except Exception:
            representation = "<unavailable>"
        return {
            "type": "unsupported",
            "python_type": python_type,
            "representation_sha256": hashlib.sha256(
                representation.encode("utf-8", errors="backslashreplace")
            ).hexdigest(),
        }

    return canonical_hash(typed(value, set()))


def request_hash(
    dataset_id: str,
    evidence_ids: list[str],
    expected_ids: list[str],
    rows: list[Row],
    rounding_scale: int,
    observed_allocation: dict[str, Decimal],
    observed_residual: Decimal,
    observed_valid: bool,
    allocation_input: Decimal,
    invalid_input_sha256: str | None = None,
) -> str:
    """Hash parsed semantic input, independent of valid transport ordering/formatting."""
    canonical_rows = [
        {
            "row_id": row.row_id,
            "group_key": row.group_key,
            "source": row.source,
            "kind": row.kind,
            "analytic_key": row.analytic_key,
            "fact": decimal_text(row.fact),
            "plan": decimal_text(row.plan),
            "quantity_fact": decimal_text(row.quantity_fact),
            "quantity_plan": decimal_text(row.quantity_plan),
            "included": row.included,
            "exclusion_reason": row.exclusion_reason,
            "exclusion_evidence_ids": sorted(row.exclusion_evidence_ids),
        }
        for row in rows
    ]
    canonical_rows.sort(key=lambda item: (item["row_id"], canonical_hash(item)))
    observed = (
        {
            "status": "available",
            "by_analytic": [
                {
                    "analytic_key": analytic_key,
                    "amount": decimal_text(amount),
                }
                for analytic_key, amount in sorted(observed_allocation.items())
            ],
            "residual": decimal_text(observed_residual),
        }
        if observed_valid
        else {"status": "unavailable_or_invalid"}
    )
    canonical_request = {
        "dataset": {
            "schema_version": SCHEMA_VERSION,
            "dataset_id": dataset_id,
            "evidence_ids": sorted(evidence_ids),
            "expected_row_ids": sorted(expected_ids),
            "rounding_scale": rounding_scale,
            "rows": canonical_rows,
            "observed_allocation": observed,
        },
        "allocation_input": decimal_text(allocation_input),
    }
    if invalid_input_sha256 is not None:
        canonical_request["invalid_input_sha256"] = invalid_input_sha256
    return canonical_hash(canonical_request)


def issue(code: str, message: str, row_ids: Iterable[str] = ()) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "row_ids": sorted(set(row_ids)),
    }


def parse_decimal(value: Any, row_id: str, field: str, errors: list[dict[str, Any]]) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float) or not isinstance(value, (str, int)):
        errors.append(
            issue(
                "invalid_decimal",
                f"{field} must be a decimal string or integer; binary floats are rejected",
                [row_id],
            )
        )
        return Decimal(0)
    try:
        parsed = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        errors.append(issue("invalid_decimal", f"{field} is not a valid decimal", [row_id]))
        return Decimal(0)
    if not parsed.is_finite():
        errors.append(issue("invalid_decimal", f"{field} must be finite", [row_id]))
        return Decimal(0)
    return parsed


def parse_bool(value: Any, row_id: str, errors: list[dict[str, Any]]) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().lower() in {"true", "false"}:
        return value.strip().lower() == "true"
    errors.append(
        issue(
            "unknown_inclusion",
            "included must be explicitly true or false",
            [row_id],
        )
    )
    return False


def nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_evidence_ids(
    value: Any,
    row_id: str,
    errors: list[dict[str, Any]],
) -> tuple[str, ...]:
    if isinstance(value, str):
        values = [item.strip() for item in value.split(";") if item.strip()]
    elif isinstance(value, list) and all(nonempty_text(item) for item in value):
        values = [str(item).strip() for item in value]
    else:
        errors.append(
            issue(
                "invalid_exclusion_evidence",
                "exclusion_evidence_ids must be a JSON list or a semicolon-separated CSV field",
                [row_id],
            )
        )
        return ()
    if len(values) != len(set(values)):
        errors.append(
            issue(
                "invalid_exclusion_evidence",
                "exclusion_evidence_ids must be unique",
                [row_id],
            )
        )
    return tuple(sorted(values))


def parse_observed_allocation(
    payload: Any,
    errors: list[dict[str, Any]],
) -> tuple[dict[str, Decimal], Decimal, bool]:
    error_count = len(errors)
    if not isinstance(payload, dict):
        errors.append(issue("invalid_observed_allocation", "observed_allocation must be an object"))
        return {}, Decimal(0), False
    missing = sorted(OBSERVED_KEYS - set(payload))
    extra = sorted(set(payload) - OBSERVED_KEYS)
    if missing:
        errors.append(issue("invalid_observed_allocation", "missing fields: " + ", ".join(missing)))
    if extra:
        errors.append(issue("invalid_observed_allocation", "unexpected fields: " + ", ".join(extra)))
    raw_rows = payload.get("by_analytic")
    if not isinstance(raw_rows, list):
        errors.append(issue("invalid_observed_allocation", "by_analytic must be a list"))
        raw_rows = []
    result: dict[str, Decimal] = {}
    for index, raw in enumerate(raw_rows):
        row_id = f"observed[{index}]"
        if not isinstance(raw, dict):
            errors.append(issue("invalid_observed_allocation", "observed row must be an object", [row_id]))
            continue
        if set(raw) != OBSERVED_ROW_KEYS:
            errors.append(issue("invalid_observed_allocation", "observed row requires analytic_key and amount only", [row_id]))
        key = raw.get("analytic_key")
        if not nonempty_text(key):
            errors.append(issue("invalid_observed_allocation", "analytic_key must be non-empty text", [row_id]))
            continue
        normalized = str(key).strip()
        if normalized in result:
            errors.append(issue("duplicate_observed_analytic", "observed analytic_key must be unique", [normalized]))
            continue
        result[normalized] = parse_decimal(raw.get("amount"), row_id, "amount", errors)
    residual = parse_decimal(payload.get("residual"), "observed", "residual", errors)
    return result, residual, len(errors) == error_count


def parse_dataset(
    payload: Any,
) -> tuple[
    str,
    list[str],
    list[str],
    list[Row],
    int,
    dict[str, Decimal],
    Decimal,
    bool,
    list[dict[str, Any]],
]:
    errors: list[dict[str, Any]] = []
    if not isinstance(payload, dict):
        return "unknown", [], [], [], 0, {}, Decimal(0), False, [issue("invalid_dataset", "dataset root must be an object")]

    missing_keys = sorted(DATASET_KEYS - set(payload))
    extra_keys = sorted(set(payload) - DATASET_KEYS)
    if missing_keys:
        errors.append(issue("invalid_dataset", "missing dataset fields: " + ", ".join(missing_keys)))
    if extra_keys:
        errors.append(issue("invalid_dataset", "unexpected dataset fields: " + ", ".join(extra_keys)))
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append(issue("invalid_dataset", "schema_version must be 1"))

    dataset_id = payload.get("dataset_id")
    if not nonempty_text(dataset_id):
        errors.append(issue("invalid_dataset", "dataset_id must be non-empty text"))
        dataset_id = "unknown"

    raw_evidence_ids = payload.get("evidence_ids")
    if not isinstance(raw_evidence_ids, list) or not all(
        nonempty_text(item) for item in raw_evidence_ids
    ):
        errors.append(
            issue(
                "invalid_evidence_manifest",
                "evidence_ids must be a list of non-empty strings",
            )
        )
        evidence_ids: list[str] = []
    else:
        evidence_ids = sorted(str(item).strip() for item in raw_evidence_ids)
        duplicate_evidence_ids = sorted(
            {item for item in evidence_ids if evidence_ids.count(item) > 1}
        )
        if duplicate_evidence_ids:
            errors.append(
                issue(
                    "duplicate_evidence_id",
                    "evidence_ids must be unique",
                    duplicate_evidence_ids,
                )
            )
    available_evidence_ids = set(evidence_ids)

    expected = payload.get("expected_row_ids")
    if not isinstance(expected, list) or not all(nonempty_text(item) for item in expected):
        errors.append(issue("invalid_manifest", "expected_row_ids must be a list of non-empty strings"))
        expected_ids: list[str] = []
    else:
        expected_ids = sorted(str(item).strip() for item in expected)
        duplicates = sorted({item for item in expected_ids if expected_ids.count(item) > 1})
        if duplicates:
            errors.append(issue("duplicate_expected_row_id", "expected_row_ids must be unique", duplicates))

    raw_rows = payload.get("rows")
    if not isinstance(raw_rows, list):
        errors.append(issue("invalid_dataset", "rows must be a list"))
        raw_rows = []

    rows: list[Row] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_rows):
        placeholder = f"row[{index}]"
        if not isinstance(raw, dict):
            errors.append(issue("invalid_row", "row must be an object", [placeholder]))
            continue
        non_text_keys = [key for key in raw if not isinstance(key, str)]
        if non_text_keys:
            errors.append(
                issue(
                    "invalid_row",
                    "row contains unnamed or non-text columns",
                    [placeholder],
                )
            )
            raw = {key: value for key, value in raw.items() if isinstance(key, str)}
        raw_id = raw.get("row_id")
        row_id = str(raw_id).strip() if nonempty_text(raw_id) else placeholder
        missing = sorted(ROW_KEYS - set(raw))
        extra = sorted(set(raw) - ROW_KEYS)
        if missing:
            errors.append(issue("invalid_row", "missing row fields: " + ", ".join(missing), [row_id]))
        if extra:
            errors.append(issue("invalid_row", "unexpected row fields: " + ", ".join(extra), [row_id]))
        if not nonempty_text(raw_id):
            errors.append(issue("invalid_row_id", "row_id must be non-empty text", [row_id]))
        if row_id in seen:
            errors.append(issue("duplicate_row_id", "row_id must be unique", [row_id]))
            continue
        seen.add(row_id)

        text_values: dict[str, str] = {}
        for field in ("group_key", "source", "kind", "analytic_key"):
            value = raw.get(field)
            if not nonempty_text(value):
                errors.append(issue("invalid_row", f"{field} must be non-empty text", [row_id]))
                text_values[field] = "unknown"
            else:
                text_values[field] = str(value).strip()

        decimals = {
            field: parse_decimal(raw.get(field), row_id, field, errors)
            for field in DECIMAL_FIELDS
        }
        included = parse_bool(raw.get("included"), row_id, errors)
        exclusion_reason = raw.get("exclusion_reason")
        if not isinstance(exclusion_reason, str):
            errors.append(issue("invalid_row", "exclusion_reason must be text", [row_id]))
            exclusion_reason = ""
        exclusion_reason = exclusion_reason.strip()
        exclusion_evidence_ids = parse_evidence_ids(
            raw.get("exclusion_evidence_ids"), row_id, errors
        )
        if not included and (not exclusion_reason or not exclusion_evidence_ids):
            errors.append(
                issue(
                    "unexplained_exclusion",
                    "excluded row requires a reason and at least one supporting Evidence ID",
                    [row_id],
                )
            )
        if included and (exclusion_reason or exclusion_evidence_ids):
            errors.append(
                issue(
                    "invalid_inclusion",
                    "included row cannot carry exclusion reason or exclusion Evidence IDs",
                    [row_id],
                )
            )
        if set(exclusion_evidence_ids) - available_evidence_ids:
            errors.append(
                issue(
                    "unknown_exclusion_evidence",
                    "excluded row references Evidence IDs absent from the dataset evidence manifest",
                    [row_id],
                )
            )

        rows.append(
            Row(
                row_id=row_id,
                group_key=text_values["group_key"],
                source=text_values["source"],
                kind=text_values["kind"],
                analytic_key=text_values["analytic_key"],
                fact=decimals["fact"],
                plan=decimals["plan"],
                quantity_fact=decimals["quantity_fact"],
                quantity_plan=decimals["quantity_plan"],
                included=included,
                exclusion_reason=exclusion_reason,
                exclusion_evidence_ids=exclusion_evidence_ids,
            )
        )

    present_ids = [row.row_id for row in rows]
    missing_expected = sorted(set(expected_ids) - set(present_ids))
    unexpected = sorted(set(present_ids) - set(expected_ids))
    if missing_expected:
        errors.append(issue("missing_expected_row", "expected rows are absent", missing_expected))
    if unexpected:
        errors.append(issue("unexpected_row", "rows are absent from expected_row_ids", unexpected))
    rounding_scale = payload.get("rounding_scale")
    if isinstance(rounding_scale, bool) or not isinstance(rounding_scale, int) or not 0 <= rounding_scale <= 12:
        errors.append(issue("invalid_rounding_scale", "rounding_scale must be an integer from 0 to 12"))
        rounding_scale = 0

    observed, observed_residual, observed_valid = parse_observed_allocation(
        payload.get("observed_allocation"), errors
    )
    return (
        str(dataset_id),
        evidence_ids,
        expected_ids,
        rows,
        rounding_scale,
        observed,
        observed_residual,
        observed_valid,
        errors,
    )


def summarize(rows: list[Row], key_name: str) -> list[dict[str, Any]]:
    buckets: dict[str, list[Row]] = defaultdict(list)
    for row in rows:
        buckets[str(getattr(row, key_name))].append(row)
    result: list[dict[str, Any]] = []
    for key in sorted(buckets):
        items = buckets[key]
        fact = fraction_sum(row.fact for row in items)
        plan = fraction_sum(row.plan for row in items)
        quantity_fact = fraction_sum(row.quantity_fact for row in items)
        quantity_plan = fraction_sum(row.quantity_plan for row in items)
        result.append(
            {
                key_name: key,
                "row_count": len(items),
                "row_ids": sorted(row.row_id for row in items),
                "fact": decimal_text(fact),
                "plan": decimal_text(plan),
                "amount_delta": decimal_text(fact - plan),
                "quantity_fact": decimal_text(quantity_fact),
                "quantity_plan": decimal_text(quantity_plan),
                "quantity_delta": decimal_text(quantity_fact - quantity_plan),
            }
        )
    return result


def analyze_dataset(payload: Any, allocation_input: Decimal) -> dict[str, Any]:
    if not isinstance(allocation_input, Decimal) or not allocation_input.is_finite():
        raise ValueError("allocation_input must be a finite Decimal")
    (
        dataset_id,
        evidence_ids,
        expected_ids,
        rows,
        rounding_scale,
        observed_allocation,
        observed_residual,
        observed_valid,
        errors,
    ) = parse_dataset(payload)
    invalid_input_sha256 = invalid_input_fingerprint(payload) if errors else None
    included = [row for row in rows if row.included]
    excluded = [row for row in rows if not row.included]

    fact = fraction_sum(row.fact for row in included)
    plan = fraction_sum(row.plan for row in included)
    quantity_fact = fraction_sum(row.quantity_fact for row in included)
    quantity_plan = fraction_sum(row.quantity_plan for row in included)

    analytics = summarize(included, "analytic_key")
    sources = summarize(included, "source")
    groups = summarize(included, "group_key")
    source_counts = []
    for source in sorted({row.source for row in rows}):
        source_rows = [row for row in rows if row.source == source]
        source_counts.append(
            {
                "source": source,
                "row_count": len(source_rows),
                "included_count": sum(row.included for row in source_rows),
                "excluded_count": sum(not row.included for row in source_rows),
                "row_ids": sorted(row.row_id for row in source_rows),
            }
        )

    plan_fraction = plan
    allocation_fraction = Fraction(allocation_input)
    if plan == 0:
        sum_share = Fraction(0)
        errors.append(issue("zero_plan", "total plan is zero; allocation shares are undefined"))
    else:
        sum_share = Fraction(fact) / plan_fraction

    allocation_rows: list[dict[str, Any]] = []
    distributed = Fraction(0)
    for analytic in analytics:
        analytic_fact = Fraction(Decimal(analytic["fact"]))
        share = analytic_fact / plan_fraction if plan != 0 else Fraction(0)
        allocated = allocation_fraction * share
        distributed += allocated
        allocation_rows.append(
            {
                "analytic_key": analytic["analytic_key"],
                "share": fraction_text(share),
                "share_fraction": rational_text(share),
                "allocated": fraction_text(allocated),
                "allocated_fraction": rational_text(allocated),
            }
        )
    residual = allocation_fraction - distributed

    rounded_allocations: dict[str, Fraction] = {}
    for item in allocation_rows:
        exact = Fraction(item["allocated_fraction"])
        rounded_allocations[item["analytic_key"]] = round_fraction(
            exact, rounding_scale
        )
    if sum_share == Fraction(1) and rounded_allocations:
        adjustment_key = sorted(rounded_allocations)[-1]
        adjustment = allocation_fraction - fraction_sum(rounded_allocations.values())
        rounded_allocations[adjustment_key] += adjustment
    expected_residual = allocation_fraction - fraction_sum(rounded_allocations.values())
    for item in allocation_rows:
        item["rounded_allocated"] = decimal_text(
            rounded_allocations[item["analytic_key"]]
        )

    observed_distributed = (
        fraction_sum(observed_allocation.values()) if observed_valid else None
    )
    observed_residual_fraction = Fraction(observed_residual) if observed_valid else None
    expected_analytic_keys = {item["analytic_key"] for item in analytics}
    observed_analytic_keys = set(observed_allocation)
    if observed_valid and expected_analytic_keys != observed_analytic_keys:
        mismatch_rows = {
            row.row_id
            for row in included
            if row.analytic_key in (expected_analytic_keys - observed_analytic_keys)
        }
        mismatch_rows.update(
            f"OBSERVED:{key}"
            for key in (observed_analytic_keys - expected_analytic_keys)
        )
        errors.append(
            issue(
                "observed_analytic_mismatch",
                "observed allocation analytic keys must match included row analytics",
                mismatch_rows,
            )
        )
    for key in sorted(expected_analytic_keys & observed_analytic_keys) if observed_valid else []:
        if Fraction(observed_allocation[key]) != rounded_allocations[key]:
            analytic_row_ids = next(
                item["row_ids"]
                for item in analytics
                if item["analytic_key"] == key
            )
            errors.append(
                issue(
                    "observed_allocation_mismatch",
                    (
                        f"observed allocation for {key} differs from deterministic "
                        f"rounded result {decimal_text(rounded_allocations[key])}"
                    ),
                    analytic_row_ids,
                )
            )
    if observed_valid and observed_residual_fraction != expected_residual:
        errors.append(
            issue(
                "observed_residual_mismatch",
                "observed residual differs from deterministic rounded residual",
            )
        )
    if (
        observed_valid
        and observed_distributed is not None
        and observed_residual_fraction is not None
        and observed_distributed + observed_residual_fraction != allocation_fraction
    ):
        errors.append(
            issue(
                "observed_allocation_imbalance",
                "observed distributed amount plus observed residual must equal allocation input",
            )
        )

    def add_balance_errors(scope: str, items: list[dict[str, Any]]) -> None:
        for item in items:
            key = str(item[scope])
            row_ids = item["row_ids"]
            if Fraction(Decimal(item["amount_delta"])) != 0:
                errors.append(issue(f"{scope}_amount_imbalance", f"{scope} {key} fact and plan differ", row_ids))
            if Fraction(Decimal(item["quantity_delta"])) != 0:
                errors.append(issue(f"{scope}_quantity_imbalance", f"{scope} {key} quantities differ", row_ids))

    if fact != plan:
        errors.append(issue("amount_imbalance", "total fact and plan differ", [row.row_id for row in included]))
    if quantity_fact != quantity_plan:
        errors.append(issue("quantity_imbalance", "total fact and plan quantities differ", [row.row_id for row in included]))
    add_balance_errors("analytic_key", analytics)
    add_balance_errors("group_key", groups)
    if sum_share != Fraction(1):
        errors.append(issue("share_imbalance", "sum of allocation shares is not 1"))
    if residual != Fraction(0):
        errors.append(issue("allocation_residual", "distributed amount plus residual does not close with zero residual"))

    unique_errors: list[dict[str, Any]] = []
    seen_errors: set[str] = set()
    for item in errors:
        marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if marker not in seen_errors:
            seen_errors.add(marker)
            unique_errors.append(item)
    unique_errors.sort(
        key=lambda item: (
            item["code"],
            item["message"],
            tuple(item["row_ids"]),
        )
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if not unique_errors else "FAIL",
        "dataset_id": dataset_id,
        "input_sha256": request_hash(
            dataset_id,
            evidence_ids,
            expected_ids,
            rows,
            rounding_scale,
            observed_allocation,
            observed_residual,
            observed_valid,
            allocation_input,
            invalid_input_sha256,
        ),
        "row_coverage": {
            "evidence_ids": evidence_ids,
            "expected_row_ids": expected_ids,
            "present_row_ids": sorted(row.row_id for row in rows),
            "included_row_ids": sorted(row.row_id for row in included),
            "excluded_rows": [
                {
                    "row_id": row.row_id,
                    "reason": row.exclusion_reason,
                    "evidence_ids": list(row.exclusion_evidence_ids),
                }
                for row in sorted(excluded, key=lambda item: item.row_id)
            ],
            "source_counts": source_counts,
            "expected_count": len(expected_ids),
            "present_count": len(rows),
            "included_count": len(included),
            "excluded_count": len(excluded),
        },
        "totals": {
            "fact": decimal_text(fact),
            "plan": decimal_text(plan),
            "amount_delta": decimal_text(fact - plan),
            "quantity_fact": decimal_text(quantity_fact),
            "quantity_plan": decimal_text(quantity_plan),
            "quantity_delta": decimal_text(quantity_fact - quantity_plan),
            "sum_share": fraction_text(sum_share),
            "sum_share_fraction": rational_text(sum_share),
            "allocation_input": decimal_text(allocation_input),
            "distributed": fraction_text(distributed),
            "distributed_fraction": rational_text(distributed),
            "residual": fraction_text(residual),
            "residual_fraction": rational_text(residual),
            "observed_distributed": (
                decimal_text(observed_distributed) if observed_distributed is not None else None
            ),
            "observed_residual": decimal_text(observed_residual) if observed_valid else None,
            "rounding_scale": rounding_scale,
        },
        "reconciliation": {
            "group_keys": groups,
            "sources": sources,
            "analytics": analytics,
        },
        "allocation": allocation_rows,
        "observed_allocation": {
            "status": "available" if observed_valid else "unavailable",
            "by_analytic": [
                {"analytic_key": key, "amount": decimal_text(observed_allocation[key])}
                for key in sorted(observed_allocation)
            ] if observed_valid else [],
            "residual": decimal_text(observed_residual) if observed_valid else None,
        },
        "formula_trace": [
            {
                "formula_id": "totals",
                "operator": "sum included rows",
                "row_ids": sorted(row.row_id for row in included),
                "operands": {
                    "fact": [decimal_text(row.fact) for row in sorted(included, key=lambda item: item.row_id)],
                    "plan": [decimal_text(row.plan) for row in sorted(included, key=lambda item: item.row_id)],
                },
                "result": {"fact": decimal_text(fact), "plan": decimal_text(plan)},
            },
            *[
                {
                    "formula_id": f"allocation:{item['analytic_key']}",
                    "operator": "analytic fact / total plan * allocation input (exact rational)",
                    "row_ids": next(
                        analytic["row_ids"]
                        for analytic in analytics
                        if analytic["analytic_key"] == item["analytic_key"]
                    ),
                    "operands": {
                        "total_plan": decimal_text(plan),
                        "allocation_input": decimal_text(allocation_input),
                    },
                    "result": {
                        "share_fraction": item["share_fraction"],
                        "allocated_fraction": item["allocated_fraction"],
                        "rounded_allocated": item["rounded_allocated"],
                    },
                }
                for item in allocation_rows
            ],
            *[
                {
                    "formula_id": "observed-balance",
                    "operator": "observed distributed + observed residual = allocation input",
                    "row_ids": sorted(row.row_id for row in included),
                    "operands": {
                        "observed_distributed": decimal_text(observed_distributed),
                        "observed_residual": decimal_text(observed_residual),
                    },
                    "result": decimal_text(observed_distributed + observed_residual_fraction),
                }
                for _ in [None]
                if observed_valid
                and observed_distributed is not None
                and observed_residual_fraction is not None
            ],
        ],
        "errors": unique_errors,
    }


def result_map(result: dict[str, Any], section: str, key: str) -> dict[str, dict[str, Any]]:
    return {str(item[key]): item for item in result["reconciliation"][section]}


def row_analytic_assignment(result: dict[str, Any]) -> dict[str, str]:
    return {
        str(row_id): str(item["analytic_key"])
        for item in result["reconciliation"]["analytics"]
        for row_id in item["row_ids"]
    }


def compare_datasets(before_payload: Any, after_payload: Any, allocation_input: Decimal) -> dict[str, Any]:
    before = analyze_dataset(before_payload, allocation_input)
    after = analyze_dataset(after_payload, allocation_input)
    errors: list[dict[str, Any]] = []
    if before["status"] != "PASS":
        errors.append(issue("before_failed", "before dataset failed accounting invariants"))
    if after["status"] != "PASS":
        errors.append(issue("after_failed", "after dataset failed accounting invariants"))

    before_analytics = result_map(before, "analytics", "analytic_key")
    after_analytics = result_map(after, "analytics", "analytic_key")
    before_shares = {
        item["analytic_key"]: item["share_fraction"] for item in before["allocation"]
    }
    after_shares = {
        item["analytic_key"]: item["share_fraction"] for item in after["allocation"]
    }

    before_complete = (
        before["status"] == "PASS"
        and before["totals"]["amount_delta"] == "0"
        and before["totals"]["quantity_delta"] == "0"
        and before["totals"]["sum_share"] == "1"
        and before["totals"]["residual"] == "0"
    )
    after_complete = (
        after["status"] == "PASS"
        and after["totals"]["amount_delta"] == "0"
        and after["totals"]["quantity_delta"] == "0"
        and after["totals"]["sum_share"] == "1"
        and after["totals"]["residual"] == "0"
    )
    completeness_changed = before_complete != after_complete
    analytic_key_changed = (
        row_analytic_assignment(before) != row_analytic_assignment(after)
    )
    allocation_proportion_changed = before_shares != after_shares
    cardinality_changed = (
        before["row_coverage"]["included_count"] != after["row_coverage"]["included_count"]
        or {key: item["row_count"] for key, item in before_analytics.items()}
        != {key: item["row_count"] for key, item in after_analytics.items()}
    )
    totals_changed = any(
        before["totals"][field] != after["totals"][field]
        for field in ("fact", "plan", "quantity_fact", "quantity_plan", "distributed", "residual")
    )
    no_material_change = not any(
        (
            completeness_changed,
            allocation_proportion_changed,
            analytic_key_changed,
            cardinality_changed,
            totals_changed,
        )
    )
    changed_metrics = [
        name
        for name, changed in (
            ("completeness", completeness_changed),
            ("allocation_proportion", allocation_proportion_changed),
            ("analytic_key", analytic_key_changed),
            ("cardinality", cardinality_changed),
            ("totals", totals_changed),
        )
        if changed
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if not errors else "FAIL",
        "before": before,
        "after": after,
        "effect": {
            "completeness_changed": completeness_changed,
            "allocation_proportion_changed": allocation_proportion_changed,
            "analytic_key_changed": analytic_key_changed,
            "cardinality_changed": cardinality_changed,
            "no_material_change": no_material_change,
        "business_basis_required": (
                before_complete
                and after_complete
                and (allocation_proportion_changed or analytic_key_changed)
            ),
            "changed_metrics": changed_metrics,
        },
        "errors": errors,
    }


def manifest_value(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_ids(path: Path) -> list[str]:
    value = manifest_value(path)
    if isinstance(value, dict):
        value = value.get("expected_row_ids")
    if not isinstance(value, list) or not all(nonempty_text(item) for item in value):
        raise ValueError("manifest must be a JSON list or object with expected_row_ids")
    return [str(item).strip() for item in value]


def load_dataset(path: Path, manifest: Path | None = None) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("JSON dataset root must be an object")
        return value
    if path.suffix.lower() != ".csv":
        raise ValueError("input must be .json or .csv")
    if manifest is None:
        raise ValueError("CSV input requires --manifest with expected row IDs")
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    manifest_payload = manifest_value(manifest)
    observed_allocation = (
        manifest_payload.get("observed_allocation")
        if isinstance(manifest_payload, dict)
        else None
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "dataset_id": path.stem,
        "evidence_ids": (
            manifest_payload.get("evidence_ids")
            if isinstance(manifest_payload, dict)
            else None
        ),
        "expected_row_ids": manifest_ids(manifest),
        "rows": rows,
        "observed_allocation": observed_allocation,
        "rounding_scale": (
            manifest_payload.get("rounding_scale")
            if isinstance(manifest_payload, dict)
            else None
        ),
    }


def allocation_decimal(value: str) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("allocation input must be a decimal") from exc
    if not parsed.is_finite():
        raise argparse.ArgumentTypeError("allocation input must be finite")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Validate one row set")
    analyze.add_argument("input", type=Path)
    analyze.add_argument("--manifest", type=Path)
    analyze.add_argument("--allocation-input", type=allocation_decimal, required=True)
    analyze.add_argument("--output", type=Path)

    compare = subparsers.add_parser("compare", help="Classify before/after effect")
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    compare.add_argument("--before-manifest", type=Path)
    compare.add_argument("--after-manifest", type=Path)
    compare.add_argument("--allocation-input", type=allocation_decimal, required=True)
    compare.add_argument("--output", type=Path)
    return parser


def write_result(result: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "analyze":
            result = analyze_dataset(
                load_dataset(args.input, args.manifest),
                args.allocation_input,
            )
        else:
            result = compare_datasets(
                load_dataset(args.before, args.before_manifest),
                load_dataset(args.after, args.after_manifest),
                args.allocation_input,
            )
    except (OSError, ValueError, json.JSONDecodeError, csv.Error):
        result = {
            "schema_version": SCHEMA_VERSION,
            "status": "FAIL",
            "errors": [
                issue(
                    "input_error",
                    "input could not be read or parsed; path and content are suppressed",
                )
            ],
        }
    write_result(result, args.output)
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
