---
name: one-c-erp-post-item-expenses
description: Diagnose 1C:ERP post-item expense allocation, unallocated balances, expense analytics and allocation-base mismatches.
---

# Post-item expenses

1. Trace disputed amount to its source document/registrar.
2. Separate expense-article configuration from analytics actually recorded by the document.
3. Identify the allocation base the mechanism should consume.
4. Reconstruct the chronology of when the expense-article setting existed relative to the source movement; a current setting does not prove the historical movement used it.
5. Compare expense and base by the same period, organization and confirmed analytics.
6. Distinguish why the expense arose from why it was not allocated; do not merge separate mechanisms into one cause.
7. Distinguish missing base from mismatched analytics and from a base whose fact/plan rows are controlled by the same predicate.
8. Run the `one-c-erp-diagnose-core` accounting helper over all primary fact/plan/fallback rows and observed allocation. A source count or total from a report is not row coverage.
9. After any correction, independently classify completeness, allocation proportion, analytic key and cardinality, then verify final balance, postings and cost/financial result. A vanished warning with a retained residual is not closure.

Do not claim “incorrect expense article setup” until the exact setting, recorded movement and consuming mechanism are all evidenced.

If `ΣДоля = 1` both before and after but analytic proportions change, state: completeness was not corrected; proportions changed; normative/business justification is required. Static/CFE/build evidence cannot authorize that change.
