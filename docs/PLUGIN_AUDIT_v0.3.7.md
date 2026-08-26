# Plugin and ecosystem self-audit — v0.3.7 Release Candidate

Audit target: optional post-verification Visual Explanation with no change to diagnostic or strict-evaluation semantics.

Pre-release audit result: **No known critical control is `FAIL`; protected CI/CodeQL and exact-version v0.3.7 runtime evidence remain pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions synchronized at 0.3.7 | PASS | Manifest, pyproject, validators and tests use one patch version. |
| 2 | Gate 0–10 semantics unchanged | PASS | No Gate, status, causal-chain or action contract was added or modified. |
| 3 | Presentation prerequisite is explicit | PASS | Visual Explanation requires passed Gate 6 and passed Gate 7. |
| 4 | Exactly two modes | PASS | Only `diagram` and `sticky` are documented and tested. |
| 5 | Reviewed source ledger preserved | PASS | Views retain existing Claim/Evidence IDs and final statuses; gaps remain gaps. |
| 6 | Non-evidentiary boundary | PASS | The sidecar creates no Evidence ID, claim support, causal edge or provenance closure. |
| 7 | Capability boundary | PASS | Capability discovery excludes Visual Explanation and its modes from Gate 0. |
| 8 | Strict evaluation exclusion | PASS | `EVAL_RESULT_JSON` admits no Visual-Explanation-derived field, prose, capability, claim or action. |
| 9 | Schema and cases unchanged | PASS | Result schema, suite and Gate expectations have no visual extension. |
| 10 | Packaged skill inventory unchanged | PASS | 32 packaged skills; presentation remains inside existing orchestrator/final-review surfaces. |
| 11 | Marketplace identity and immutable pins unchanged | PASS | Four entries and reviewed SHAs retained. |
| 12 | Privacy/write surface unchanged | PASS | Inline Markdown only; no renderer, telemetry, persistence or external write. |
| 13 | Velis assets unchanged | PASS | Existing approved assets retained. |
| 14 | Public package, lock, history, eval and unit validation | PENDING | Requires protected Pull Request CI. |
| 15 | Python 3.10/3.12 and CodeQL | PENDING | Requires protected Pull Request checks. |
| 16 | Installed normal and strict smoke checks | PENDING | Requires clean sessions with exact v0.3.7. |
| 17 | Complete hashed 16-case runtime acceptance | PENDING | Requires `validate_runtime_run.py`. |

## Conclusion

The candidate isolates Visual Explanation as a one-way presentation sidecar over the reviewed ledger. Repository readiness is not runtime acceptance; the installed v0.3.7 package must still pass the documented normal/strict smoke checks and full clean-session suite.
