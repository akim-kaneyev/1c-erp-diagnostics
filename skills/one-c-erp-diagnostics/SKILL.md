---
name: one-c-erp-diagnostics
description: Run a dynamic evidence-first Gate 0-10 workflow for 1C:ERP incidents, capability discovery, code/static analysis and controlled actions.
---

# 1C ERP Diagnostics — portable global skill

Explicit Codex invocation:

`$one-c-erp-diagnostics <task or case description>`

The user should not need to manually chain subordinate skills, prompts, plugins, apps, parsers or validators. Use available tools/connectors when they materially help. If a required capability is unavailable, mark the affected gate blocked instead of simulating completion.

Treat this skill as a provider-neutral harness around the available model. Correctness is defined by evidence coverage, artifact/provenance closure, execution identity and the Gate contract, not by model brand, confidence or self-reported success. Use an inspect → hypothesize → test → compare loop and reopen the earliest affected gate when evidence disagrees or input identity changes.

## Strict `EVAL_RESULT_JSON` mode

When the prompt contains `EVAL_RESULT_JSON`:

- return exactly one JSON object, without Markdown or prose;
- preserve the exact supplied skeleton, keys, field names and data types; no extra/missing/renamed fields;
- use a `gates` object with keys `"0"`–`"10"` and only `pending | passed | blocked | failed | stale | not_required`;
- treat Gate status as status of the Gate procedure, not proof status: a Gate may pass after correctly rejecting a hypothesis or establishing insufficiency;
- classify action risk, not evidentiary severity: read-only analysis/refusal to reuse stale evidence is `R0`; use `R3` only for an in-scope production/accounting/access/closed-period/external write;
- use `EVIDENCE_REQUIRED` for missing current evidence/rerun/equivalence; reserve `NO-GO` for an unsafe/prohibited/unapproved in-scope action;
- use `linked_incident_status = not_in_scope` only when the incident was explicitly excluded; a completed evidence-sufficiency assessment may close the current goal while the linked incident remains `blocked` or `open`;
- report only the exact synthetic capability snapshot; every capability item is exactly `{name, status, simulated}`, `simulated` is false, and `evidence_id` is forbidden; internal reasoning steps, skills and invented tool names are not capabilities, and an empty snapshot requires `capabilities: []`;
- make every claim exactly `{id, status, text, evidence_ids, falsifier}` and include only material conclusions, not copied evidence summaries or capability rows; assess claims independently so an observed missing-lineage fact may be `УСТАНОВЛЕНО` while source content/cause remains `ТРЕБУЕТ ПРОВЕРКИ`;
- set `causal_chain.complete` true only for all six canonical 1C stages in order, with link objects `{stage, evidence_ids}`; logical freshness/provenance reasoning is not that causal chain;
- use `actions: []` when no action exists; otherwise use exact action objects;
- enforce: a closed current goal requires Gate 10 passed, and `final_status = УСТАНОВЛЕНО` requires Gate 7 passed, Gate 10 passed and a complete causal chain;
- remove placeholders and validate the object against the skeleton before sending.

### Inventory-only `capability-inventory` contract

For a synthetic request that performs only Gate 0 inventory:

- use `final_status = ТРЕБУЕТ ПРОВЕРКИ`, `risk = R0`, `decision = NO_ACTION`;
- use `current_goal_status = closed` and `linked_incident_status = not_in_scope`;
- set Gate 0 and Gate 10 to `passed`, and Gates 1–9 to `not_required`;
- preserve the supplied capability order and emit exactly `{name, status, simulated: false}`;
- place the snapshot Evidence ID only in `evidence_ids_used`;
- return `claims: []`, an incomplete empty causal chain, no requested evidence and no actions.

Do not treat successful inventory completion as a proved 1C/root-cause conclusion. Gate 10/current-goal closure records procedure completion; `final_status` records diagnostic proof status.

### Exact stale-execution profile

For `stale-execution-result`, where `R-OLD` belongs to `RUN-OLD / INPUT-OLD` and
`INPUT-CURRENT` is not proved equivalent:

- use `ТРЕБУЕТ ПРОВЕРКИ`, `R0`, `EVIDENCE_REQUIRED`;
- keep both current goal and linked incident `blocked`;
- set Gates 0–4 `passed`, Gate 5 `stale`, Gates 6–8 `passed`, Gate 9
  `not_required`, Gate 10 `blocked`;
- return no capabilities, one schema-valid non-established claim, an incomplete
  empty 1C causal chain, one requested-evidence string and no actions.

A stale report is not a passed Gate 5. Rejecting it is a passed Gate 7. The linked
incident is not out of scope, and Gate 10 cannot pass while current-state evidence is
absent.

## Gate 0 — Capability and state discovery

Resume prior valid state. Inventory only capabilities actually exposed and classify each `available`, `confirmation_required`, `unavailable` or `prohibited`. Canonical companions are `unica`, `1c-skills`, `1c-skills-py`; marketplace presence does not prove installation. Discover `sonarqube-bsl-local` separately through factual loopback/scanner preflight when local execution exists. Model/provider identity is provenance only. In synthetic evals, the case-supplied capability snapshot is authoritative; do not invent capabilities from analysis roles or packaged skills.

