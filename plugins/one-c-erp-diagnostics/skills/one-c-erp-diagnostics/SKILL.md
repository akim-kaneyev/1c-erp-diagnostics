---
name: one-c-erp-diagnostics
description: Single dynamic entrypoint for evidence-first Gate 0-10 orchestration across 1C:ERP data, code, releases, a verified Unica/1C Skills ecosystem and controlled actions.
---

# Master orchestrator

Run Gate 0 through Gate 10 in order. Internally apply packaged specialist skills and installed companion capabilities. The user must not manually chain them.

This orchestrator is a provider-neutral harness around the available model: correctness comes from the Gate contract, evidence coverage, artifact/provenance closure, execution identity, tool/capability provenance, an inspect → hypothesize → test → compare loop and independent validation. Model confidence or provider identity never substitutes for evidence.

## Verified marketplace registry

Check these canonical companions by exact name during Gate 0:
- `unica` — Unica developer workflows;
- `1c-skills` — 1C Skills PowerShell;
- `1c-skills-py` — 1C Skills Python.

Marketplace presence does not prove installation or runtime availability.

## Runtime sequence

### Gate 0 — discover
Apply `one-c-erp-capability-discovery`, `one-c-erp-case-state` and the canonical registry. Discover optional `sonarqube-bsl-local` through factual read-only server/scanner preflight when host execution exists. Produce capability map, permissions/risk, version/ref, provenance and resume point. Model/provider identity is provenance only.

### Gate 1 — contract
Apply `one-c-erp-goal-contract`. Completion must be verifiable. Separate current goal/task scope from any linked 1C incident.

### Gate 2 — intake
Apply `one-c-erp-evidence-intake`, `one-c-erp-data-safety`, and when relevant `one-c-erp-artifact-extraction`. Account for every supplied source/attachment. For every material derived artifact preserve parent Evidence IDs, transformation, tool/version/ref, run identity when applicable and output identifier/hash. Broken material lineage blocks conclusions it supports.

### Gate 3 — plan
Apply `one-c-erp-route-case` and `one-c-erp-dynamic-plan`. Select one primary domain and at most two justified secondary domains. Assign exact skills/capabilities/fallbacks and define required independent validation level/evidence before execution.

### Gate 4 — investigate
Run selected domain skills plus `one-c-erp-diagnose-core`. Specialists may run in parallel only for independent read-only questions. Every output contains claim IDs, evidence references, analytic keys, assumptions, falsifiers and provenance. External executable output also carries execution identity.

If diagnosis is outside the current goal, Gate 4 may be `not_required`; keep linked incident `open`/`blocked`. No decorated statuses.

### Gate 5 — execute when justified
Apply `one-c-erp-companion-plugins`, `one-c-erp-sandbox-execution` and `one-c-erp-risk-control`.

Every executable result used as evidence records unique `run_id`, current `case_id`, input evidence identities/hashes, tool/version/ref, operation without secrets, timestamps when exposed, output identifier/hash, status and limitations. Reject or reopen stale results when case/input identity changed unless deterministic equivalence is proven.

Prefer supported Python/PowerShell/Unica adapters according to confirmed prerequisites. Use SonarQube only after factual preflight. Never use a companion solely because installed.

### Gate 6 — synthesize
Apply `one-c-erp-evidence-synthesis`. Preserve support, contradictions, limitations and provenance. For each material claim require provenance closure:

`source artifact → inspected/derived evidence → claim premise → causal link → conclusion`.

Closure is `closed | open | broken`. Preliminary `УСТАНОВЛЕНО` requires complete causal chain and closed material provenance.

### Gate 7 — challenge
Apply `one-c-erp-verify-conclusion` as a distinct adversarial pass over original evidence. Verify evidence coverage, every material causal link, provenance closure and execution freshness. Reviewer severity/confidence is a testable finding, not proof. Final `УСТАНОВЛЕНО` is forbidden with open/broken lineage, stale/mismatched execution evidence or failed/unavailable Gate 7.

### Gate 8 — decide action
Apply `one-c-erp-action-decision` and `one-c-erp-risk-control`. Use the smallest safe reversible action.

### Gate 9 — validate
Apply `one-c-erp-post-change-validation` on identical analytics. Required ladder: structural → static → metadata/runtime → functional → business/accounting. Lower levels cannot substitute for required higher levels. Analysis-only goals may mark `not_required`.

### Gate 10 — close
Apply `one-c-erp-final-review`. Return `Краткий вывод`, `Основание`, `Что делать дальше`, Gate 0–10 status, active graph, capability provenance, current-goal and linked-incident statuses. Escaped findings feed earliest missed control/regression eval.

Gate statuses are `pending | passed | blocked | failed | stale | not_required`. New/changed evidence reopens from earliest affected gate.

## Evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Prefer movements → exact register records → postings/drill-down → reports → code → screenshots → current official sources → theory.
- General knowledge/external output generate hypotheses, not case truth alone.
- Every material supplied source/attachment must be accounted for.
- Every material derived result must trace to an original artifact through documented derivation lineage.
- Every relied-upon executable result must match the current case and current material input identity.
- Clean syntax/static/build cannot prove runtime, functional or business/accounting correctness.
- Self-reported producer success is not independent validation.
- Final `УСТАНОВЛЕНО` requires closed provenance and Gate 7.

## Companion boundary

Unica, 1C Skills, GitHub, Drive, PDF, Spreadsheets, Documents, Computer Use, OpenSandbox and local SonarQube are optional runtime capabilities. External implementations are invoked, not copied. Missing required capability becomes fallback or `blocked` only after documented discovery.
