---
name: one-c-erp-risk-control
description: Classify and control the blast radius of tools and proposed changes in 1C:ERP diagnostics.
---

# Risk control

Use before every executable or write action.

## Levels

- `R0` read-only inspection, reasoning, comparison or refusal to rely on invalid/stale evidence.
- `R1` generated local derivatives, manifests, reports or test scripts.
- `R2` reversible change in a disposable sandbox or test information base.
- `R3` production data, accounting records, rights, closed periods, mass reposting, configuration or external-system writes.

Risk classifies the blast radius of the actual or proposed action. It does not classify how serious an incident is, how uncertain a conclusion is, or how harmful a wrong evidentiary decision could be. A read-only assessment that rejects stale evidence remains `R0`. Use `R3` only when the in-scope action itself can change production/accounting/access/closed-period state.

## Required controls

R0: provenance and no secret exposure.

R1: output path, input hashes and cleanup/rollback.

R2: isolated environment, snapshot/backup, expected result and rollback test.

R3: explicit user approval for the exact action, affected scope, standard-mechanism justification, rollback, responsible operator and Gate 9 validation plan.

Never lower a risk level to make execution easier. When the action surface is genuinely uncertain, use the higher level; do not raise risk merely because evidence is incomplete.
