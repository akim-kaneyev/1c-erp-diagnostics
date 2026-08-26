---
name: one-c-erp-diagnostics
description: Single dynamic entrypoint for evidence-first Gate 0-10 orchestration across 1C:ERP data, code, releases, a verified Unica/1C Skills ecosystem and controlled actions.
---

# Master orchestrator

Run Gate 0 through Gate 10 in order. Internally apply packaged specialist skills and installed companion capabilities. The user must not manually chain them.

This orchestrator is a provider-neutral harness around the available model: correctness comes from the Gate contract, evidence coverage, artifact/provenance closure, execution identity, tool/capability provenance, an inspect → hypothesize → test → compare loop and independent validation. Model confidence or provider identity never substitutes for evidence.

## Strict `EVAL_RESULT_JSON` mode

When the request contains the literal token `EVAL_RESULT_JSON`, machine-readable acceptance takes precedence over the normal prose response:

1. Return exactly one JSON object, with no Markdown fence, preamble, explanation or trailing text.
2. When the prompt provides a skeleton, preserve its exact top-level keys, nested types and field names. Do not add, omit or rename fields.
3. `gates` must be one object with string keys `"0"` through `"10"`. Use only `pending | passed | blocked | failed | stale | not_required` in lower case.
4. A Gate status describes whether the Gate procedure completed correctly, not whether the hypothesis was proved. A Gate may be `passed` when it correctly establishes insufficient evidence, rejects a cause or performs an adversarial downgrade. Use `blocked` only when the Gate itself cannot run; `failed` only for an invalid/failed Gate procedure; `stale` only for evidence invalidated by changed identity.
5. `risk` classifies the actual/proposed action surface. Read-only analysis, comparison or refusal to reuse stale evidence is `R0`. Do not use `R3` for evidentiary seriousness or uncertainty; `R3` requires an in-scope production/accounting/access/closed-period/external write.
6. Use `EVIDENCE_REQUIRED` when the requested conclusion/current state needs additional current evidence, rerun or proved equivalence. Use `NO-GO` only when an actual in-scope action is unsafe, prohibited or unapproved. Use `NO_ACTION` when the declared goal is complete without action or further evidence.
7. `linked_incident_status = not_in_scope` only when the prompt explicitly excludes the underlying incident. If it remains relevant but cannot be resolved, use `blocked` or `open`. `EVIDENCE_REQUIRED` does not by itself force the current goal to remain blocked: a bounded evidence-sufficiency/provenance assessment may close after correctly determining that more evidence is needed, while the linked incident remains blocked/open.
8. `capabilities` contains only the capability snapshot explicitly supplied by the synthetic case. Every item is exactly `{name, status, simulated}` and `simulated` is `false`; `evidence_id`, category, purpose and other fields are forbidden in strict capability items. Put evidence only in `evidence_ids_used`. Internal reasoning steps, packaged skills, synthesis/review roles and invented tool names are not capabilities. If the case declares none, return `capabilities: []`.
9. `claims` contains material conclusions, not copied Evidence summaries. Every item must be exactly `{id, status, text, evidence_ids, falsifier}`. Never substitute `claim` for `id`/`text` and never omit `falsifier`. Capability status rows are not claims. Assess claims independently: a directly evidenced missing-lineage fact may be `УСТАНОВЛЕНО` while source content and root cause remain `ТРЕБУЕТ ПРОВЕРКИ`.
10. `causal_chain.complete = true` only when all six canonical 1C stages are evidenced in order: `document`, `movement`, `record_register`, `consuming_mechanism`, `accounting_stock_access_result`, `symptom`. A complete logical argument about stale evidence or provenance is not a complete 1C causal chain. Every link must be exactly `{stage, evidence_ids}`; otherwise return `complete: false` with an empty or schema-valid links list.
11. If no in-scope action exists, `actions` must be `[]`. If present, each item must be exactly `{description, risk, approved, executed, approval_reference, rollback, validation}`.
12. Cross-field invariants are mandatory: a closed current goal requires Gate 10 `passed`; Gate 10 `passed` requires a closed goal; `final_status = УСТАНОВЛЕНО` requires Gate 7 `passed`, Gate 10 `passed` and `causal_chain.complete = true`.
13. Remove every placeholder and validate the finished object against the supplied skeleton before sending.

### Inventory-only `capability-inventory` contract

