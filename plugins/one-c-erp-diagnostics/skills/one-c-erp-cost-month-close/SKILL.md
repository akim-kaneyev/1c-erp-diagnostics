---
name: one-c-erp-cost-month-close
description: Diagnose 1C:ERP cost calculation, cost deviations and month-close incidents from evidence, including registrar tracing and before/after validation.
---

# Cost and month close

Use when the observed symptom is cost, month-close error, cost deviation, residual amount, or a result that changes after recalculation.

Required method:
1. Fix period, organization and symptom before repost/reclose.
2. Drill the amount/quantity to registrar.
3. Compare problem/control on identical analytics.
4. Separate source movements from close-generated movements.
5. Prove which calculation consumes the disputed record.
6. Validate final balances/postings, not only the close UI message.

Stop with `ТРЕБУЕТ ПРОВЕРКИ` if the amount is not drilled to registrar, key movements are missing, consuming mechanism is unproven, or validation only shows disappearance of an error message.
