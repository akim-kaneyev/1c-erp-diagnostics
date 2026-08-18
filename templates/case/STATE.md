# Case state

## Identity

- Case ID:
- Title:
- Owner:
- Updated at:
- Overall status: `open | blocked | action_pending | validating | closed`

## Goal contract

- Outcome:
- Scope:
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

## Evidence ledger

| Evidence ID | Source | Hash/identifier | What it proves | Limitations |
|---|---|---|---|---|

## Claim ledger

| Claim ID | Status | Claim | Support | Contradiction | Falsifier | Provenance |
|---|---|---|---|---|---|---|

## Actions and rollback

| Action | Risk | Approval | Expected result | Rollback | Validation |
|---|---|---|---|---|---|
