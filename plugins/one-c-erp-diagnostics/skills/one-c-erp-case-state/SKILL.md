---
name: one-c-erp-case-state
description: Maintain resumable Gate 1-10 state for a 1C:ERP investigation across long sessions and project handoffs.
---

# Case state

Track: goal contract; overall status; primary/secondary domain; Gate 1-10 status; evidence set; established facts; active hypotheses with confirm/falsify conditions; conclusions under verification; changes applied; blind spots.

Gate statuses: `pending | passed | blocked | failed | stale | not_required`.

Resume from the earliest non-final gate. Do not repeat passed work unless new evidence invalidates it. A case is closed only when every required gate is `passed` or `not_required`.
