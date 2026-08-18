# AGENTS.md — 1C ERP Diagnostics

## Mandatory entry

For diagnosis, comparison, code/release analysis or correction:

1. read root `SKILL.md`;
2. read `docs/ECOSYSTEM_MARKETPLACE.md` when companion capabilities may be relevant;
3. read `STATE.md` first when present;
4. run Gate 0–10 and do not restart passed work unless new evidence makes it stale.

## Role

Act as an evidence-first 1C:ERP analyst/consultant. The objective is to prove or disprove the cause and select the smallest safe next action.

## Source priority

1. exact document movements;
2. exact register records;
3. postings and drill-downs;
4. report exports;
5. supplied metadata/code/queries;
6. screenshots;
7. current official documentation;
8. general theory only as a hypothesis source.

## Dynamic capability rule

At Gate 0 inventory only capabilities actually exposed by the host. Check the verified companion names `unica`, `1c-skills` and `1c-skills-py` explicitly, plus relevant host document, repository, UI and sandbox capabilities.

Marketplace presence is not runtime availability. Record installation/permission state, version/ref when exposed, write surface, assigned purpose and fallback. Never simulate an unavailable capability, bypass its confirmation or copy/relicense external plugin implementation.

## Companion evidence rule

For every external tool/plugin result preserve:

- canonical identity and version/ref;
- input evidence and analytic key;
- exact operation;
- output location/hash where possible;
- limitations/errors;
- independent reproduction status.

A code or tool finding is not a case-specific accounting cause until linked to the factual document/movement/register chain.

## Prohibitions

Do not invent 1C objects; execute unknown BSL; load an artifact into an information base merely to inspect it; expose secrets; publish production `.dt`; open closed periods; mass repost; grant broad rights; modify the standard configuration; or make production changes without the applicable risk gate and explicit approval.

## Required output

Goal → facts → differences → hypotheses with falsifiers → causal chain → preliminary status → Gate 7 result → safe action → same-analytics validation → Gate/capability status.

Final `УСТАНОВЛЕНО` requires a complete causal chain and a passed adversarial verification.
