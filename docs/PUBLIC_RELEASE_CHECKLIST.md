# Public release checklist — v0.3.7

## Repository and plugin package

- [x] Dynamic Gate 0–10 master workflow exists.
- [x] Independent adversarial verification is mandatory for final root-cause `УСТАНОВЛЕНО`.
- [x] 32 packaged skills cover principal 1C:ERP diagnostic/control domains.
- [x] `R0–R3` controls protect production/accounting/access/closed-period actions.
- [x] Every supplied material source must be accounted for before a conclusion it could falsify becomes final.
- [x] Gate 2 distinguishes supplied-but-unexamined evidence from expected-but-missing evidence.
- [x] Missing expected evidence blocks the affected diagnostic Gate rather than a completed evidence-intake procedure.
- [x] Material derived evidence requires artifact anchor and derivation lineage.
- [x] Executable evidence requires current run/case/input/tool/output identity.
- [x] Literal `EVAL_RESULT_JSON` activates a strict one-object/no-Markdown contract.
- [x] Strict mode requires exact skeleton fields and structured capability/claim/link/action items.
- [x] Gate-procedure status is separated from claim proof status.
- [x] A closed current goal requires Gate 10 `passed`.
- [x] `УСТАНОВЛЕНО` requires Gate 7, Gate 10, a closed goal and complete six-stage causality.
- [x] Synthetic capability output exactly matches the case-declared snapshot.
- [x] Inventory-only, stale-execution, provenance-closure and under-evidenced profiles are explicit.
- [x] `under-evidenced-cost` requires Gate 2 passed, Gate 4 blocked, Gate 7 passed and Gate 10 blocked.
- [x] Under-evidenced symptom statements cannot become copied `УСТАНОВЛЕНО` claims.
- [x] Evidence requests are string arrays; absence of an executable action requires `actions=[]`.
- [x] Public package, skill governance, deterministic lock and full-history publication checks are mandatory.
- [x] GitHub Actions validates Python 3.10 and 3.12.
- [x] Approved Velis assets and independent-project trademark boundary remain unchanged.
- [x] Plugin manifest and `pyproject.toml` declare `0.3.7`.
- [x] v0.3.7 release notes and self-audit exist without claiming pending runtime steps as complete.

## Unified 1C ecosystem marketplace

- [x] Primary `one-c-erp-diagnostics` plugin remains local.
- [x] Marketplace ID remains `one-c-erp-diagnostics-marketplace`.
- [x] Marketplace contains exactly four independently installed entries.
- [x] Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`).
- [x] 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- [x] 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.
- [x] Third-party sources, licenses, permissions and update boundaries remain documented.

## Runtime findings and required re-test

- [x] Installed v0.3.6 `capability-inventory` passed.
- [x] Installed v0.3.6 `stale-execution-result` passed.
- [x] Installed v0.3.6 `provenance-closure-broken` passed.
- [x] Installed v0.3.6 `under-evidenced-cost` preserved `ТРЕБУЕТ ПРОВЕРКИ`, `R0`, `EVIDENCE_REQUIRED`, blocked scopes, empty capabilities and incomplete causality.
- [x] The same result reproduced official-contract failures in Gate 2/4/10, claim schema/status, requested-evidence type and action schema.
- [x] v0.3.7 adds the exact under-evidenced semantic profile and rejected regression fixture.
- [ ] Refresh/re-import the marketplace and confirm installed version `0.3.7` when exposed.
- [ ] Re-run `capability-inventory` in a clean session.
- [ ] Re-run `stale-execution-result` in a separate clean session.
- [ ] Re-run `provenance-closure-broken` in a separate clean session.
- [ ] Re-run `under-evidenced-cost` and validate the saved result.
- [ ] Complete and hash all 16 clean-session results.
- [ ] Pass `tools/validate_runtime_run.py` for exact installed v0.3.7.

## GitHub identity, security and presentation

- [x] Repository visibility is Public.
- [x] README, logo, license and policy/support files are reachable publicly.
- [x] Pull Request, linear-history and conversation-resolution controls are configured.
- [x] Private vulnerability reporting is enabled.
- [x] Dependabot, secret scanning and push protection are enabled.
- [ ] Confirm v0.3.7 Pull Request Python 3.10/3.12 and CodeQL checks are green before merge.
- [ ] Verify post-merge `main` validation and CodeQL.

## Global ChatGPT Plugin Directory

- [ ] Use the supported ChatGPT/workspace import or publish flow.
- [ ] Review listing metadata, skills, policies and companion requirements.
- [ ] Publish only after supported platform review/configuration is complete.
- [ ] Repeat clean-session acceptance on the installed public listing.

## Stop condition

Do **not** claim v0.3.7 runtime acceptance while the complete hashed 16-case run is
missing or invalid. Repository CI, CodeQL and publication-history PASS do not substitute
for exact-version runtime evidence.
