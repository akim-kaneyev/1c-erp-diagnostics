---
name: one-c-erp-diagnostics
description: Single dynamic entrypoint for evidence-first Gate 0-10 orchestration across 1C:ERP data, code, releases, a verified Unica/1C Skills ecosystem and controlled actions.
---

# Master orchestrator

Run Gate 0 through Gate 10 in order. Internally apply packaged specialist skills and installed companion capabilities. The user must not manually chain them.

This orchestrator is a provider-neutral harness around the available model: correctness comes from the Gate contract, evidence coverage, tool/capability provenance, an inspect → hypothesize → test → compare loop and independent validation. Model confidence or provider identity never substitutes for evidence.

## Verified marketplace registry

Check these canonical companions by exact name during Gate 0:

- `unica` — Unica developer workflows;
- `1c-skills` — 1C Skills PowerShell;
- `1c-skills-py` — 1C Skills Python.

The repository marketplace exposes them together, but each remains separately installed and permissioned. Do not treat marketplace presence as runtime availability.

## Runtime sequence

### Gate 0 — discover
Apply `one-c-erp-capability-discovery`, `one-c-erp-case-state` and the canonical registry above. Discover the optional host capability `sonarqube-bsl-local` without treating it as a marketplace plugin. A dedicated SonarQube tool is not required: when local execution and loopback HTTP exist, perform the factual read-only server/scanner preflight instead of classifying from the tool list. Produce a capability map, permission/risk surface, version/ref where exposed and resume point. Record model/provider identity only as provenance when exposed; do not change acceptance rules by provider.

### Gate 1 — contract
Apply `one-c-erp-goal-contract`. Completion must be verifiable. Separate the current goal/task scope from any linked 1C incident that may remain unresolved.

### Gate 2 — intake
Apply `one-c-erp-evidence-intake`, `one-c-erp-data-safety`, and when relevant `one-c-erp-artifact-extraction`. Account for every supplied source/attachment with an explicit disposition. Gate 2 cannot pass while material supplied evidence is silently unexamined.

### Gate 3 — plan
Apply `one-c-erp-route-case` and `one-c-erp-dynamic-plan`. Select one primary domain and at most two justified secondary domains. Assign an exact internal skill or canonical companion to every node and define a fallback. For every material claim/change define the required validation level and independent acceptance evidence before execution.

### Gate 4 — investigate
Run the selected domain skills plus `one-c-erp-diagnose-core`. Specialists may run in parallel only for independent read-only questions. Every output must contain claim IDs, evidence references, analytic keys, assumptions, falsifiers and capability provenance.

If diagnosis is explicitly outside the current goal, mark Gate 4 `not_required` for that goal and keep the linked incident `open` or `blocked`. Never use `passed*` or another decorated status.

### Gate 5 — execute when justified
Apply `one-c-erp-companion-plugins`, `one-c-erp-sandbox-execution` and `one-c-erp-risk-control`.

- Prefer `1c-skills-py` for supported cross-platform artifact operations.
- Prefer `1c-skills` for confirmed Windows/1C runtime operations.
- Use Unica for developer workflows, code navigation and controlled build/test work when exposed.
- Use `one-c-erp-local-static-analysis` for an explicitly authorized sanitized BSL scan only after its loopback, version, plugin/profile, project and authentication preflight passes.
- Never use a companion solely because it is installed.

### Gate 6 — synthesize
Apply `one-c-erp-evidence-synthesis`. Preserve supporting and contradicting evidence, plugin/tool provenance and limitations. Contradictions stay visible.

### Gate 7 — challenge
Apply `one-c-erp-verify-conclusion` as a distinct adversarial pass with access to original evidence. Final `УСТАНОВЛЕНО` is forbidden otherwise, including when the preliminary conclusion came from an external plugin. A reviewer label such as `critical` or `blocking` is a testable finding, not proof of a defect, until reproduced or linked to case evidence.

### Gate 8 — decide action
Apply `one-c-erp-action-decision` and `one-c-erp-risk-control`. Use the smallest safe reversible action.

### Gate 9 — validate
Apply `one-c-erp-post-change-validation` on identical analytics. Use the required validation ladder: structural → static → metadata/runtime → functional → business/accounting. A lower validation level cannot substitute for a required higher one. Analysis-only goals may explicitly mark this gate `not_required`.

### Gate 10 — close
Apply `one-c-erp-final-review`. Return `Краткий вывод`, `Основание`, `Что делать дальше`, Gate 0–10 status, active specialist graph, capability provenance, current-goal status and linked-incident status. When a defect or material omission escaped an earlier control, record the earliest missed gate and convert it into a regression eval/checklist improvement when reproducible.

Gate status values are limited to `pending | passed | blocked | failed | stale | not_required`; decorated variants such as `passed*` are prohibited.

A narrow safety-assessment goal may close while the linked incident remains open, but the response must state both statuses explicitly. If diagnosis or correction is part of the current goal, any required unresolved gate prevents Gate 10 from passing.

## Evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Prefer movements → exact register records → postings/drill-down → reports → code → screenshots → current official sources → theory.
- General knowledge and external plugin output generate hypotheses; they do not prove the case alone.
- A disappearing UI error is not proof of accounting correctness.
- Completion of a narrow assessment is not closure of the underlying incident.
- Every material supplied source/attachment must be accounted for before a conclusion it could falsify becomes final.
- Clean syntax, static analysis or a successful build cannot prove a 1C runtime, functional or business/accounting result.
- Self-reported success by the producing specialist is not independent validation.

## Companion boundary

Unica, 1C Skills, GitHub, Drive, PDF, Spreadsheets, Documents, Computer Use, OpenSandbox and local SonarQube are optional runtime capabilities. SonarQube remains a host execution adapter and is not added to the marketplace registry. Do not copy external implementation, bypass installation/permissions or declare fabricated app/MCP dependencies. For SonarQube, the host execution surface plus a successful factual preflight is the evidence; the absence of a named MCP/app tool is not. A missing required capability becomes fallback or `blocked` only after the documented discovery attempt.
