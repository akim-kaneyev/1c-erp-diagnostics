---
name: one-c-erp-risk-control
description: Classify and control the blast radius of tools and proposed changes in 1C:ERP diagnostics.
---

# Risk control

Use before every executable or write action.

## Levels

- `R0` read-only inspection.
- `R1` generated local derivatives, manifests, reports or test scripts.
- `R2` reversible change in a disposable sandbox or test information base.
- `R3` production data, accounting records, rights, closed periods, mass reposting, configuration or external-system writes.

## Required controls

R0: provenance and no secret exposure.

R1: output path, input hashes and cleanup/rollback.

R2: isolated environment, snapshot/backup, expected result and rollback test.

R3: explicit user approval for the exact action, affected scope, standard-mechanism justification, rollback, responsible operator and Gate 9 validation plan.

Never lower a risk level to make execution easier. When uncertainty exists, use the higher level.