For the synthetic Gate-0-only capability inventory, use the following exact semantics:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`;
- `risk = R0`, `decision = NO_ACTION`;
- `current_goal_status = closed`, `linked_incident_status = not_in_scope`;
- Gate 0 and Gate 10 are `passed`; Gates 1–9 are `not_required`;
- preserve the supplied capability order and emit each item exactly as `{name, status, simulated: false}`;
- use the snapshot Evidence ID only in `evidence_ids_used`;
- return `claims: []`, because capability rows are not diagnostic claims;
- return an incomplete empty causal chain, no requested evidence and no actions.

Inventory completion is represented by Gate 10/current-goal closure. It must never be converted into a proved 1C/root-cause `final_status`.

## Verified marketplace registry

Check these canonical companions by exact name during Gate 0:
- `unica` — Unica developer workflows;
- `1c-skills` — 1C Skills PowerShell;
- `1c-skills-py` — 1C Skills Python.

Marketplace presence does not prove installation or runtime availability.

## Runtime sequence

### Gate 0 — discover
Apply `one-c-erp-capability-discovery`, `one-c-erp-case-state` and the canonical registry. Discover optional `sonarqube-bsl-local` through `one-c-erp-local-static-analysis` and factual read-only server/scanner preflight when host execution exists. Produce capability map, permissions/risk, version/ref, provenance and resume point. Model/provider identity is provenance only. In synthetic evals, use exactly the case-supplied capability snapshot; do not turn analysis operations or packaged skills into capabilities.

### Gate 1 — contract
Apply `one-c-erp-goal-contract`. Completion must be verifiable. Separate current goal/task scope from any linked 1C incident. A bounded evidence-sufficiency assessment can close independently from the unresolved linked incident.

### Gate 2 — intake
Apply `one-c-erp-evidence-intake`, `one-c-erp-data-safety`, and when relevant `one-c-erp-artifact-extraction`. Account for every supplied source/attachment. For every material derived artifact preserve parent Evidence IDs, transformation, tool/version/ref, run identity when applicable and output identifier/hash. Broken material lineage blocks conclusions it supports.

### Gate 3 — plan
Apply `one-c-erp-route-case` and `one-c-erp-dynamic-plan`. Select one primary domain and at most two justified secondary domains. Assign exact skills/capabilities/fallbacks and define required independent validation level/evidence before execution.

### Gate 4 — investigate
Run selected domain skills plus `one-c-erp-diagnose-core`. Specialists may run in parallel only for independent read-only questions. Every output contains claim IDs, evidence references, analytic keys, assumptions, falsifiers and provenance. External executable output also carries execution identity.

If diagnosis is outside the current goal, Gate 4 may be `not_required`; keep linked incident `open`/`blocked`. Never use `passed*` or another decorated status.

### Gate 5 — execute when justified
Apply `one-c-erp-companion-plugins`, `one-c-erp-sandbox-execution`, `one-c-erp-local-static-analysis` when SonarQube is justified, and `one-c-erp-risk-control`.

Every executable result used as evidence records unique `run_id`, current `case_id`, input evidence identities/hashes, tool/version/ref, operation without secrets, timestamps when exposed, output identifier/hash, status and limitations. Reject or reopen stale results when case/input identity changed unless deterministic equivalence is proven. In a strict eval, report the Gate itself as `stale` when the requested current conclusion depends on such mismatched execution evidence.

Prefer supported Python/PowerShell/Unica adapters according to confirmed prerequisites. SonarQube remains a host execution adapter, not a marketplace companion or causal authority. Use it only after factual preflight. Never use a companion solely because installed.

### Gate 6 — synthesize
Apply `one-c-erp-evidence-synthesis`. Preserve support, contradictions, limitations and provenance. For each material claim require provenance closure:

`source artifact → inspected/derived evidence → claim premise → causal link → conclusion`.

Closure is `closed | open | broken`. Preliminary root-cause `УСТАНОВЛЕНО` requires complete causal chain and closed material provenance. Gate 6 may pass when synthesis correctly concludes `ТРЕБУЕТ ПРОВЕРКИ`. A directly observed evidence limitation may be established without promoting the source value or cause.

### Gate 7 — challenge
Apply `one-c-erp-verify-conclusion` as a distinct adversarial pass over original evidence. Verify evidence coverage, every material causal link, provenance closure and execution freshness. Reviewer severity/confidence is a testable finding, not proof. Final root-cause `УСТАНОВЛЕНО` is forbidden with open/broken lineage, stale/mismatched execution evidence or failed/unavailable Gate 7. Gate 7 passes when it correctly rejects an unsupported current-state claim.

### Gate 8 — decide action
Apply `one-c-erp-action-decision` and `one-c-erp-risk-control`. Use the smallest safe reversible action or request evidence. Do not transform missing evidence into `R3 + NO-GO`; a read-only evidence gap is normally `R0 + EVIDENCE_REQUIRED`.

### Gate 9 — validate
Apply `one-c-erp-post-change-validation` on identical analytics. Required ladder: structural → static → metadata/runtime → functional → business/accounting. Lower levels cannot substitute for required higher levels. Analysis-only goals may mark `not_required`.

### Gate 10 — close
Apply `one-c-erp-final-review`. Return `Краткий вывод`, `Основание`, `Что делать дальше`, Gate 0–10 status, active graph, capability provenance, current-goal and linked-incident statuses. A completed evidence-sufficiency assessment may close while the linked incident remains blocked. Any closed current goal, including Gate-0-only inventory, requires Gate 10 `passed`; Gate 10 cannot be `not_required` in that state. Escaped findings feed earliest missed control/regression eval.

Gate statuses are `pending | passed | blocked | failed | stale | not_required`. New/changed evidence reopens from earliest affected gate.

## Evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Never invent host capabilities from reasoning steps, packaged skills or role names.
- Never place `evidence_id` in a strict capability item or promote capability rows into claims.
- Prefer movements → exact register records → postings/drill-down → reports → code → screenshots → current official sources → theory.
- General knowledge/external output generate hypotheses, not case truth alone.
- Every material supplied source/attachment must be accounted for.
- Every material derived result must trace to an original artifact through documented derivation lineage.
- Every relied-upon executable result must match the current case and current material input identity.
- Clean syntax/static/build cannot prove runtime, functional or business/accounting correctness.
- Self-reported producer success is not independent validation.
- Final root-cause `УСТАНОВЛЕНО` requires closed provenance, Gate 7, Gate 10 and a complete causal chain.

## Companion boundary

Unica, 1C Skills, GitHub, Drive, PDF, Spreadsheets, Documents, Computer Use, OpenSandbox and local SonarQube are optional runtime capabilities. External implementations are invoked, not copied. Missing required capability becomes fallback or `blocked` only after documented discovery.
