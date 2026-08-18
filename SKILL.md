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

## Gate 0 — Capability and state discovery

1. Read `AGENTS.md`, `docs/ECOSYSTEM_MARKETPLACE.md` and existing `STATE.md`.
2. Inventory only capabilities actually exposed in the current host/session.
3. Check the canonical marketplace companions by exact identity:
   - `unica` — Unica 1C developer workflows;
   - `1c-skills` — 1C Skills PowerShell;
   - `1c-skills-py` — 1C Skills Python.
4. Also inventory relevant host capabilities such as PDF, Spreadsheets, Documents, GitHub, Drive, Computer Use and OpenSandbox.
5. Classify each capability as `available`, `confirmation_required`, `unavailable` or `prohibited`.
6. Record version/ref when exposed, permissions, write-risk, provenance and the exact purpose for which a capability may be used.
7. Continue from the earliest `pending`, `blocked`, `failed` or `stale` gate.

The unified marketplace makes companions discoverable; it does not prove installation or cross-plugin invocation support. Do not claim availability until the host exposes the capability.

### Capability routing baseline

- `unica`: metadata/BSL navigation, developer workflows and controlled build/test investigation.
- `1c-skills`: Windows-first configurator, XML, MXL/СКД/form/report and web-client tooling.
- `1c-skills-py`: cross-platform artifact parsing, comparison and controlled automation.
- internal domain skills: accounting causality, movements/registers/postings, ERP process and release analysis.
- OpenSandbox: isolated executable validation, never a source of 1C truth.

Use the smallest sufficient set. If the preferred capability is unavailable, use a documented read-only fallback or mark the dependent node `blocked`.

## Gate 1 — Goal contract

Define the concrete outcome, scope, evidence of completion, exclusions and stop condition. Use the measurable quality bar from OpenAI `define-goal`, but do not turn ordinary work into a separate persistent goal automatically.

## Gate 2 — Evidence intake

Inventory all files, screenshots, reports, movements, register records, postings, code and official sources. State what each item proves and cannot prove. Preserve identifiers and hashes when possible. For CF/CFE/EPF or unpacked BSL/JSON, apply the artifact-extraction skill and checklist.

## Gate 3 — Dynamic execution graph

Choose one primary domain and no more than two justified secondary domains. Build a directed execution graph containing:

- specialist objective;
- input evidence IDs and analytic keys;
- dependency nodes;
- exact internal skill or canonical companion capability;
- read/write surface and `R0–R3` risk;
- output schema and provenance fields;
- stop/falsification condition;
- fallback if the assigned companion is unavailable.

Run specialists in parallel only when they do not mutate shared state and their questions are independent. Do not activate more than four specialist nodes without explicit dependency justification.

## Gate 4 — Specialist analysis

Each specialist must separate facts, interpretations, hypotheses and missing evidence. The core causal chain is:

`document → movement → record/register → consuming mechanism → accounting/stock/access result → symptom`

The earliest proven divergence is more important than the latest visible symptom. Code or tooling findings remain hypotheses until linked to the factual case chain.

For every external companion output record canonical plugin/tool identity, assigned operation, evidence inputs, version/ref when available, output location/hash, limitations and whether another method reproduced the material result.

## Gate 5 — Executable validation and sandbox decision

Use local tools, `1c-skills`, `1c-skills-py`, Unica runtime capabilities or OpenSandbox only when executable validation adds measurable value. Default to read-only and sanitized inputs.

- Use 1C Skills PowerShell for Windows-first operations only when Windows/1C runtime prerequisites are confirmed.
- Use 1C Skills Python for cross-platform artifact operations when its implementation supports the exact format/task.
- Use Unica build/test/write capabilities only after the relevant risk classification and confirmation.
- Use OpenSandbox for isolation, not to bypass permissions or data minimization.

If required execution is unavailable, mark the gate `blocked`; never simulate it.

## Gate 6 — Evidence synthesis

Merge specialist outputs by source, evidence and claim ID. Preserve supporting and contradicting evidence, capability provenance and falsifiers. Resolve contradictions explicitly; a majority vote is not evidence. Produce a preliminary status only from:

- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

## Gate 7 — Adversarial verification

A distinct reviewer re-reads original evidence, not only the synthesis. It challenges every causal link, checks identical analytics, searches for an earlier divergence, tests alternatives, identifies invented objects and records a falsifier. Final `УСТАНОВЛЕНО` is forbidden if this gate is unavailable or fails.

An external plugin's conclusion is not exempt from this review.

## Gate 8 — Risk-controlled action decision

Classify the action:

- `R0` — read-only analysis;
- `R1` — derived local files or reports;
- `R2` — reversible test-environment change;
- `R3` — production, accounting, access rights, closed periods or broad reposting.

R3 requires explicit user approval, tested rollback, affected-scope statement and post-change validation plan. Prefer standard 1C configuration/NSI, then a standard document/mechanism, then correction of the actual source document in an allowed period. Do not automatically grant broad rights, open closed periods, mass repost or modify the standard configuration.

## Gate 9 — Post-change validation

Compare the same analytic key before and after. Check movements, records, quantities, amounts, balances, postings/subaccounts, month-close result, duplicates, side effects or access matrix. Disappearance of an interface error is not sufficient proof. Analysis-only work may mark Gate 9 `not_required` explicitly.

## Gate 10 — Final closure

Return:

1. **Краткий вывод** — final status and proven cause or explicit uncertainty.
2. **Основание** — evidence, causal chain and verification result.
3. **Что делать дальше** — safe action or smallest missing evidence set.
4. Compact Gate 0–10 status, active specialist graph and capability provenance.

A case is closed only when all required gates are `passed` or `not_required`. New evidence invalidates downstream gates from the earliest affected point.

## Non-negotiable controls

- No invented 1C objects.
- No hidden use of unavailable companion plugins.
- No copied or simulated Unica/1C Skills output.
- No external plugin output treated as truth without evidence linkage.
- No final cause without Gate 7.
- No production-changing action without the applicable risk gate.
- No restart from zero when valid state exists.
