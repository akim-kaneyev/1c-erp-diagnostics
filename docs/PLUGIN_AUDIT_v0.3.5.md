# Plugin and ecosystem self-audit — v0.3.5 Release Candidate

Audit target: the inventory-only strict output correction after the installed v0.3.4 `capability-inventory` clean-session failure.

Pre-release audit result: **No known critical control is `FAIL`; protected CI/CodeQL and exact-version v0.3.5 runtime evidence remain pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions are synchronized at 0.3.5 | PASS | Manifest, pyproject, validators and version regressions use one patch version. |
| 2 | Inventory completion is separated from diagnostic proof | PASS | Inventory-only contract requires `final_status=ТРЕБУЕТ ПРОВЕРКИ`; successful closure is represented by Gate 10/current goal. |
| 3 | Gate 10 closes every closed bounded goal | PASS | Closed current goal requires Gate 10 `passed`; Gate 10 cannot be `not_required` for a closed inventory goal. |
| 4 | Capability item schema is exact | PASS | Strict row is exactly `{name,status,simulated}` and `simulated=false`; `evidence_id` and other fields are prohibited. |
| 5 | Capability evidence remains top-level | PASS | `E-CAP-1` belongs in `evidence_ids_used`, not in each capability row. |
| 6 | Capability rows are not claims | PASS | Canonical inventory result requires `claims=[]` and permits zero established claims. |
| 7 | Claim schema remains exact | PASS | Any nonempty claim must use `{id,status,text,evidence_ids,falsifier}`; `claim` is not accepted. |
| 8 | Established final status has cross-field proof requirements | PASS | `УСТАНОВЛЕНО` requires Gate 7 passed, Gate 10 passed, closed goal and complete six-stage causality. |
| 9 | Canonical capability statuses are preserved | PASS | `unica=unavailable`, `1c-skills=confirmation_required`, `1c-skills-py=available`, `opensandbox=prohibited`. |
| 10 | Complete inventory Gate profile is explicit | PASS | Gate 0 and 10 passed; Gates 1–9 not required; R0/NO_ACTION; false causal-chain completeness. |
| 11 | Runtime regression reproduces the v0.3.4 failure | PASS | Test fixture contains wrong final status, Gate 10, capability fields, six malformed established claims and incomplete causality. |
| 12 | Earlier stale/provenance corrections are preserved | PASS | Existing v0.3.2/v0.3.3 reproduced shapes and canonical results remain in the same regression suite. |
| 13 | Marketplace identity/composition and companion pins are unchanged | PASS | Four entries; Unica `aefc880f9bab606a5c55ed11af563b740054a549`, PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`, Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`. |
| 14 | Packaged skills and Velis assets are unchanged | PASS | 32 packaged skills; approved composer/card/dark assets retained. |
| 15 | Local repository validators/regressions pass | PENDING | Requires CI execution on the release Pull Request. |
| 16 | Python 3.10/3.12 and CodeQL pass | PENDING | Requires protected Pull Request checks. |
| 17 | Exact installed v0.3.5 capability-inventory test passes | PENDING | Must be repeated in a new clean session after marketplace refresh. |
| 18 | Complete clean-session runtime acceptance passes | PENDING | Requires all 16 case results and strict hashed run manifest. |

## Observed v0.3.4 runtime finding

Installed v0.3.4 repeated all four supplied capability statuses correctly and retained `R0`, `NO_ACTION` and `causal_chain.complete=false`. The result nevertheless returned `УСТАНОВЛЕНО`, made Gate 10 `not_required`, replaced mandatory `simulated` with `evidence_id`, used malformed claim objects and produced six established claims.

The failure is a strict output-contract and semantic-separation defect, not a failure to read the supplied capability statuses.

## Scope of correction

This hotfix changes the authoritative/packaged/portable instructions, capability discovery, final review, the canonical eval prompt, release metadata and regression coverage. It does not add a new agent, packaged skill, external tool, network service, write capability or dependency. Companion pins and approved Velis assets are unchanged.

## Conclusion

The candidate addresses every reproduced v0.3.4 capability-inventory deviation at the earliest applicable controls. Repository readiness cannot be marked complete until protected CI and CodeQL pass. Runtime acceptance remains **BLOCKED** until installed v0.3.5 produces a validator-conformant clean-session result and the full 16-case hashed run passes.
