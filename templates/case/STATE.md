# Case state

## Identity

- Case ID:
- Title:
- Owner:
- Updated at:
- Overall workflow status: `open | blocked | action_pending | validating | closed`
- Current goal status: `open | blocked | closed`
- Linked incident status: `not_in_scope | open | blocked | resolved`
- Closure statement:

## Goal contract

- Outcome:
- Scope:
- Linked incident:
- Completion evidence:
- Exclusions:
- Stop condition:

## Capability map

| Capability | Status | Read/write risk | Case purpose | Provenance/fallback |
|---|---|---|---|---|

## Routing and graph

- Primary domain:
- Secondary domains:

| Node | Objective | Dependencies | Capability | Risk | Status | Output/stop condition |
|---|---|---|---|---|---|---|

## Gate status

| Gate | Status | Evidence/result |
|---|---|---|
| 0 Capability/state discovery | pending | |
| 1 Goal contract | pending | |
| 2 Evidence intake | pending | |
| 3 Dynamic plan | pending | |
| 4 Specialist analysis | pending | |
| 5 Executable validation | pending | |
| 6 Evidence synthesis | pending | |
| 7 Adversarial verification | pending | |
| 8 Action decision | pending | |
| 9 Post-change validation | pending | |
| 10 Final closure | pending | |

Allowed gate status: `pending | passed | blocked | failed | stale | not_required`.

Do not use decorated values such as `passed*`. When a gate is outside the current goal, use `not_required` and record any unresolved linked incident separately.

## Evidence ledger

| Evidence ID | Source | Hash/identifier | What it proves | Limitations |
|---|---|---|---|---|

## Claim ledger

| Claim ID | Status | Claim | Support | Contradiction | Falsifier | Provenance |
|---|---|---|---|---|---|---|

## Actions and rollback

| Action | Risk | Approval | Expected result | Rollback | Validation |
|---|---|---|---|---|---|
