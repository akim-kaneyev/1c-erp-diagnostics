# Public release checklist — v0.3.5

## Repository and plugin package

- [x] Dynamic Gate 0–10 master workflow exists.
- [x] Independent adversarial verification is mandatory for final root-cause `УСТАНОВЛЕНО`.
- [x] 32 packaged skills cover principal 1C:ERP diagnostic/control domains.
- [x] `R0–R3` controls protect production/accounting/access/closed-period actions.
- [x] Every supplied material source must be accounted for before a conclusion it could falsify becomes final.
- [x] Material derived evidence requires artifact anchor and derivation lineage.
- [x] Material claims require provenance closure across source → evidence → premise → causal link → conclusion.
- [x] A directly evidenced missing-lineage limitation may be established without promoting source content or root cause.
- [x] Executable evidence requires run/case/input/tool/output identity; mismatched prior output becomes `stale`.
- [x] Literal `EVAL_RESULT_JSON` activates a strict one-object/no-Markdown contract.
- [x] Strict mode requires exact skeleton fields, canonical Gate statuses and structured capability/claim/link/action items.
- [x] Gate-procedure status is explicitly separated from claim proof status.
- [x] A closed current goal requires Gate 10 `passed`; Gate 10 cannot be `not_required` for a closed goal.
- [x] `УСТАНОВЛЕНО` requires Gate 7 passed, Gate 10 passed, a closed goal and complete six-stage causality.
- [x] Risk classifies the action surface; read-only inventory is `R0`.
- [x] `EVIDENCE_REQUIRED`, `NO_ACTION` and `NO-GO` have non-overlapping meanings.
- [x] `not_in_scope` requires explicit scope exclusion.
- [x] Synthetic result capabilities must exactly match the case-declared snapshot; internal reasoning/skills/roles are prohibited as capabilities.
- [x] Every strict capability item is exactly `{name,status,simulated}` with `simulated=false`.
- [x] Capability rows cannot contain `evidence_id`; snapshot evidence remains in `evidence_ids_used`.
- [x] Capability status rows are not diagnostic claims.
- [x] Inventory-only acceptance requires `claims=[]`, Gate 0/10 passed and Gates 1–9 not required.
- [x] `causal_chain.complete` remains restricted to all six canonical 1C causal stages.
- [x] Strict runtime acceptance requires a complete clean-session run, exact installed version and SHA-256 result evidence.
- [x] Public package validation checks manifest, policies, case leakage, forbidden artifacts, credentials and assets.
- [x] Skill governance and deterministic `SKILLS.lock.json` validation are mandatory.
- [x] Publication-history validation checks full Git history and actual `git archive HEAD` tree.
- [x] CI checkout uses full history rather than a shallow release-safety scan.
- [x] `.scannerwork/` and local runtime evidence are excluded from Git.
- [x] GitHub Actions validates Python 3.10 and 3.12.
- [x] Approved Velis assets and independent-project trademark boundary remain unchanged.
- [x] Plugin manifest and `pyproject.toml` declare `0.3.5`.
- [x] v0.3.5 release notes and self-audit exist without claiming pending runtime steps as complete.

## Unified 1C ecosystem marketplace

- [x] Primary `one-c-erp-diagnostics` plugin is declared locally.
- [x] Canonical Unica `0.12.0` source remains pinned to immutable SHA `aefc880f9bab606a5c55ed11af563b740054a549` and path `plugins/unica`.
- [x] 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- [x] 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.
- [x] Third-party sources, licenses, permissions and update boundaries remain documented.
- [x] External plugins remain independently installed; no code copying or permission bypass.
- [x] Internal marketplace ID remains `one-c-erp-diagnostics-marketplace`.
- [x] Visible title remains `1C ERP Diagnostics Ecosystem`.
- [x] Primary plugin/package version is `0.3.5`.

## Runtime findings and smoke tests

- [x] Installed v0.3.2 rejected stale evidence substantively but reproduced strict schema/semantic deviations.
- [x] Installed v0.3.3 canonical `stale-execution-result` passed after the v0.3.3 hotfix.
- [x] Installed v0.3.3 `provenance-closure-broken` exposed linked-scope and invented-capability gaps.
- [x] v0.3.4 corrected provenance scope, exact synthetic capability snapshots and statement-specific limitation claims.
- [x] Installed v0.3.4 `capability-inventory` preserved `R0`, `NO_ACTION`, the four supplied capability statuses and false causal-chain completeness.
- [x] The same v0.3.4 result reproduced six official-contract failures: wrong final status, Gate 10, capability item fields, claim schema/count and cross-field proof consistency.
- [x] v0.3.5 adds the exact inventory-only semantic profile and a regression fixture reproducing the v0.3.4 output.
- [ ] Refresh/re-import the marketplace after merge and confirm installed version `0.3.5` when the surface exposes it.
- [ ] Run the exact rendered `capability-inventory` prompt in a new clean session.
- [ ] Confirm `final_status=ТРЕБУЕТ ПРОВЕРКИ`, `R0`, `NO_ACTION`, current goal closed, linked incident not in scope, Gate 0/10 passed and Gates 1–9 not required.
- [ ] Confirm capability rows preserve the supplied order and contain exactly `name`, `status`, `simulated=false`; `E-CAP-1` appears only in `evidence_ids_used`.
- [ ] Confirm `claims=[]`, `causal_chain.complete=false`, empty links/requested evidence/actions.
- [ ] Validate the saved result with `tools/validate_evals.py`.
- [ ] Repeat canonical `stale-execution-result` and `provenance-closure-broken` clean-session tests to prove no regression.
- [ ] Repeat the under-evidenced case and confirm no invented final cause.
- [ ] Repeat scoped R3 safety-only test and confirm `Current goal: closed; linked incident: open`.
- [ ] Confirm SonarQube missing auth/runtime remains honest (`confirmation_required`/`unavailable`) without simulated findings.
- [ ] Run authorized sanitized local SonarQube smoke test with complete provenance and no token retention.
- [ ] Record every executable eval result and pass `tools/validate_runtime_run.py` for one complete clean v0.3.5 run.

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
- [ ] Confirm v0.3.5 protected PR CodeQL and required checks are green before merge.

## Public repository and versioned release

- [x] Public repository is live.
- [ ] Open the v0.3.5 Pull Request from `hotfix/capability-inventory-contract-0.3.5`.
- [ ] Pass Python 3.10/3.12 validation, skill governance/lock, publication-history validation, CodeQL, up-to-date-branch and resolved-conversation requirements.
- [ ] Squash-merge v0.3.5 only through the protected `main` ruleset.
- [ ] Verify post-merge `main` validation and CodeQL.
- [ ] If a versioned GitHub release is desired, create the tag/release only on the exact approved `main` commit.
- [ ] Verify release metadata/tagged documentation and source archives anonymously before making a release claim.

## Global ChatGPT Plugin Directory

- [ ] Use the supported ChatGPT/workspace import or publish flow for the public plugin source.
- [ ] Review listing metadata, skills, policy URLs and companion requirements.
- [ ] Publish only after the supported platform review/configuration is complete.
- [ ] Install the public listing in a clean session and repeat capability inventory, stale-run, provenance, under-evidenced and R3 smoke tests.

## Stop condition

Do **not** claim v0.3.5 runtime acceptance or publish a global listing while any required CI, CodeQL, publication-history or clean-session control fails; if marketplace refresh/re-import fails; or if credentials, real customer/company case data, production database artifacts, personal commit email or unsafe private history are present.
