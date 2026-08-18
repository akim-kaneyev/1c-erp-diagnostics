---
name: one-c-erp-diagnostics
description: Orchestrate evidence-first 1C:ERP diagnosis and safe correction. Use for incidents involving movements, registers, postings, month close, cost, expenses, settlements, VAT, warehouse/series/assignments, production, or access rights when the user needs a cause, comparison, correction plan, or verified conclusion.
user-invocable: true
argument-hint: "[case path or task description]"
---

# 1C ERP Diagnostics — Mandatory Workflow

## Single entry command

Explicit invocation command:

`$one-c-erp-diagnostics <case path or task description>`

This is the only command the user should need for the full diagnostic workflow. Do not ask the user to invoke internal skills, playbooks, prompts or validators manually.

On explicit invocation, run the workflow from Stage 0 through Gate 10 in order. A gate may be `not_required` only when its own criteria say so. A required gate may never be silently skipped.

If a required external capability, plugin, connector, sandbox or evidence source is unavailable, mark the affected gate `blocked`, state exactly what is unavailable, and do not represent downstream verification as completed.

## Purpose

Run 1C:ERP investigations in a fixed, resumable order so that a plausible hypothesis is never presented as a proven cause.

For a simple explanatory question that does not require diagnosis, comparison, or correction, answer directly and do not force the full workflow unless the user explicitly invoked `$one-c-erp-diagnostics`. The no-invention rules from `AGENTS.md` still apply.

## Stage 0 — Resume or initialize

1. Read `AGENTS.md`.
2. If the case already has `STATE.md`, read it before doing new analysis.
3. Continue from the first incomplete, blocked or stale gate. Do not repeat passed gates unless new evidence can invalidate them.
4. If no state exists and a persistent case workspace is available, create it from `templates/case/STATE.md`.
5. If persistent files cannot be created in the current surface, maintain the same gate state in the working response/context and explicitly say that durable resume state is unavailable.

## Gate 1 — Goal contract

Before investigation, state a concrete goal using the quality bar aligned with OpenAI `define-goal`:

- what concrete result must become true;
- which system/document/report/period is in scope;
- what evidence will prove completion;
- what is explicitly out of scope when it matters;
- what condition requires stopping and asking instead of guessing.

Do not turn ordinary work into a persistent goal-tool task automatically. If an installed `define-goal` skill is explicitly requested/appropriate, use it; otherwise apply the quality bar as an internal case contract.

**Gate passes only when success can be verified.**

## Gate 2 — Evidence intake

1. Inventory all provided files and screenshots.
2. Prefer exact movements, register records, postings, report drill-downs, code and official documentation over general theory.
3. Hash/index files when working in a case directory.
4. Mark what each source can and cannot prove.
5. Record missing evidence.

**Gate passes only when the available evidence and blind spots are explicit.**

## Gate 3 — Route the case

Read `playbooks/router.md` and select one primary playbook. Add a second only when a concrete cross-domain link is evidenced.

**Gate passes only when the selected playbook matches the observed symptom, not an assumed cause.**

## Gate 4 — Primary diagnosis

Execute `skills/diagnose-1c-erp/SKILL.md` plus the selected playbook.

Required chain:

`document → movement → record/register → consuming mechanism → accounting/stock result → observed symptom`

Build:

- fact table;
- good/bad or before/after comparison where available;
- hypotheses with confirm/falsify conditions;
- earliest demonstrated divergence point.

Never invent metadata object names.

## Gate 5 — Execution / sandbox decision

Use OpenSandbox only when isolated execution adds value, for example:

- running Codex or scripts on sanitized case files;
- testing an untrusted parser/tool;
- reproducing a transformation;
- running repeatable validation commands without touching the working environment.

If OpenSandbox is used:

1. use sanitized minimum data;
2. do not place production `.dt` or plaintext secrets in the sandbox;
3. restrict network egress where practical;
4. record commands, versions, inputs and outputs;
5. treat sandbox output as evidence to evaluate, not as truth by itself;
6. destroy/expire the sandbox after the case when appropriate.

