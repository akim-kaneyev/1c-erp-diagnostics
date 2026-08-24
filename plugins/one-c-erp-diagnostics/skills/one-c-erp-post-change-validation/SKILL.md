---
name: one-c-erp-post-change-validation
description: Validate a 1C:ERP correction by comparing the same analytics before and after, not merely by disappearance of an error message.
---

# Post-change validation

Use for Gate 9.

## Validation ladder

Select every level required by the change and record the evidence produced at each level:

1. **Structural/syntax** — the artifact, query, schema or source can be parsed and referenced identifiers are proven rather than invented.
2. **Static** — applicable lint/static-analysis checks; findings are hypotheses, not proof of runtime behavior.
3. **Metadata/runtime** — relevant 1C metadata/build/compile/runtime behavior is actually exercised when the result depends on execution.
4. **Functional** — reproduce the target user or process scenario and its expected observable result.
5. **Business/accounting** — compare identical analytics before/after and verify the relevant movements, register records, quantities, amounts, balances, postings/subaccounts, month-close result, duplicates/side effects, or access matrix.

Passing a lower validation level never substitutes for a required higher level. In particular, clean syntax, static analysis or a successful build cannot prove that a 1C business/accounting defect is corrected.

If a required runtime or business validation cannot be performed, mark Gate 9 `blocked` rather than treating the producer's self-report, disappearance of an interface error, or a lower-level check as proof.

If the expected result is not reproduced, reopen the earliest affected gate and mark downstream gates stale. Record where the mismatch first became observable so the missed control can be converted into a regression case or checklist improvement.

For analysis-only goals, explicitly mark this gate `not_required`.
