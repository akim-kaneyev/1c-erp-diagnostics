---
name: one-c-erp-diagnostics
description: Orchestrate a mandatory evidence-first Gate 1-10 workflow for 1C:ERP incidents. Use when the user needs a verified cause, comparison, correction plan, or safe next action for movements, registers, postings, month close, cost, expenses, settlements, VAT, warehouse/series/assignments, production, access rights, or 1C code behavior.
---

# 1C ERP Diagnostics — master orchestrator

This is the single entrypoint. The user must not have to invoke companion skills manually.

## Core contract

Run Gate 1 through Gate 10 in order. A required gate may not be silently skipped. If a required capability or evidence source is unavailable, mark the gate `blocked` and do not claim downstream verification occurred.

Use companion skills from this plugin when they match the gate/domain. If the host does not explicitly expose sub-skill invocation, apply their rules inline; the sequence remains authoritative here.

## Evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Prefer: exact movements → exact register records → postings/OSV drill-down → reports → code/queries → screenshots → official documentation → general theory.
- General knowledge may generate hypotheses, never prove this case by itself.
- A disappearing UI error is not proof that accounting is correct.
- Final `УСТАНОВЛЕНО` requires an adversarial second pass.

## Gate 1 — Goal contract
Define outcome, verification evidence, scope, material exclusions and stop condition. Pass only when success is checkable.

## Gate 2 — Evidence intake
Inventory all supplied evidence, record what each item can/cannot prove, preserve identifiers/hashes where possible, and list blind spots.

## Gate 3 — Route case
Choose one primary domain by observed symptom, not assumed cause. Add at most one secondary domain when a concrete cross-domain link is evidenced.

## Gate 4 — Primary diagnosis
Separate fact / interpretation / hypothesis. Build chronology, good-vs-bad or before-vs-after comparison, earliest demonstrated divergence, and causal chain:
`document → movement → record/register → consuming mechanism → accounting/stock/access result → symptom`.

## Gate 5 — Execution / sandbox decision
Use isolated execution only when it adds verifiable value. If not needed: `not_required`. If required but unavailable: `blocked`.

## Gate 6 — Preliminary conclusion
Use only `УСТАНОВЛЕНО`, `ВЕРОЯТНО`, `ТРЕБУЕТ ПРОВЕРКИ`. For each material conclusion record exact evidence, causal link, alternatives checked and falsifier. No business correction is authorized yet.

## Gate 7 — Independent verification
Perform a distinct adversarial pass: re-read evidence, challenge every causal link, search earlier divergence, detect invented assumptions, compare identical analytics, test reasonable alternatives, downgrade when needed. Final `УСТАНОВЛЕНО` is forbidden if this gate did not pass.

## Gate 8 — Action decision
Choose the smallest safe reversible action. Prefer proven standard setting/NSI → standard 1C mechanism/document → correction of actual source document in an allowed period → manual/specialized correction only when justified. Do not automatically open closed periods, mass repost, grant broad rights or modify the standard configuration.

## Gate 9 — Post-change validation
Compare the same analytics before/after: movements, records, quantities, amounts, balances, postings, close results, duplicates/side effects or access matrix. Analysis-only goals may mark this `not_required` explicitly.

## Gate 10 — Final closure
Return: `Краткий вывод`, `Основание`, `Что делать дальше`, plus compact Gate 1–10 statuses. Close only when every required gate is `passed` or `not_required`.

## Resume behavior
If prior state/decision log exists, read it first. Continue from earliest `pending`, `blocked`, `failed` or `stale` gate. New evidence may invalidate passed gates; reopen from the earliest affected gate.
