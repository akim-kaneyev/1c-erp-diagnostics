# Public release checklist — v0.3.2

## Repository and plugin package

- [x] Dynamic Gate 0–10 master workflow exists.
- [x] Independent adversarial verification is mandatory for final `УСТАНОВЛЕНО`.
- [x] 32 packaged skills cover principal 1C:ERP diagnostic/control domains.
- [x] `R0–R3` controls protect production/accounting/access/closed-period actions.
- [x] Every supplied material source must be accounted for before a conclusion it could falsify becomes final.
- [x] Material derived evidence requires artifact anchor and derivation lineage.
- [x] Material claims require provenance closure across source → evidence → premise → causal link → conclusion.
- [x] Executable evidence requires run/case/input/tool/output identity; mismatched prior output becomes `stale`.
- [x] Synthetic executable eval specifications include provenance-closure and execution-identity controls.
- [x] Strict runtime acceptance requires a complete clean-session run, exact installed version and SHA-256 result evidence.
- [x] Public package validation checks manifest, policies, case leakage, forbidden artifacts, credentials and assets.
- [x] Publication-history validation checks full Git history and actual `git archive HEAD` tree.
- [x] CI checkout uses full history rather than a shallow release-safety scan.
- [x] `.scannerwork/` and local runtime evidence are excluded from Git.
- [x] GitHub Actions validates Python 3.10 and 3.12.
- [x] Approved Velis assets and independent-project trademark boundary remain unchanged.
- [x] Plugin manifest and `pyproject.toml` declare `0.3.2`.
- [x] v0.3.2 release notes and self-audit exist without claiming pending GitHub/runtime steps as complete.

## Unified 1C ecosystem marketplace

- [x] Primary `one-c-erp-diagnostics` plugin is declared locally.
- [x] Canonical Unica `0.12.0` source remains pinned to immutable SHA `aefc880f9bab606a5c55ed11af563b740054a549` and path `plugins/unica`.
- [x] 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- [x] 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.
- [x] Third-party sources, licenses, permissions and update boundaries remain documented.
- [x] External plugins remain independently installed; no code copying or permission bypass.
- [x] Internal marketplace ID remains `one-c-erp-diagnostics-marketplace`.
- [x] Visible title remains `1C ERP Diagnostics Ecosystem`.
- [x] Primary plugin/package version is `0.3.2`.

## Marketplace/plugin smoke tests

- [ ] Refresh the marketplace after v0.3.2 and confirm the new version is installed.
- [ ] Repeat Gate 0 in a clean v0.3.2 session and record actual capability availability.
- [ ] Repeat the under-evidenced case and confirm no invented final cause.
- [ ] Run the synthetic broken-provenance scenario and confirm `УСТАНОВЛЕНО` is blocked.
- [ ] Run the stale-execution scenario and confirm old mismatched output is not accepted as current evidence.
- [ ] Repeat scoped R3 safety-only test and confirm `Current goal: closed; linked incident: open`.
- [ ] Confirm SonarQube missing auth/runtime remains honest (`confirmation_required`/`unavailable`) without simulated findings.
- [ ] Run authorized sanitized local SonarQube smoke test with complete provenance and no token retention.
- [ ] Confirm installed plugin details/card reports version `0.3.2` if exposed.
- [ ] Record every executable eval result and pass `tools/validate_runtime_run.py` for one complete clean v0.3.2 run.

## GitHub identity, security and presentation

- [x] Final username: `akim-kaneyev`.
- [x] Repository visibility is Public.
- [x] README, logo, license and policy/support files are reachable publicly.
- [x] Issues and Pull Requests are enabled.
- [x] Effective `main` ruleset requires Pull Request, Python 3.10/3.12 checks, current branch state, resolved conversations and CodeQL results.
- [x] Effective `main` ruleset requires linear history and blocks force-push and deletion.
- [x] Private vulnerability reporting is enabled.
- [x] Dependency graph, Dependabot alerts/security updates, secret scanning and push protection are enabled.
- [x] CodeQL default setup has previously completed successfully for GitHub Actions and Python.
- [ ] Confirm v0.3.2 protected PR CodeQL and required checks are green before merge.

## Public repository and versioned release

- [x] Public repository is live.
- [ ] Open the v0.3.2 Pull Request from the feature branch.
- [ ] Pass Python 3.10/3.12 validation, publication-history validation, CodeQL, up-to-date-branch and resolved-conversation requirements.
- [ ] Squash-merge v0.3.2 only through the protected `main` ruleset.
- [ ] If a versioned GitHub release is desired, create the tag/release only on the exact approved `main` commit.
- [ ] Verify release metadata/tagged documentation and source archives anonymously before making a release claim.

## Global ChatGPT Plugin Directory

- [ ] Use the supported ChatGPT/workspace import or publish flow for the public plugin source.
- [ ] Review listing metadata, skills, policy URLs and companion requirements.
- [ ] Publish only after the supported platform review/configuration is complete.
- [ ] Install the public listing in a clean session and repeat Gate 0, provenance, stale-run, under-evidenced and R3 smoke tests.

## Stop condition

Do **not** claim v0.3.2 release/runtime acceptance or publish a global listing while any required CI, CodeQL, publication-history or clean-session control fails; if marketplace refresh/re-import fails; or if credentials, real customer/company case data, production database artifacts, personal commit email or unsafe private history are present.
