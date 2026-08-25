---
name: one-c-erp-action-decision
description: Select the smallest safe reversible action after a 1C:ERP cause has been verified or define the next evidence request when it has not.
---

# Action decision

Use for Gate 8.

## Decision semantics

- `EVIDENCE_REQUIRED` — the requested conclusion/current state cannot be established without additional current evidence, a rerun, or proved input equivalence.
- `NO-GO` — an actual in-scope proposed action is prohibited, unapproved or missing mandatory controls.
- `NO_ACTION` — the task is complete without an action and no additional evidence is required for the declared goal.
- `GO` — a specifically scoped action is authorized by the applicable risk gate and may proceed.

Do not return `NO-GO` merely because evidence is insufficient. Rejecting a stale report in a read-only analysis normally produces `R0 + EVIDENCE_REQUIRED`, not `R3 + NO-GO`.

Priority for an approved corrective action:
1. proven standard configuration/NSI correction;
2. standard 1C document/mechanism;
3. correction of the actual source document in an allowed period;
4. specialized/manual correction only when standard mechanisms are unsuitable and consequences are understood.

Before a production-changing action state expected accounting effect, scope, rollback and validation plan. Do not automatically open closed periods, mass repost, grant broad rights or modify the standard configuration.
