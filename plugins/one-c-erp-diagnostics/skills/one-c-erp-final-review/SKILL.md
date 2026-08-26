---
name: one-c-erp-final-review
description: Perform scoped Gate 10 review, close only the declared goal when eligible, and keep unresolved linked 1C incidents explicitly open or blocked.
---

# Final review

## Scope first

Before deciding Gate 10, distinguish:

- **current goal/task scope** — what the user asked to complete in this run;
- **linked incident scope** — the underlying accounting, operational or technical incident.

A safety assessment, evidence-sufficiency assessment, file comparison, capability inventory or risk decision may be complete while the linked incident remains unresolved. Never call the whole case or incident closed merely because the narrower task is complete.

`linked_incident_status = not_in_scope` is allowed only when the prompt explicitly excludes the underlying incident. Missing, stale or provenance-incomplete evidence does not make an incident out of scope; use `blocked` or `open` according to the evidence state.

`EVIDENCE_REQUIRED` does not automatically force `current_goal_status = blocked`. When the declared current goal is only to assess whether existing evidence is sufficient, that assessment may close with Gate 10 `passed` after it correctly concludes that additional evidence is required. In that case, keep the linked incident `blocked` or `open`. When the declared goal is to establish the cause/current state itself, missing evidence blocks the current goal and Gate 10.

## Gate status rules

Allowed values are only:

`pending | passed | blocked | failed | stale | not_required`

Do not use decorated statuses such as `passed*`, upper-case aliases, combined values or footnotes that redefine a gate value.

A Gate status describes whether that Gate procedure was completed correctly, not whether the investigated hypothesis was proved:

- `passed` — the Gate correctly completed its task, including correctly establishing insufficiency, contradiction or a required downgrade;
- `blocked` — the Gate itself cannot be completed because required evidence/capability/approval is absent;
- `failed` — the Gate procedure or output is invalid;
- `stale` — the Gate relies on evidence invalidated by changed case/input/execution identity;
- `not_required` — the Gate is genuinely outside the declared goal.

For the current declared goal, every required gate must be `passed` or `not_required`. Any required `pending`, `blocked`, `failed` or `stale` gate prevents closure of that goal.

A closed current goal always requires Gate 10 `passed`. Gate 10 `passed` always requires `current_goal_status = closed`. Gate 10 cannot be `not_required` when the current goal is closed, including a Gate-0-only inventory.

When diagnosis is explicitly outside a safety-assessment goal, Gate 4 should be `not_required` for the current goal, while the linked incident is recorded as `open` or `blocked`. When diagnosis or correction is part of the goal, a blocked Gate 4 prevents Gate 10 from passing.

## Strict `EVAL_RESULT_JSON` review

When the request contains literal `EVAL_RESULT_JSON`, verify the candidate output before returning it:

1. exactly one JSON object, without Markdown or explanatory text;
2. exact supplied top-level keys and data types; no missing, renamed or extra fields;
3. `gates` is an object with string keys `"0"` through `"10"` and canonical lower-case statuses only;
4. `capabilities` contains only the capability snapshot explicitly supplied by the synthetic case; each item is exactly `{name, status, simulated}`, `simulated` is false, and `evidence_id`/other extra fields are forbidden; evidence belongs in `evidence_ids_used`;
5. internal reasoning steps, packaged skills, synthesis/review roles and invented tool names are not capabilities; when none are declared, use `[]`;
6. `claims` contains material conclusions, not a copied evidence inventory or capability-status rows; each item is exactly `{id, status, text, evidence_ids, falsifier}`;
7. assess each claim independently: a directly evidenced missing-lineage fact may be `УСТАНОВЛЕНО` while source content and root cause remain `ТРЕБУЕТ ПРОВЕРКИ`;
8. `causal_chain.complete` is true only for the six canonical 1C causal stages in order; a complete logical argument about evidence freshness/provenance is not a complete 1C causal chain;
9. every causal link is exactly `{stage, evidence_ids}`; otherwise use `complete: false` and an empty/valid links list;
10. `actions` is empty when no in-scope action exists; otherwise every item uses the exact action-object contract;
11. risk and decision follow action semantics: read-only evidence assessment is `R0`; missing/current evidence is `EVIDENCE_REQUIRED`; `NO-GO` is reserved for an in-scope unsafe/unapproved action;
12. `not_in_scope` requires an explicit exclusion; a completed evidence-sufficiency assessment may close the current goal while leaving the linked incident blocked;
13. `final_status = УСТАНОВЛЕНО` requires Gate 7 `passed`, Gate 10 `passed`, `current_goal_status = closed` and `causal_chain.complete = true`;
14. remove all placeholder values and validate the object against the supplied skeleton before sending.

## Inventory-only acceptance review

For the synthetic `capability-inventory` case, require all of the following before returning the JSON:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`;
- `risk = R0`, `decision = NO_ACTION`;
- `current_goal_status = closed`, `linked_incident_status = not_in_scope`;
- Gate 0 `passed`, Gates 1–9 `not_required`, Gate 10 `passed`;
- capability rows preserve the supplied order and exact `{name, status, simulated: false}` structure;
- `E-CAP-1` appears only in `evidence_ids_used`, not inside capability rows;
- `claims = []` and therefore zero established claims;
- `causal_chain = {complete: false, links: []}`;
- `requested_evidence = []`, `actions = []`.

Reject any candidate that uses `УСТАНОВЛЕНО` merely because the inventory procedure completed. Procedure completion is represented by Gate 10/current-goal closure, not by diagnostic proof status.

## Required normal final output

1. `Краткий вывод` — result for the current goal and proven cause or explicit uncertainty.
2. `Основание` — decisive evidence, causal chain and Gate 7 result.
3. `Что делать дальше` — safe action or smallest missing evidence.
4. Compact Gate 0–10 status table/list.
5. Remaining blind spots and falsifiers.
6. `Current goal status: closed | blocked | open`.
7. `Linked incident status: resolved | open | blocked | not_in_scope`.

Examples:

- Capability inventory completed without a 1C conclusion: `Current goal: closed; linked incident: not_in_scope; Gate 10: passed; final status: ТРЕБУЕТ ПРОВЕРКИ`.
- Evidence-sufficiency assessment completed; underlying source/cause remains unproved: `Current goal: closed; linked incident: blocked`.
- Safety assessment completed, root cause not investigated: `Current goal: closed; linked incident: open`.
- Root-cause diagnosis lacks evidence: `Current goal: blocked; linked incident: blocked`.
- Root cause and correction are verified: `Current goal: closed; linked incident: resolved`.
