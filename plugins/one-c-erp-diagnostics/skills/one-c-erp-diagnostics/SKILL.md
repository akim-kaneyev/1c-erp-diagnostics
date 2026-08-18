---
name: one-c-erp-diagnostics
description: Single dynamic entrypoint for evidence-first Gate 0-10 orchestration across 1C:ERP data, code, releases and controlled actions.
---

# Master orchestrator

Run Gate 0 through Gate 10 in order. Internally invoke/apply packaged specialist skills and optional companion capabilities. The user must not manually chain them.

## Runtime sequence

### Gate 0 — discover
Apply `one-c-erp-capability-discovery` and `one-c-erp-case-state`. Produce a capability map and resume point.

### Gate 1 — contract
Apply `one-c-erp-goal-contract`. Completion must be verifiable.

### Gate 2 — intake
Apply `one-c-erp-evidence-intake`, `one-c-erp-data-safety`, and when relevant `one-c-erp-artifact-extraction`.

### Gate 3 — plan
Apply `one-c-erp-route-case` and `one-c-erp-dynamic-plan`. Select one primary domain and at most two justified secondary domains.

### Gate 4 — investigate
Run the selected domain skills plus `one-c-erp-diagnose-core`. Specialists may run in parallel only for independent read-only questions. Every output must contain claim IDs, evidence references, assumptions and falsifiers.

### Gate 5 — execute when justified
Apply `one-c-erp-companion-plugins`, `one-c-erp-sandbox-execution` and `one-c-erp-risk-control`. Never use a companion solely because it is installed.

### Gate 6 — synthesize
Apply `one-c-erp-evidence-synthesis`. Contradictions stay visible.

### Gate 7 — challenge
Apply `one-c-erp-verify-conclusion` as a distinct adversarial pass with access to original evidence. Final `УСТАНОВЛЕНО` is forbidden otherwise.

### Gate 8 — decide action
Apply `one-c-erp-action-decision` and `one-c-erp-risk-control`. Use the smallest safe reversible action.

### Gate 9 — validate
Apply `one-c-erp-post-change-validation` on identical analytics. Analysis-only goals may explicitly mark this gate `not_required`.

### Gate 10 — close
Apply `one-c-erp-final-review`. Return `Краткий вывод`, `Основание`, `Что делать дальше`, Gate 0–10 status and capability provenance.

## Evidence rules

- Never invent 1C metadata objects, registers, fields, roles, documents or settings.
- Prefer movements → exact register records → postings/drill-down → reports → code → screenshots → current official sources → theory.
- General knowledge and external plugin output generate hypotheses; they do not prove the case alone.
- A disappearing UI error is not proof of accounting correctness.

## Companion boundary

Unica, 1C Skills (Python/PowerShell), GitHub, Drive, PDF, Spreadsheets, Documents, Computer Use and OpenSandbox are optional companions. Discover them at runtime. Do not copy their private implementation, declare fabricated dependencies or imply availability when the host does not expose them.
