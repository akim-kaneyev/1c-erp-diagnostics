---
name: one-c-erp-final-review
description: Perform scoped Gate 10 review, close only the declared goal when eligible, and keep unresolved linked 1C incidents explicitly open or blocked.
---

# Final review

## Scope first

Before deciding Gate 10, distinguish:

- **current goal/task scope** — what the user asked to complete in this run;
- **linked incident scope** — the underlying accounting, operational or technical incident.

A safety assessment, file comparison or risk decision may be complete while the linked incident remains unresolved. Never call the whole case or incident closed merely because the narrower task is complete.

## Gate status rules

Allowed values are only:

`pending | passed | blocked | failed | stale | not_required`

Do not use decorated statuses such as `passed*` or footnotes that redefine a gate value.

For the current declared goal, every required gate must be `passed` or `not_required`. Any required `pending`, `blocked`, `failed` or `stale` gate prevents closure of that goal.

When diagnosis is explicitly outside a safety-assessment goal, Gate 4 should be `not_required` for the current goal, while the linked incident is recorded as `open` or `blocked`. When diagnosis or correction is part of the goal, a blocked Gate 4 prevents Gate 10 from passing.

## Required final output

1. `Краткий вывод` — result for the current goal and proven cause or explicit uncertainty.
2. `Основание` — decisive evidence, causal chain and Gate 7 result.
3. `Что делать дальше` — safe action or smallest missing evidence.
4. Compact Gate 0–10 status table/list.
5. Remaining blind spots and falsifiers.
6. `Current goal status: closed | blocked | open`.
7. `Linked incident status: resolved | open | blocked | not_in_scope`.

Examples:

- Safety assessment completed, root cause not investigated: `Current goal: closed; linked incident: open`.
- Root-cause diagnosis lacks evidence: `Current goal: blocked; linked incident: blocked`.
- Root cause and correction are verified: `Current goal: closed; linked incident: resolved`.
