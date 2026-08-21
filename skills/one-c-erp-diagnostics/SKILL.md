---
name: one-c-erp-diagnostics
description: Run a dynamic evidence-first Gate 0-10 workflow for 1C:ERP incidents, capability discovery, code/static analysis and controlled actions.
---

# 1C ERP Diagnostics — portable global skill

Explicit Codex invocation:

`$one-c-erp-diagnostics <task or case description>`

The user should not need to manually chain subordinate skills, prompts, plugins, apps, parsers or validators. Use available tools/connectors when they materially help. If a required capability is unavailable, mark the affected gate blocked instead of simulating completion.

## Gate 0 — Capability and state discovery

Resume prior valid case state. Inventory only capabilities actually exposed in the current host and classify each as `available`, `confirmation_required`, `unavailable` or `prohibited`. Canonical marketplace companions are `unica`, `1c-skills` and `1c-skills-py`; marketplace presence does not prove installation.

Discover `sonarqube-bsl-local` separately as an optional host adapter, not a marketplace plugin. The absence of a dedicated SonarQube tool is not evidence of absence: when local process execution and loopback HTTP exist, actually probe the loopback status/version and scanner version first. It is available only after confirming an `UP` loopback server, scanner, `communitybsl` plugin, `bsl` language/profile, pre-created project and scoped authentication. A blocked probe or `401/403` is `confirmation_required`, not an invented `unavailable`. Never expose a token or infer that a static finding proves the ERP incident.

## Non-negotiable evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Prefer case evidence in this order: document movements; exact register records; postings/OSV drill-down; reports; code/queries; screenshots; official 1C documentation; general theory.
- General 1C knowledge may generate a hypothesis, never prove the case by itself.
- A disappearing UI error is not proof that accounting is corrected.
- Final root cause `УСТАНОВЛЕНО` requires an adversarial verification pass.

## Gate 1 — Goal contract
State concrete outcome, scope, verification evidence, material exclusions, and stop condition. Pass only when completion can be checked.

## Gate 2 — Evidence intake
Inventory supplied files/screenshots/text; record what each can prove, limitations, missing evidence and blind spots. Prefer immutable source identifiers/hashes when available.

## Gate 3 — Route the case
Select one primary domain by observed symptom, not assumed cause: `cost-and-month-close`, `post-item-expenses`, `settlements`, `vat`, `warehouse-series-assignments`, `production`, or `access-rights`. Add a secondary domain only when a concrete cross-domain link is evidenced.

## Gate 4 — Primary diagnosis
Separate facts, interpretations and hypotheses; compare good/bad or before/after where available; build chronology and earliest demonstrated divergence. Required chain: `document → movement → record/register → consuming mechanism → accounting/stock/access result → observed symptom`.

Domain controls:
- Cost/month close: trace amount/quantity to registrar, separate source movements from close-generated movements, verify balances/postings.
- Post-item expenses: separate article settings from actual recorded analytics, prove allocation base and compare matching analytics.
- Settlements: build registrar chronology and find first analytical split/mismatch.
- VAT: separate operation/document/tax-record/declaration dates; drill book entry to registrar; check duplicates/corrections; verify current legal/methodology claims via official sources.
- Warehouse/series/assignments: preserve full analytical key and find first divergence without premature aggregation.
- Production: reconstruct actual chain and first break in quantity/series/assignment/order/stage continuity.
- Access rights: build `business operation → required permission` matrix; separate functional/admin/organization restrictions and test safely before mass changes.

## Gate 5 — Execution / sandbox decision
Use OpenSandbox or another isolated executor only when executable validation adds value. Use sanitized minimum data, no production `.dt` or plaintext secrets, restrict egress where practical, record commands/versions/inputs/outputs, and treat output as evidence.

For a new local BSL scan, apply `one-c-erp-local-static-analysis`: loopback sanitized scan is `R1`; project/token/profile administration is `R2`; remote source upload is `R3`. The scanner token exists only in the child-process `SONAR_TOKEN` environment, never in arguments, properties, files, logs or chat. If not needed: `not_required`. If required but unavailable: `blocked`.

## Gate 6 — Preliminary conclusion
Use only `УСТАНОВЛЕНО`, `ВЕРОЯТНО`, or `ТРЕБУЕТ ПРОВЕРКИ`. For each material conclusion record evidence, causal link, alternatives checked and falsifier. No business correction is authorized yet.

## Gate 7 — Independent/adversarial verification
Run a distinct second pass that tries to disprove Gate 6: re-read evidence, challenge every causal link, find unproven assumptions/invented objects, verify same analytics before/after, search earlier divergence, test reasonable alternatives, and downgrade when insufficient. Final `УСТАНОВЛЕНО` is forbidden without surviving this gate.

## Gate 8 — Action decision
Choose the smallest safe reversible action. Priority: proven standard setting/NSI → standard 1C mechanism/document → correction of actual source document in allowed period → specialized/manual correction only when standard mechanisms are unsuitable and consequences understood. Do not automatically open closed periods, mass repost, grant broad rights, or modify the standard configuration.

## Gate 9 — Post-change validation
Compare the same analytics before/after: applicable movements, records, quantities, amounts, balances, postings/subaccounts, month-close result, duplicates/side effects, or access matrix. If result is not reproduced, reopen from earliest affected gate. Analysis-only goals may mark this `not_required` explicitly.

## Gate 10 — Final closure
Return: 1) `Краткий вывод`; 2) `Основание`; 3) `Что делать дальше`. Also report compact Gate 0–10 statuses and capability provenance. Close only if every required gate is passed or `not_required`; state any blocked/pending/failed/stale gate.

## Resume behavior
If a project/case contains prior state or decision log, read it first and continue from the earliest incomplete/stale gate. Do not restart passed investigation steps unless new evidence invalidates them.
