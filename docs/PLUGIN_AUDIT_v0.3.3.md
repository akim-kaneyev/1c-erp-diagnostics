# Plugin and ecosystem self-audit — v0.3.3 Release Candidate

Audit target: the strict `EVAL_RESULT_JSON` runtime-contract correction after the installed v0.3.2 stale-execution smoke test.

Pre-release audit result: **No known critical control is `FAIL`; protected CI/CodeQL and exact-version runtime evidence remain pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions are synchronized at 0.3.3 | PASS | Manifest, pyproject, validators and tests use one patch version. |
| 2 | Strict eval output is one JSON object with exact skeleton fields | PASS | Authoritative, packaged, portable and final-review contracts explicitly prohibit prose, extra/missing/renamed fields and placeholder leakage. |
| 3 | Gate statuses remain canonical | PASS | Only `pending | passed | blocked | failed | stale | not_required` are allowed; upper-case, combined and custom values are prohibited. |
| 4 | Gate procedure status is separated from claim proof status | PASS | Gate 6/7 may pass after correctly rejecting an unsupported conclusion while Gate 10 stays blocked. |
| 5 | Action risk is separated from evidentiary severity | PASS | Read-only stale-evidence rejection is explicitly `R0`; `R3` requires an in-scope write surface. |
| 6 | `EVIDENCE_REQUIRED` is separated from `NO-GO` | PASS | Missing current evidence/rerun/equivalence uses the evidence decision; `NO-GO` blocks an unsafe/unapproved action. |
| 7 | Linked-incident scope is controlled | PASS | `not_in_scope` requires explicit exclusion; unresolved relevant incidents remain `blocked`/`open`. |
| 8 | Claim/link/action item schemas are explicit | PASS | Exact field sets are specified; string arrays and renamed claim fields are prohibited. |
| 9 | Causal-chain completeness retains 1C meaning | PASS | `complete=true` requires all six canonical 1C stages in order; logical freshness reasoning is insufficient. |
| 10 | Marketplace identity/composition and companion pins are unchanged | PASS | Four entries; Unica `aefc880f9bab606a5c55ed11af563b740054a549`, PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`, Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`. |
| 11 | Packaged skills and Velis assets are unchanged | PASS | 32 skills; approved composer/card/dark assets retained. |
| 12 | Local repository validators/regressions pass | PENDING | Requires CI execution on the release Pull Request. |
| 13 | Python 3.10/3.12 and CodeQL pass | PENDING | Requires protected Pull Request checks. |
| 14 | Exact installed v0.3.3 stale/provenance smoke tests pass | PENDING | Must be repeated in a new clean chat after marketplace refresh. |
| 15 | Complete clean-session runtime acceptance passes | PENDING | Requires all 16 case results and strict hashed run manifest. |

## Observed v0.3.2 runtime finding

The installed v0.3.2 model correctly determined that `R-OLD / RUN-OLD / INPUT-OLD` could not prove `INPUT-CURRENT` and set Gate 5 to `stale`. However, the returned JSON failed the published contract by using `R3`, `NO-GO`, `not_in_scope`, malformed claim/link/action structures and `causal_chain.complete=true`. The defect is therefore a format/semantic-classification defect, not a failure to detect stale evidence.

## Scope of correction

This hotfix changes instructions and regression contracts only. It does not add a new agent, skill, tool, network service, write capability or external dependency. It does not alter the 16 hidden eval expectations.

## Conclusion

The candidate addresses every reproduced v0.3.2 strict-output deviation at the earliest applicable runtime instruction and adds regression assertions. Repository readiness cannot be marked complete until protected CI and CodeQL pass. Runtime acceptance cannot be claimed until the installed v0.3.3 package returns validator-conformant JSON in a clean session.
