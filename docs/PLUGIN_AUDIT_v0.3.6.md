# Plugin and ecosystem self-audit — v0.3.6 Release Candidate

Audit target: the exact stale-execution output correction after installed v0.3.5
passed capability inventory but failed the next canonical runtime case.

Pre-release audit result: **No known critical control is `FAIL`; protected CI/CodeQL
and exact-version v0.3.6 runtime evidence remain pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions synchronized at 0.3.6 | PASS | Manifest, pyproject, validators and tests use one patch version. |
| 2 | Capability-inventory v0.3.5 correction preserved | PASS | Canonical inventory result remains exact and claim-free. |
| 3 | Old run/input result is stale for current input | PASS | Gate 5 exact profile is `stale`, not `passed`. |
| 4 | Adversarial stale rejection is explicit | PASS | Gate 7 must pass after rejecting reuse. |
| 5 | Current-state goal cannot close without current evidence | PASS | Gate 10 and both scopes remain blocked. |
| 6 | Claim schema/status is exact | PASS | One non-established `{id,status,text,evidence_ids,falsifier}` claim. |
| 7 | Logical run graph is not 1C causal chain | PASS | `complete=false`, links empty. |
| 8 | Evidence request and actions are exact | PASS | One string request; no pseudo-actions. |
| 9 | Exact v0.3.5 runtime regression exists | PASS | Reproduced response is rejected by executable tests. |
| 10 | Marketplace identity and immutable pins unchanged | PASS | Four entries and reviewed SHAs retained. |
| 11 | Packaged skills and Velis assets unchanged | PASS | 32 skills and approved assets retained. |
| 12 | Public package, lock, history, eval and unit validation | PENDING | Requires protected Pull Request CI. |
| 13 | Python 3.10/3.12 and CodeQL | PENDING | Requires protected Pull Request checks. |
| 14 | Exact installed v0.3.6 priority cases | PENDING | Requires new clean sessions after refresh. |
| 15 | Complete hashed 16-case runtime acceptance | PENDING | Requires `validate_runtime_run.py`. |

## Conclusion

The candidate addresses every reproduced v0.3.5 stale-execution deviation at the
prompt, orchestrator, Gate 5, Gate 7, Gate 10 and regression layers. Repository
readiness is not runtime acceptance; the installed v0.3.6 package must still pass the
canonical cases in clean sessions.
