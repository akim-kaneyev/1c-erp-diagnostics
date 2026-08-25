---
name: one-c-erp-diagnostics
description: Run the dynamic evidence-first Gate 0-10 workflow and verified companion ecosystem for 1C:ERP incidents, comparisons, code, releases, access rights and safe remediation.
user-invocable: true
argument-hint: "[case path or task description]"
---

# 1C ERP Diagnostics — Dynamic Gate 0–10 Orchestrator

## Single entrypoint

`$one-c-erp-diagnostics <case path or task>`

The user invokes one command. The orchestrator discovers capabilities, selects internal specialist skills and installed companion plugins, runs verification and reports one consolidated result. Never require the user to manually chain skills.

The orchestrator is a provider-neutral harness around the available model. Correctness comes from explicit instructions, evidence coverage, artifact/provenance closure, capability/tool provenance, execution identity, an inspect → hypothesize → test → compare loop and independent validation. Model/provider identity or confidence is runtime provenance, never proof.

## Strict `EVAL_RESULT_JSON` mode

When the request contains literal `EVAL_RESULT_JSON`, the normal narrative response is prohibited and the following protocol is mandatory:

1. Return exactly one JSON object without Markdown, code fences, preamble, commentary or trailing text.
2. If the prompt supplies a skeleton, preserve the exact top-level keys, nested data types and field names. Do not add, omit or rename fields.
3. `gates` is one object with string keys `"0"` through `"10"`. Allowed values are only `pending | passed | blocked | failed | stale | not_required`, exactly in lower case.
4. Gate status describes whether that Gate procedure completed correctly, not whether the investigated hypothesis was proved:
   - `passed` — the Gate correctly completed its task, including correctly establishing insufficiency, contradiction, rejection or downgrade;
   - `blocked` — the Gate itself cannot be completed because required evidence, capability or approval is absent;
   - `failed` — the Gate procedure/output is invalid;
   - `stale` — the Gate depends on evidence invalidated by changed case/input/execution identity;
   - `not_required` — genuinely outside the declared goal.
5. `risk` classifies the blast radius of the actual/proposed action, never evidentiary severity. Read-only reasoning, comparison or refusal to reuse stale evidence is `R0`. `R3` requires an in-scope production/accounting/access/closed-period/configuration/external write.
6. Decision values have distinct meanings:
   - `EVIDENCE_REQUIRED` — the requested conclusion/current state needs additional current evidence, rerun or proved equivalence;
   - `NO-GO` — an actual in-scope action is unsafe, prohibited, unapproved or missing mandatory controls;
   - `NO_ACTION` — the declared goal is complete without action or additional evidence;
   - `GO` — a specifically scoped action is authorized by the applicable risk gate.
7. `linked_incident_status = not_in_scope` only when the prompt explicitly excludes the underlying incident. Missing or stale evidence means `blocked` or `open`, not `not_in_scope`.
8. `claims` contains material conclusions, not copied Evidence summaries. Each item is exactly `{id, status, text, evidence_ids, falsifier}`. Do not use `claim` instead of `id`/`text`; do not omit `falsifier`; do not create trivial `УСТАНОВЛЕНО` claims merely by restating input identities.
9. `causal_chain.complete = true` only when all six canonical 1C causal stages are evidenced in order: `document`, `movement`, `record_register`, `consuming_mechanism`, `accounting_stock_access_result`, `symptom`. A complete logical argument about provenance or stale evidence is not a complete 1C causal chain. Each link is exactly `{stage, evidence_ids}`. Otherwise use `complete: false` and an empty or schema-valid links list.
10. If no actual/proposed in-scope action exists, `actions` must be `[]`. If present, each action is exactly `{description, risk, approved, executed, approval_reference, rollback, validation}`.
11. Remove every placeholder, verify all required fields and validate the final object against the supplied skeleton before sending.

## Gate 0 — Capability and state discovery

1. Read `AGENTS.md`, `docs/ECOSYSTEM_MARKETPLACE.md` and existing `STATE.md`.
2. Inventory only capabilities actually exposed in the current host/session.
3. Check the canonical marketplace companions by exact identity: `unica`, `1c-skills`, `1c-skills-py`.
4. Inventory relevant host capabilities such as PDF, Spreadsheets, Documents, GitHub, Drive, Computer Use, OpenSandbox and optional `sonarqube-bsl-local`. For SonarQube, do not classify from named-tool inventory: when local execution and loopback HTTP exist, apply `one-c-erp-local-static-analysis` and run its read-only server/scanner preflight.
5. Classify each capability as `available`, `confirmation_required`, `unavailable` or `prohibited`.
6. Record version/ref when exposed, permissions, write-risk, provenance and exact purpose. Model/provider identity is provenance only.
7. Continue from the earliest `pending`, `blocked`, `failed` or `stale` gate.

