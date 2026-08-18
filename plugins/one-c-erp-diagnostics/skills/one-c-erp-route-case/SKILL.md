---
name: one-c-erp-route-case
description: Route a 1C:ERP incident to the correct diagnostic domain by observed symptom, with at most one justified secondary domain.
---

# Route case

Use for Gate 3.

Primary domains:
- `cost-month-close` — cost calculation, deviations, month close, residual cost;
- `post-item-expenses` — expense articles, allocation base, unallocated expenses;
- `settlements` — receivables/payables, advances, offsets, settlement analytics;
- `vat` — VAT registers/books/tax periods/corrections;
- `warehouse-series-assignments` — warehouse, series, assignments, split/negative stock;
- `production` — production chain, stages, materials, output, returns, repair;
- `access-rights` — roles, profiles, access groups, organization restrictions;
- `code-analysis` — supplied 1C code, query/СКД/extension behavior.

Choose from the symptom and evidence, not the user's assumed cause. Add a secondary domain only after naming the concrete intersection.
