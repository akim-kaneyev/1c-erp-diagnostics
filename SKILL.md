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
4. Also inventory relevant host capabilities such as PDF, Spreadsheets, Documents, GitHub, Drive, Computer Use, OpenSandbox and the optional local `sonarqube-bsl-local` adapter. For SonarQube, do not classify from named-tool inventory: when local execution and loopback HTTP exist, apply `one-c-erp-local-static-analysis` and run its read-only server/scanner preflight.
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
- `sonarqube-bsl-local`: static BSL findings from an actually discovered loopback SonarQube instance; read existing analysis as `R0`, and route a new sanitized scan through Gate 5 as `R1`.

Use the smallest sufficient set. If the preferred capability is unavailable, use a documented read-only fallback or mark the dependent node `blocked`.

## Gate 1 — Goal contract

Define the concrete outcome, scope, evidence of completion, exclusions and stop condition. Use the measurable quality bar from OpenAI `define-goal`, but do not turn ordinary work into a separate persistent goal automatically.

### Scope model

Separate two statuses whenever the current request is narrower than the underlying 1C incident:

- **current goal/task scope** — the exact analysis or decision the user requested now;
- **linked incident scope** — the accounting, operational or technical incident that may remain unresolved.

Example: a request to assess whether mass reposting is safe may be completed as a safety assessment even though the root cause of the cost incident remains open. Do not silently convert a safety-assessment goal into a root-cause diagnosis, and do not describe the incident itself as closed merely because the narrower assessment is complete.

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

When root-cause investigation is explicitly outside the current goal, mark Gate 4 `not_required` for that goal and record the linked incident as `open` or `blocked`. Do not use decorated or qualified gate values such as `passed*` to hide an unresolved diagnostic branch.

## Gate 5 — Executable validation and sandbox decision

Use local tools, `1c-skills`, `1c-skills-py`, Unica runtime capabilities, OpenSandbox or `one-c-erp-local-static-analysis` only when executable validation adds measurable value. Default to read-only and sanitized inputs.

- Use 1C Skills PowerShell for Windows-first operations only when Windows/1C runtime prerequisites are confirmed.
- Use 1C Skills Python for cross-platform artifact operations when its implementation supports the exact format/task.
- Use Unica build/test/write capabilities only after the relevant risk classification and confirmation.
- Use OpenSandbox for isolation, not to bypass permissions or data minimization.
- Use `sonarqube-bsl-local` only after Gate 0 confirms the loopback server, scanner, BSL plugin/profile, pre-created project and scoped authentication. Keep scanner credentials only in the child-process environment and treat every static finding as a hypothesis until linked to case evidence.

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
5. **Current goal status** — `closed | blocked | open`.
6. **Linked incident status** — `resolved | open | blocked | not_in_scope`.

Allowed gate statuses are only `pending | passed | blocked | failed | stale | not_required`. Do not use decorated statuses such as `passed*`.

Gate 10 may be `passed` for a narrowly defined safety assessment when all gates required by that assessment are `passed` or `not_required`. In that case the output must say, for example, `Current goal: closed; linked incident: open`, and must not state that the 1C incident or root cause is closed.

If the current goal includes root-cause diagnosis or correction, any required `blocked`, `failed`, `pending` or `stale` gate prevents Gate 10 from passing. New evidence invalidates downstream gates from the earliest affected point.

## Non-negotiable controls

- No invented 1C objects.
- No hidden use of unavailable companion plugins.
- No copied or simulated Unica/1C Skills output.
- No external plugin output treated as truth without evidence linkage.
- No final cause without Gate 7.
- No production-changing action without the applicable risk gate.
- No decorated gate statuses or ambiguous asterisk qualifications.
- No statement that an incident is closed when only a narrower assessment is complete.
- No restart from zero when valid state exists.
