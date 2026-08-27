---
name: one-c-erp-case-state
description: Maintain resumable Gate 1-10 state for a 1C:ERP investigation across long sessions and project handoffs.
---

# Case state

Track: goal contract; overall status; primary/secondary domain; Gate 1-10 status; evidence set; established facts; active hypotheses with confirm/falsify conditions; conclusions under verification; changes applied; blind spots.

Initialize the ID-bearing integrity surface from the [bundled machine-state template](assets/STATE.json), persist the working copy in the case workspace, and validate it with [the state-integrity contract](references/state-integrity.md) before resume and Gate 10. `STATE.md` is the human journal, not a substitute for the machine state.

Gate statuses: `pending | passed | blocked | failed | stale | not_required`.

Resume from the earliest non-final gate. Do not repeat passed work unless new evidence invalidates it. Mismatched run identity, supersession or explicit invalidation propagates through derived evidence, claims, documents/reports and the earliest affected downstream Gate. A case is closed only when every required gate is `passed` or `not_required` and the state validator passes.
