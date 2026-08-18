---
name: one-c-erp-diagnostics
description: Run the dynamic evidence-first Gate 0-10 workflow for 1C:ERP incidents, comparisons, code, releases, access rights and safe remediation.
user-invocable: true
argument-hint: "[case path or task description]"
---

# 1C ERP Diagnostics — Dynamic Gate 0–10 Orchestrator

## Single entrypoint

`$one-c-erp-diagnostics <case path or task>`

The user invokes one command. The orchestrator discovers capabilities, selects internal specialist skills and optional companion plugins, runs verification and reports one consolidated result. Never require the user to manually chain skills.

## Gate 0 — Capability and state discovery

1. Read `AGENTS.md` and existing `STATE.md`.
2. Inventory only capabilities actually exposed in the current host/session.
3. Classify each capability as `available`, `confirmation_required`, `unavailable` or `prohibited`.
4. Record provenance, write-risk and the exact purpose for which a capability may be used.
5. Continue from the earliest `pending`, `blocked`, `failed` or `stale` gate.

Do not claim that Unica, 1C Skills, OpenSandbox, MCP, a connector or any other companion is available until the host exposes it.

## Gate 1 — Goal contract

Define the concrete outcome, scope, evidence of completion, exclusions and stop condition. Use the measurable quality bar from OpenAI `define-goal`, but do not turn ordinary work into a separate persistent goal automatically.

## Gate 2 — Evidence intake

Inventory all files, screenshots, reports, movements, register records, postings, code and official sources. State what each item proves and cannot prove. Preserve identifiers and hashes when possible. For CF/CFE/EPF or unpacked BSL/JSON, apply the artifact-extraction skill and checklist.

## Gate 3 — Dynamic execution graph

Choose one primary domain and no more than two justified secondary domains. Build a directed execution graph containing:

- specialist objective;
- input evidence;
- dependency nodes;
- allowed capabilities;
- output schema;
- stop/falsification condition.

Run specialists in parallel only when they do not mutate shared state and their questions are independent.

## Gate 4 — Specialist analysis

Each specialist must separate facts, interpretations, hypotheses and missing evidence. The core causal chain is:

`document → movement → record/register → consuming mechanism → accounting/stock/access result → symptom`

The earliest proven divergence is more important than the latest visible symptom. Code or tooling findings remain hypotheses until linked to the factual case chain.

## Gate 5 — Executable validation and sandbox decision

Use local tools, 1C Skills runtimes or OpenSandbox only when executable validation adds measurable value. Default to read-only and sanitized inputs. If required execution is unavailable, mark the gate `blocked`; never simulate it.

## Gate 6 — Evidence synthesis

Merge specialist outputs by source and claim ID. Resolve contradictions explicitly. A majority vote is not evidence. Produce a preliminary status only from:

- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

## Gate 7 — Adversarial verification

A distinct reviewer re-reads original evidence, not only the synthesis. It challenges every causal link, checks identical analytics, searches for an earlier divergence, tests alternatives, identifies invented objects and records a falsifier. Final `УСТАНОВЛЕНО` is forbidden if this gate is unavailable or fails.

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
4. Compact Gate 0–10 status and capability provenance.

A case is closed only when all required gates are `passed` or `not_required`. New evidence invalidates downstream gates from the earliest affected point.

## Non-negotiable controls

- No invented 1C objects.
- No hidden use of unavailable companion plugins.
- No external plugin output treated as truth without evidence linkage.
- No final cause without Gate 7.
- No production-changing action without the applicable risk gate.
- No restart from zero when valid state exists.