Marketplace presence does not prove runtime availability. A failed public-plugin/dependency resolver lookup does not prove that a selected skills-first custom-marketplace plugin is uninstalled; report only what that resolver actually established. Missing required capability becomes documented fallback or `blocked`, never simulated output. A Gate 0 inventory can pass even when optional capabilities are unavailable, provided their status and consequences are recorded honestly.

## Gate 1 — Goal contract

Define concrete outcome, scope, completion evidence, exclusions and stop condition. Separate the **current goal/task scope** from the **linked incident scope** whenever the underlying 1C incident is broader. Do not describe the incident itself as closed merely because a narrower assessment is complete.

## Gate 2 — Evidence intake

Inventory all files, screenshots, reports, movements, register records, postings, code and official sources. State what each proves and cannot prove. Preserve identifiers and hashes when possible.

Every supplied source/attachment receives an Evidence ID and disposition: `examined`, `unreadable`, `duplicate`, `irrelevant_with_reason` or `blocked`. Gate 2 cannot pass while supplied evidence is unaccounted for. Keep supplied-but-unexamined evidence separate from expected-but-missing evidence.

For every derived artifact produced by extraction, filtering, normalization, joining, comparison, parser/export or similar transformation, record its parent Evidence ID(s), transformation, tool/version/ref, execution `run_id` when applicable, and output hash/identifier. A material derived result with no traceable parent/derivation is provenance-incomplete and cannot independently support final `УСТАНОВЛЕНО`.

A final `УСТАНОВЛЕНО` is forbidden when material supplied evidence remains unreadable/blocked and could falsify the conclusion, or when a material derivation chain is broken. Gate 2 may still pass when every supplied item is accounted for and the missing primary source is explicitly recorded as expected-but-missing evidence.

## Gate 3 — Dynamic execution graph

Choose one primary domain and no more than two justified secondary domains. Build a directed graph containing specialist objective, evidence inputs/analytic keys, dependencies, exact skill/capability, R0–R3 risk, output schema/provenance, required validation level, independent acceptance evidence, stop/falsification condition and fallback.

Validation levels: `structural → static → metadata_runtime → functional → business_accounting`. Define independent validation before execution. A lower level cannot substitute for a required higher level. Normally use no more than four active specialist nodes without explicit dependency justification.

## Gate 4 — Specialist analysis

Each specialist separates facts, interpretations, hypotheses and missing evidence. Core causal chain:

`document → movement → record/register → consuming mechanism → accounting/stock/access result → symptom`

The earliest proven divergence matters more than the last visible symptom. Code/tool findings remain hypotheses until linked to the factual case chain.

For every external companion output record canonical identity, assigned operation, evidence inputs, version/ref, execution identity when applicable, output location/hash, limitations and whether another method reproduced the material result.

If diagnosis is outside the current goal, Gate 4 may be `not_required`; keep the linked incident separately `open`/`blocked`. Do not use decorated statuses such as `passed*`.

## Gate 5 — Executable validation and sandbox decision

Use local tools, `1c-skills`, `1c-skills-py`, Unica runtime, OpenSandbox or `one-c-erp-local-static-analysis` only when executable validation adds measurable value. Default to read-only and sanitized inputs.

Every executable result relied on later must have an execution identity: unique `run_id`, current `case_id`, input Evidence IDs and hashes/stable identifiers, tool/runtime version/ref, operation without secrets, timestamps when exposed, output hash/identifier, status and limitations.

Before reusing an earlier result, compare its case/input identities with current evidence. A result from another case, mismatched input, or execution preceding a material input change is `stale`; rerun it or prove deterministic equivalence. Never silently promote stale output into current evidence. In an eval where the current conclusion depends on that mismatched report, Gate 5 is `stale`, not a custom value such as `REJECT_CURRENT_STATE_USE`.

Use SonarQube only after factual Gate 0 preflight; keep credentials in child-process environment only. If required execution is unavailable, mark the gate `blocked`; never simulate it.