If no executable validation is needed, mark Gate 5 `not_required`.
If executable sandbox validation is required for the claimed result but OpenSandbox or an equivalent isolated executor is unavailable, mark Gate 5 `blocked`; do not pretend the validation occurred.

## Gate 6 — Preliminary conclusion

Produce a preliminary result using only:

- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

For every material conclusion record:

- conclusion ID;
- exact evidence;
- causal link;
- alternative explanation checked;
- falsifier: what finding would make the conclusion wrong.

No business correction is authorized by this gate alone.

## Gate 7 — Independent verification

Run `prompts/verify-conclusion.md` as a separate adversarial pass.

The verifier must not defend the preliminary answer. It must:

1. re-read the evidence;
2. challenge each causal link;
3. identify invented/unproven objects or assumptions;
4. check whether before/after comparisons use identical analytics;
5. search for an earlier divergence point;
6. check reasonable alternatives;
7. downgrade the status when evidence is insufficient.

If a separate verification pass cannot actually be performed in the current environment, mark this gate `blocked` or return `ТРЕБУЕТ ПРОВЕРКИ`; never label the cause final `УСТАНОВЛЕНО` on the basis of the primary pass alone.

**A cause is final `УСТАНОВЛЕНО` only if it survives this gate.**

## Gate 8 — Action decision

Choose the smallest safe and reversible action.

Priority:

1. verify/adjust standard configuration or NSI when proven relevant;
2. use a standard 1C document/mechanism;
3. correct the actual source document in an allowed period when justified;
4. use specialized/manual corrections only when standard mechanisms are unsuitable and consequences are understood.

Do not automatically open closed periods, mass repost, grant broad rights, or modify the standard configuration.

If a production-changing action is required, state the expected accounting effect, scope, rollback path, and validation plan before execution.

## Gate 9 — Post-change validation

After an approved change, compare the same analytics before and after.

Verify not only that an error message disappeared, but also the relevant:

- movements/records;
- quantities and amounts;
- balances;
- postings/subaccounts;
- month-close result;
- duplicate/side effects;
- user access matrix, for rights cases.

If no change has been applied yet, Gate 9 remains `pending` or becomes `not_required` only when the user's goal is analysis-only and Gate 8 explicitly records that no change is in scope.

If the expected result is not reproduced, reopen the earliest affected gate and mark downstream gates `stale`.

## Gate 10 — Final closure

Final response must contain:

1. **Краткий вывод** — status and proven cause or explicit uncertainty.
2. **Основание** — evidence and causal chain.
3. **Что делать дальше** — safe action or smallest missing evidence.

Update `STATE.md` with the final status, evidence set, verification result, applied change (if any), and remaining blind spots.

A case may be `CLOSED` only when every required gate is `passed` or `not_required`. If any gate is `blocked`, `failed`, `pending` or `stale`, final closure must say what remains unresolved.

## Internal routing — no user commands required

The orchestrator itself must invoke/use as relevant:

- `playbooks/router.md`;
- one primary playbook and at most one justified secondary playbook;
- `skills/diagnose-1c-erp/SKILL.md`;
- `prompts/verify-conclusion.md`;
- local parsers/comparison tools from `tools/` when they are suitable;
- available connected apps/plugins only when their data/action is required;
- OpenSandbox only under Gate 5 rules.

Do not make the user manually chain these components.

## Non-negotiable controls

- No invented 1C objects.
- No cause without a causal chain.
- No final `УСТАНОВЛЕНО` without an independent verification pass.
- No correction validated only by disappearance of a UI error.
- No restart-from-zero when a valid case state exists.
- No silent substitution for an unavailable required plugin/tool/evidence source.
- New evidence can invalidate earlier gates; when it does, mark them stale and re-run from the earliest affected gate.
