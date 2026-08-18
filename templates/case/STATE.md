# Case State

## Case ID
`YYYY-MM-DD-short-name`

## Goal contract
- Outcome:
- Verification evidence:
- In scope:
- Out of scope:
- Stop condition:

## Current status
- Overall: `NEW | IN_PROGRESS | BLOCKED | VERIFIED | CLOSED`
- Primary playbook:
- Secondary playbook (optional):

## Gate status

Use: `pending | passed | failed | stale | not_required`.

| Gate | Status | Evidence / note |
|---|---|---|
| 1 Goal contract | pending | |
| 2 Evidence intake | pending | |
| 3 Route case | pending | |
| 4 Primary diagnosis | pending | |
| 5 Sandbox/execution | pending | |
| 6 Preliminary conclusion | pending | |
| 7 Independent verification | pending | |
| 8 Action decision | pending | |
| 9 Post-change validation | pending | |
| 10 Final closure | pending | |

## Evidence set

List immutable source identifiers where possible: filename, hash, document number/date, report parameters, code revision, screenshot reference.

## Established facts

Only facts directly supported by evidence.

## Active hypotheses

For each hypothesis record:
- hypothesis;
- supporting evidence;
- contradicting evidence;
- confirm condition;
- falsify condition.

## Conclusions under verification

For each conclusion:
- ID:
- status: `УСТАНОВЛЕНО | ВЕРОЯТНО | ТРЕБУЕТ ПРОВЕРКИ`;
- evidence:
- causal chain:
- alternatives checked:
- falsifier:
- verification result:

## Changes applied

For each approved change:
- what changed;
- where;
- why;
- expected effect;
- rollback;
- validation result.

## Blind spots / missing evidence

Record the smallest evidence needed to continue.

## Resume instruction

On a new session, read this file first. Continue from the earliest gate that is `pending`, `failed`, or `stale`. Do not repeat passed gates unless new evidence invalidates them.
