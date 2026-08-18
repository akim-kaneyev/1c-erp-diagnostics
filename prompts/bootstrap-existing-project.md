# Bootstrap existing 1C:ERP project into the diagnostics workflow

Use this when a project/chat/case already exists and contains prior conclusions, files or partial analysis.

## Objective

Adopt the repository workflow without discarding useful prior work or repeating completed investigation.

## Procedure

1. Read root `SKILL.md` and `AGENTS.md`.
2. Inventory the existing project materials and prior conclusions.
3. Create/update a case `STATE.md` from `templates/case/STATE.md`.
4. Map prior work to workflow gates:
   - mark a gate `passed` only if its required evidence is actually present;
   - mark unsupported prior conclusions `stale` or `pending` rather than accepting them by history;
   - record prior actions and their observed results.
5. Run the goal contract quality check.
6. Route the case through `playbooks/router.md`.
7. Continue from the earliest gate that is `pending`, `failed` or `stale`.
8. Before relying on an old conclusion, run the independent verification gate.
9. Do not re-run passed work unless new evidence can invalidate it.
10. End by updating `STATE.md` so the next session can resume deterministically.

## Required bootstrap output

- current goal and success validator;
- selected playbook;
- evidence inventory;
- gate status table;
- prior conclusions classified as verified / unverified / stale;
- exact next gate and action.
