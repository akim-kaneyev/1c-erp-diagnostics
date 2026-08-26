# Plugin and ecosystem self-audit — v0.3.4 Release Candidate

Audit target: the provenance-scope and deterministic synthetic capability-snapshot correction after the installed v0.3.3 priority smoke tests.

Pre-release audit result: **No known critical control is `FAIL`; protected CI/CodeQL and exact-version v0.3.4 runtime evidence remain pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions are synchronized at 0.3.4 | PASS | Manifest, pyproject, validators and tests use one patch version. |
| 2 | v0.3.3 stale-execution correction is preserved | PASS | Canonical stale result remains `R0`, `EVIDENCE_REQUIRED`, linked incident blocked, Gate 5 stale, Gate 7 passed, Gate 10 blocked, exact schema, false causal-chain completeness and empty actions/capabilities. |
| 3 | Synthetic capability snapshot is authoritative | PASS | Strict orchestrators and capability-discovery skill prohibit invented internal reasoning/skill/reviewer capabilities. |
| 4 | Empty synthetic capability snapshot remains empty | PASS | Rendered prompt explicitly requires `capabilities: []`; validator rejects every unexpected capability. |
| 5 | Declared synthetic capabilities cannot be omitted or changed | PASS | Validator compares exact capability names and statuses against the case snapshot. |
| 6 | Current-goal and linked-incident closure are separated | PASS | A bounded evidence-sufficiency assessment may close while the unresolved linked incident remains blocked/open. |
| 7 | `not_in_scope` remains explicit-only | PASS | Missing provenance/source/root-cause evidence cannot itself move the linked incident out of scope. |
| 8 | Claim status is statement-specific | PASS | Directly evidenced missing lineage may be established without proving source content, derivation relation or root cause. |
| 9 | Canonical provenance eval expectation is aligned | PASS | Current goal closed; linked incident blocked; Gate 2/6/7/8/10 passed; at most one established limitation; capability snapshot empty. |
| 10 | Runtime regressions cover reproduced v0.3.3 output | PASS | The reproduced `not_in_scope` plus invented-capabilities result is explicitly rejected. |
| 11 | Marketplace identity/composition and companion pins are unchanged | PASS | Four entries; Unica `aefc880f9bab606a5c55ed11af563b740054a549`, PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`, Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`. |
| 12 | Packaged skills and Velis assets are unchanged | PASS | 32 skills; approved composer/card/dark assets retained. |
| 13 | Local repository validators/regressions pass | PENDING | Requires CI execution on the release Pull Request. |
| 14 | Python 3.10/3.12 and CodeQL pass | PENDING | Requires protected Pull Request checks. |
| 15 | Exact installed v0.3.4 priority smoke tests pass | PENDING | Must be repeated in new clean chats after marketplace refresh. |
| 16 | Complete clean-session runtime acceptance passes | PENDING | Requires all 16 case results and strict hashed run manifest. |

## Observed v0.3.3 runtime findings

The installed v0.3.3 package passed the canonical stale-execution case. The canonical provenance-closure test correctly refused to use D-1 as proof of S-1 content or causality, returned `R0`, `EVIDENCE_REQUIRED`, canonical Gate values and a false six-stage causal chain. However, it incorrectly marked the unresolved linked issue `not_in_scope` and invented internal analysis/review operations as capabilities.

The same output established a valid methodological distinction: E-PROV-2 directly proves that the supplied D-1 lacks the declared lineage identifiers. That evidence limitation can be established independently from the still-unproved source value and root cause. The v0.3.4 eval expectation now reflects this distinction rather than forcing zero established claims.

## Scope of correction

This hotfix changes instructions, eval semantics, validation and regression contracts only. It does not add a new agent, packaged skill, external tool, network service, write capability or dependency. It does not modify the verified companion pins or approved Velis assets.

## Conclusion

The candidate addresses every reproduced v0.3.3 provenance-scope/capability deviation at the earliest applicable controls and makes the validator enforce the exact synthetic capability snapshot. Repository readiness cannot be marked complete until protected CI and CodeQL pass. Runtime acceptance cannot be claimed until the installed v0.3.4 package returns validator-conformant results in clean sessions and the complete 16-case hashed run passes.
