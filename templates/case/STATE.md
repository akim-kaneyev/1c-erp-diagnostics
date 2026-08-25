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

## Evidence coverage

Every supplied attachment/source must be accounted for before Gate 2 passes.

| Source/attachment | Evidence ID | Disposition | Inspection method | Result/limitation |
|---|---|---|---|---|

Allowed dispositions: `examined | unreadable | duplicate | irrelevant_with_reason | blocked`.

## Evidence ledger and derivation lineage

| Evidence ID | Source | Hash/identifier | Derived from | Transformation/tool/version | Run ID | Output hash | What it proves | Limitations |
|---|---|---|---|---|---|---|---|---|

For source evidence, `Derived from`, transformation and Run ID may be empty. For derived evidence they are required when materially relevant. A derived result with no traceable parent artifact cannot by itself establish a final cause.

## Execution records

Use for executable Gate 5 evidence and any external tool output relied upon later.

| Run ID | Case ID | Tool/version/ref | Input evidence + hashes | Started/completed | Output identifier/hash | Status | Limitations |
|---|---|---|---|---|---|---|---|

If current inputs no longer match an execution record, mark dependent evidence/claims `stale` and reopen from the earliest affected gate.

## Routing and graph

- Primary domain:
- Secondary domains:

| Node | Objective | Dependencies | Capability | Risk | Validation level | Status | Output/stop condition |
|---|---|---|---|---|---|---|---|

## Independent verification plan

| Claim/change | Required validation level | Method | Independent evidence | Expected result/falsifier | Status |
|---|---|---|---|---|---|

Validation levels: `structural | static | metadata_runtime | functional | business_accounting`.

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

## Claim ledger

| Claim ID | Status | Claim | Support | Contradiction | Falsifier | Provenance closure |
|---|---|---|---|---|---|---|

For a material `УСТАНОВЛЕНО` claim, `Provenance closure` must trace every material premise/causal link back to original evidence or a documented derivation chain. `open` or `broken` closure blocks final establishment.

## Actions and rollback

| Action | Risk | Approval | Expected result | Rollback | Validation |
|---|---|---|---|---|---|

## Escaped/missed finding feedback

Use this section only when a defect, contradiction or material omission survives a prior control. Feed the lesson back into the earliest gate that could have caught it and add a regression eval/checklist when reproducible.

| Finding | Where it escaped | Why the control missed it | Earliest gate/control to improve | Regression eval/checklist |
|---|---|---|---|---|
