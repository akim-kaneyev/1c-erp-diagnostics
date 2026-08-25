# Plugin and ecosystem self-audit — v0.3.2 Release Candidate

Audit target: provenance closure, execution identity, publication integrity and the unchanged 32-skill / four-plugin ecosystem.

Pre-release audit result: **No known critical control is accepted as PASS until protected PR CI completes; exact-version clean-session runtime evidence remains pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions are synchronized at 0.3.2 | PASS | Manifest, pyproject and versioned tests use 0.3.2. |
| 2 | Supplied evidence coverage remains mandatory | PASS | Gate 2 retains explicit disposition and blocking rules. |
| 3 | Derived evidence has artifact lineage | PASS | Evidence intake/state require parent IDs, transformation, tool/version/run and output identity where applicable. |
| 4 | Material claims require provenance closure | PASS | Gate 6/7 require source-to-conclusion closure and block open/broken material lineage. |
| 5 | Executable evidence has run identity | PASS | Gate 5/companion/sandbox contracts bind outputs to case/input/tool/output identity and mark mismatches stale. |
| 6 | Static/build output remains non-causal | PASS | Runtime/business validation and causal evidence remain mandatory where required. |
| 7 | Marketplace identity and composition remain stable | PASS | Four entries and stable marketplace ID are unchanged. |
| 8 | Companion provenance remains immutable | PASS | Unica `aefc880f9bab606a5c55ed11af563b740054a549`, PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`, Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`. |
| 9 | Publication validator requires full Git history | PASS | CI uses `fetch-depth: 0`; validator rejects shallow history. |
| 10 | Release archive identity is checked | PASS | Validator compares tracked HEAD with `git archive HEAD`. |
| 11 | Historical unsafe residue is checked | PASS | Historical paths/text blobs are scanned for prohibited artifacts, credential assignments and user-machine paths. |
| 12 | Behavioral eval coverage includes provenance/run freshness | PASS | Suite defines 16 cases and required `provenance_closure` / `execution_identity` controls. |
| 13 | Python 3.10/3.12 CI and CodeQL pass | PENDING | Requires protected Pull Request checks. |
| 14 | Clean-session runtime acceptance passes | PENDING | Must be executed with exactly installed v0.3.2 after repository merge/update. |
| 15 | Annotated tag/GitHub pre-release | PENDING | Not created by this implementation task. |

## Licensing boundary

The reviewed `b-nnett/grok-bot-0.18-reconstructed` repository is used only as a source of general engineering methodology. No reconstructed Grok Bot application code, renderer, inference router, upstream binary or unclear-license payload is copied into this project.

## Conclusion

The v0.3.2 candidate materially strengthens evidence traceability and release hygiene without weakening Gate 0–10, `R0–R3`, independent verification, companion isolation or the 1C causal model. Merge remains conditional on CI; runtime acceptance remains conditional on a later clean installed-plugin run.