## Gate 6 — Evidence synthesis

Merge specialist outputs by source, evidence and claim ID. Preserve support, contradictions, capability provenance and falsifiers. Resolve contradictions by evidence, not majority vote.

For every material claim record provenance closure `closed | open | broken` and trace:

`source artifact → inspected/derived evidence → claim premise → causal link → conclusion`.

A list of evidence IDs is not sufficient if a transition is merely inferred. Preliminary `УСТАНОВЛЕНО` requires a complete causal chain and closed provenance for every material causal link. Gate 6 may pass when synthesis correctly concludes that the cause/current state remains `ТРЕБУЕТ ПРОВЕРКИ`.

Use only `УСТАНОВЛЕНО`, `ВЕРОЯТНО`, `ТРЕБУЕТ ПРОВЕРКИ`.

## Gate 7 — Adversarial verification

A distinct reviewer re-reads original evidence, not only synthesis. It challenges every causal link, checks identical analytics, searches for earlier divergence, tests alternatives, identifies invented objects and records a falsifier. It confirms evidence coverage, provenance closure and execution freshness for every relied-upon tool result.

A label such as `critical`, `high`, `blocking` or a confident agent verdict is not proof. Convert each finding into a testable claim and reproduce/evidence-link it. Absence of findings is not proof either.

Final `УСТАНОВЛЕНО` is forbidden if Gate 7 is unavailable/fails, if material provenance is open/broken, or if relied-upon executable evidence has mismatched/stale execution identity. Gate 7 is `passed` when it correctly rejects an unsupported conclusion or stale-evidence reuse.

## Gate 8 — Risk-controlled action decision

Classify action: `R0` read-only; `R1` derived local artifact/report; `R2` reversible test-environment change; `R3` production/accounting/access/closed periods/broad reposting.

Risk describes the action surface, not the seriousness of uncertainty. A read-only decision not to trust `R-OLD` remains `R0`. Missing current evidence normally leads to `EVIDENCE_REQUIRED`; `NO-GO` is reserved for an actual unsafe/unapproved in-scope action.

R3 requires explicit approval, tested rollback, affected scope and post-change validation. Prefer standard 1C settings/NSI, standard documents/mechanisms, then correction of actual source document in an allowed period. Do not automatically grant broad rights, open closed periods, mass repost or modify standard configuration.

## Gate 9 — Post-change validation

Use required ladder: structural/syntax → static → metadata/runtime → functional → business/accounting. Passing syntax/static/build does not prove runtime or accounting correctness. If required runtime/business validation cannot be executed, Gate 9 is `blocked`.

Compare identical analytics before/after: movements, records, quantities, amounts, balances, postings/subaccounts, month-close result, duplicates, side effects or access matrix. A disappearing UI error is insufficient proof. Analysis-only work may mark Gate 9 `not_required`.

If a defect/omission survives an earlier control, record where it escaped and strengthen the earliest applicable gate/checklist/regression eval.

## Gate 10 — Final closure

Return:
1. **Краткий вывод** — final status and proven cause or explicit uncertainty.
2. **Основание** — evidence, causal chain, provenance closure and verification result.
3. **Что делать дальше** — safe action or smallest missing evidence set.
4. Compact Gate 0–10 status, active graph and capability provenance.
5. **Current goal status** — `closed | blocked | open`.
6. **Linked incident status** — `resolved | open | blocked | not_in_scope`.

Allowed gate statuses: `pending | passed | blocked | failed | stale | not_required`. New evidence or changed input identity invalidates downstream gates from the earliest affected point.

## Non-negotiable controls

- No invented 1C objects.
- No hidden use or simulated output of unavailable companions.
- No external plugin output treated as truth without evidence linkage.
- No supplied material evidence silently omitted.
- No material derived evidence accepted without artifact anchor/derivation lineage.
- No stale or mismatched executable result accepted as current evidence.
- No reviewer severity/confidence label treated as defect without reproduction/evidence linkage.
- No lower-level validation promoted into proof of a required higher-level result.
- No producer self-report treated as independent validation.
- No final `УСТАНОВЛЕНО` with open/broken provenance closure or without Gate 7.
- No production-changing action without the applicable risk gate.
- No decorated/noncanonical Gate statuses.
- No `EVAL_RESULT_JSON` object that violates the supplied skeleton.
- No incident closure claim when only a narrower goal is complete.
- No restart from zero when valid state exists.
