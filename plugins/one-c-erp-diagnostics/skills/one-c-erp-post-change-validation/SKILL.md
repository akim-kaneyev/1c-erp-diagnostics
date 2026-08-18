---
name: one-c-erp-post-change-validation
description: Validate a 1C:ERP correction by comparing the same analytics before and after, not merely by disappearance of an error message.
---

# Post-change validation

Use for Gate 9.

Check the same analytic key before/after and verify all relevant outputs: movements, register records, quantities, amounts, balances, postings/subaccounts, month-close result, duplicates/side effects, or access matrix.

If the expected result is not reproduced, reopen the earliest affected gate and mark downstream gates stale. For analysis-only goals, explicitly mark this gate `not_required`.
