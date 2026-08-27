# Accounting invariants interface

This reference defines the executable arithmetic gate used by `one-c-erp-diagnose-core`.
It controls row coverage and allocation arithmetic; it does not establish 1C metadata,
business meaning or the six-stage causal chain.

## Input

Use only synthetic or sanitized `.json`/`.csv` rows. JSON has exactly:

```json
{
  "schema_version": 1,
  "dataset_id": "stable-dataset-id",
  "evidence_ids": [],
  "expected_row_ids": ["R-1"],
  "rounding_scale": 2,
  "rows": [
    {
      "row_id": "R-1",
      "group_key": "G-1",
      "source": "S-1",
      "kind": "fact",
      "analytic_key": "A-1",
      "fact": "100",
      "plan": "100",
      "quantity_fact": "0",
      "quantity_plan": "0",
      "included": true,
      "exclusion_reason": "",
      "exclusion_evidence_ids": []
    }
  ],
  "observed_allocation": {
    "by_analytic": [{"analytic_key": "A-1", "amount": "110"}],
    "residual": "0"
  }
}
```

Every source row needs a stable `row_id` and an explicit `included` flag. An excluded
row requires both a reason and supporting IDs that exist in the top-level
`evidence_ids` manifest. A non-empty but unknown ID is `FAIL`. CSV uses the same row
columns; `exclusion_evidence_ids` is semicolon-separated, and its JSON manifest
contains `evidence_ids`, `expected_row_ids`, `rounding_scale` and
`observed_allocation`. Financial inputs are decimal strings or integers; binary JSON
floats are rejected. Totals, human-readable fraction rendering and rounding are exact
rationals and do not depend on process-wide Decimal precision, rounding mode or traps.

`observed_allocation` is required so that `distributed + residual = input` checks an
observed result rather than a residual invented by subtraction. The helper compares
every observed analytic amount with its deterministic calculated allocation. It uses
exact rational division internally, then `ROUND_HALF_EVEN` at `rounding_scale`; any
rounding adjustment is assigned deterministically to the last sorted analytic key.
When observed allocation is missing or malformed, the result is `FAIL`, its
`observed_allocation.status` is `unavailable`, observed totals/residual are `null`, and
the observed-balance formula is omitted. Calculated allocation remains visible but is
never materialized as observed Evidence.

## Commands

Run one deterministic balance:

```text
python scripts/accounting_invariants.py analyze rows.json --allocation-input 110
```

Classify a proposed change:

```text
python scripts/accounting_invariants.py compare before.json after.json --allocation-input 110
```

Exit `0` means the requested calculation completed with all invariants passing. Exit
`1` means invalid input, missing/unknown row coverage, amount/quantity imbalance,
per-key reconciliation failure, observed-vs-calculated allocation mismatch, non-unit
share or non-zero observed allocation balance. CLI usage errors use the standard
argparse exit `2`.

## Output contract

`analyze` returns row coverage, `ΣФакт`, `ΣПлан`, quantity totals, `ΣДоля`,
`distributed + residual = input`, source/group/analytic reconciliation, allocations,
formula trace with contributing row IDs, exact fraction fields, rounded allocations and
non-secret error objects. The request hash covers both the dataset and allocation input
and ignores transport ordering and equivalent valid decimal representations. If a
decoded payload reaches dataset validation but fails it, the hash also covers a
type-tagged SHA-256 fingerprint of that invalid value so distinct invalid values cannot
collapse to the same request identity; neither that fingerprint nor the raw value is
emitted. JSON/CSV decoding failures occur before a request identity can be constructed
and therefore return a controlled error without `input_sha256`. `compare` embeds both
analyses and returns:

- `completeness_changed`;
- `allocation_proportion_changed`;
- `analytic_key_changed`;
- `cardinality_changed`;
- `no_material_change`.

`analytic_key_changed` compares each stable `row_id → analytic_key` assignment, not
only the set of names. When completeness stays valid but proportions or a row's
analytic assignment change, `business_basis_required=true`. This is a classification,
not approval. Gate 7 must still verify business semantics and Gate 9 must verify actual
accounting results.

## Stop rules

- A missing expected row, unknown inclusion or unexplained exclusion is `FAIL`.
- A manually copied total cannot replace this result.
- Build/load/activate is blocked until the baseline and proposed result pass and Gate 7
  accepts the analytic meaning independently.
- A lower-level structural/static/CFE pass never upgrades this arithmetic result.
