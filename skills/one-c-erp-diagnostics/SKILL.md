---
name: one-c-erp-diagnostics
description: Run a dynamic evidence-first Gate 0-10 workflow for 1C:ERP incidents, capability discovery, code/static analysis and controlled actions.
---

# 1C ERP Diagnostics — portable global skill

Explicit Codex invocation:

`$one-c-erp-diagnostics <task or case description>`

The user should not need to manually chain subordinate skills, prompts, plugins, apps, parsers or validators. Use available tools/connectors when they materially help. If a required capability is unavailable, mark the affected gate blocked instead of simulating completion.

Treat this skill as a provider-neutral harness around the available model. Correctness is defined by evidence coverage, artifact/provenance closure, execution identity and the Gate contract, not by model brand, confidence or self-reported success. Use an inspect → hypothesize → test → compare loop and reopen the earliest affected gate when evidence disagrees or input identity changes.

## Gate 0 — Capability and state discovery

Resume prior valid state. Inventory only capabilities actually exposed and classify each `available`, `confirmation_required`, `unavailable` or `prohibited`. Canonical companions are `unica`, `1c-skills`, `1c-skills-py`; marketplace presence does not prove installation. Discover `sonarqube-bsl-local` separately through factual loopback/scanner preflight when local execution exists. Model/provider identity is provenance only.

## Non-negotiable evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Prefer document movements; exact register records; postings/drill-down; reports; code/queries; screenshots; official 1C documentation; theory.
- General knowledge may generate a hypothesis, never prove the case alone.
- Every material supplied source/attachment must be accounted for.
- Every material derived result must preserve parent Evidence IDs, transformation, tool/version/ref, execution run when applicable and output identity/hash.
- Every relied-upon executable result must belong to the current case and current material input identities; stale/mismatched output is not current evidence.
- A disappearing UI error or clean syntax/static/build is not proof that accounting is corrected.
- Reviewer severity/confidence is a finding to test, not defect proof.
- Final `УСТАНОВЛЕНО` requires complete causal chain, closed provenance closure and adversarial Gate 7.

## Gate 1 — Goal contract
State concrete outcome, scope, verification evidence, exclusions and stop condition. Separate current task scope from linked incident scope.

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
A list of references does not close an inferred transition.

## Gate 7 — Independent/adversarial verification
Run a distinct second pass: re-read original evidence, confirm coverage, challenge causal links, verify same analytics, test alternatives, identify invented objects, verify provenance closure and confirm all relied-upon executable outputs match current case/input identity. Downgrade on open/broken lineage or stale/mismatched run. Final `УСТАНОВЛЕНО` is forbidden without surviving this gate.

## Gate 8 — Action decision
Choose smallest safe reversible action. `R0` read-only; `R1` derived local result; `R2` reversible test change; `R3` production/accounting/access/closed period. R3 requires explicit approval, rollback and validation plan.

## Gate 9 — Post-change validation
Apply required structural/syntax, static, metadata/runtime, functional and business/accounting levels. Compare identical analytics before/after. Required unavailable higher-level validation blocks the gate. Feed escaped reproducible defects into earliest missed control/eval.

## Gate 10 — Final closure
Return `Краткий вывод`, `Основание`, `Что делать дальше`, compact Gate 0–10 statuses, capability provenance, current-goal and linked-incident statuses. Allowed gate statuses: `pending | passed | blocked | failed | stale | not_required`. New evidence/input identity reopens from earliest affected gate.

## Resume behavior
Read prior state first and continue from earliest incomplete/stale gate. Do not restart valid passed work unless new evidence invalidates it.