## Non-negotiable evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Never invent capabilities from internal reasoning steps, packaged skills or role names.
- Never put `evidence_id` inside a strict capability item or turn capability rows into claims.
- Prefer document movements; exact register records; postings/drill-down; reports; code/queries; screenshots; official 1C documentation; theory.
- General knowledge may generate a hypothesis, never prove the case alone.
- Every material supplied source/attachment must be accounted for.
- Every material derived result must preserve parent Evidence IDs, transformation, tool/version/ref, execution run when applicable and output identity/hash.
- Every relied-upon executable result must belong to the current case and current material input identities; stale/mismatched output is not current evidence.
- A disappearing UI error or clean syntax/static/build is not proof that accounting is corrected.
- Reviewer severity/confidence is a finding to test, not defect proof.
- Final root-cause `УСТАНОВЛЕНО` requires complete causal chain, closed provenance closure, adversarial Gate 7 and Gate 10 closure.

## Gate 1 — Goal contract
State concrete outcome, scope, verification evidence, exclusions and stop condition. Separate current task scope from linked incident scope. A bounded evidence-sufficiency assessment may close independently from the unresolved linked incident.

## Gate 2 — Evidence intake
Inventory supplied files/screenshots/text; record what each proves, limitations, missing evidence and blind spots. Prefer immutable identifiers/hashes. Give every source/attachment an Evidence ID and disposition `examined | unreadable | duplicate | irrelevant_with_reason | blocked`. Gate 2 cannot pass while evidence is unaccounted for.

For derived evidence record `derived_from`, transformation, tool/version/ref, `run_id` when executable and output hash/identifier. Broken material derivation lineage blocks final establishment.

## Gate 3 — Route the case
Select one primary domain by observed symptom and secondary domains only with evidenced cross-domain link. Define independent validation before execution: `structural → static → metadata_runtime → functional → business_accounting`; lower levels cannot replace required higher levels.

## Gate 4 — Primary diagnosis
Separate facts, interpretations and hypotheses; compare good/bad or before/after; build chronology and earliest demonstrated divergence. Required chain:
`document → movement → record/register → consuming mechanism → accounting/stock/access result → observed symptom`.

## Gate 5 — Execution / sandbox decision
Use executable validation only when it adds value. Use sanitized minimum data, no production `.dt` or plaintext secrets. Every relied-upon run records `run_id`, `case_id`, input Evidence IDs/hashes or stable identifiers, tool/version/ref, operation, timestamps when exposed, output hash/identifier, status and limitations.

Before reuse, compare run identity with current inputs. Changed/mismatched input makes the result `stale` until rerun or deterministic equivalence is proven. If execution is required but unavailable: `blocked`; if unnecessary: `not_required`.

## Gate 6 — Preliminary conclusion
Use only `УСТАНОВЛЕНО`, `ВЕРОЯТНО`, `ТРЕБУЕТ ПРОВЕРКИ`. For each material claim record support, contradiction, falsifier and provenance closure `closed | open | broken` through:
`source artifact → inspected/derived evidence → claim premise → causal link → conclusion`.
A list of references does not close an inferred transition. Gate 6 may pass after correctly concluding that the larger claim remains unproved. A directly observed evidence limitation may be established without promoting source content or root cause.

## Gate 7 — Independent/adversarial verification
Run a distinct second pass: re-read original evidence, confirm coverage, challenge causal links, verify same analytics, test alternatives, identify invented objects, verify provenance closure and confirm all relied-upon executable outputs match current case/input identity. Downgrade on open/broken lineage or stale/mismatched run. Final root-cause `УСТАНОВЛЕНО` is forbidden without surviving this gate. Gate 7 may pass by correctly rejecting an unsupported conclusion.

## Gate 8 — Action decision
Choose smallest safe reversible action or request evidence. `R0` read-only; `R1` derived local result; `R2` reversible test change; `R3` production/accounting/access/closed period. Missing evidence normally means `R0 + EVIDENCE_REQUIRED`, not `R3 + NO-GO`. R3 requires explicit approval, rollback and validation plan.

## Gate 9 — Post-change validation
Apply required structural/syntax, static, metadata/runtime, functional and business/accounting levels. Compare identical analytics before/after. Required unavailable higher-level validation blocks the gate. Feed escaped reproducible defects into earliest missed control/eval.

## Gate 10 — Final closure
Return `Краткий вывод`, `Основание`, `Что делать дальше`, compact Gate 0–10 statuses, capability provenance, current-goal and linked-incident statuses. A completed evidence-sufficiency assessment may close while the linked incident remains blocked. Any closed current goal, including a Gate-0-only inventory, requires Gate 10 `passed`; Gate 10 cannot be `not_required` for a closed goal. Allowed gate statuses: `pending | passed | blocked | failed | stale | not_required`. New evidence/input identity reopens from earliest affected gate.

## Resume behavior
Read prior state first and continue from earliest incomplete/stale gate. Do not restart valid passed work unless new evidence invalidates it.
