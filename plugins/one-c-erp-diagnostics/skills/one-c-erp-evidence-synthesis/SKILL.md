---
name: one-c-erp-evidence-synthesis
description: Merge specialist outputs into a claim-to-evidence graph while preserving contradictions, uncertainty and provenance.
---

# Evidence synthesis

Use at Gate 6.

Build a claim ledger:

- claim ID;
- statement;
- status: fact, interpretation, hypothesis or missing evidence;
- supporting evidence IDs;
- contradicting evidence IDs;
- consuming mechanism;
- alternatives tested;
- falsifier;
- specialist/capability provenance;
- provenance closure status: `closed | open | broken`.

## Provenance closure contract

For every material claim, trace each material premise and causal link back to either:

1. original source evidence with a stable identifier/hash where available; or
2. derived evidence whose `derived_from`, transformation, tool/version and execution record link it to its parent artifact.

The required closure is:

`source artifact → inspected/derived evidence → claim premise → causal link → conclusion`.

A list of evidence IDs is not sufficient if the transition between them is inferred but not demonstrated. Mark closure `open` when a required link still needs evidence and `broken` when a relied-upon derived result has no recoverable parent/transformation identity.

Claim status is assessed per statement. A directly evidenced limitation such as “the supplied derived artifact has no declared parent/transformation/run/output identity” may be `УСТАНОВЛЕНО`, while the source value, source-to-derived relationship and business/root-cause conclusion remain `ТРЕБУЕТ ПРОВЕРКИ`. Do not downgrade an observed evidence limitation merely because the larger causal conclusion is unproved, and do not promote the larger conclusion from the established limitation.

A preliminary root-cause `УСТАНОВЛЕНО` requires both a complete causal chain and `closed` provenance closure for every material causal link, but remains preliminary until Gate 7 passes.

For accounting/proportional claims, synthesis also requires a PASS helper Evidence traced to primary rows. Preserve the five effect flags as fields of that Evidence rather than adding fields to strict `EVAL_RESULT_JSON`. One calculated total copied into multiple reports is one derived source, not independent corroboration.

Deduplicate equivalent claims but never erase disagreement. Resolve conflicts by returning to original evidence and analytic keys, not by majority vote or specialist confidence.
