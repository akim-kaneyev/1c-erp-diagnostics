# Public release checklist

## Repository and plugin package

- [x] Dynamic Gate 0–10 master workflow exists.
- [x] Independent adversarial verification is mandatory for final `УСТАНОВЛЕНО`.
- [x] 31 packaged skills cover the principal 1C:ERP diagnostic and control domains.
- [x] `R0–R3` action controls protect production/accounting/access/closed-period actions.
- [x] Variant A `composerIcon`, `logo` and `logoDark` pass PNG structural/CRC checks.
- [x] LICENSE, PRIVACY, TERMS, SECURITY, SUPPORT, CONTRIBUTING and notices are present.
- [x] `.gitignore` excludes secrets, databases and raw case input/work directories.
- [x] Public-package, ecosystem-marketplace and regression validators are present.
- [x] GitHub Actions validates Python 3.10 and 3.12.
- [x] Clean public repository was initialized without private development history.
- [x] Public-candidate commits use GitHub `noreply` identity.
- [x] Current-tree searches found no known internal credentials/company names.
- [x] v0.2.1 self-audit had no critical `FAIL` before the refresh hotfix.
- [x] Scoped Gate-closure ambiguity found by the R3 test was corrected and regression-tested.

## Unified 1C ecosystem marketplace

- [x] Primary `one-c-erp-diagnostics` plugin is declared locally.
- [x] Canonical Unica `0.12.0` release is pinned to immutable SHA `aefc880f9bab606a5c55ed11af563b740054a549` and path `plugins/unica`.
- [x] 1C Skills PowerShell and Python are pinned to reviewed immutable generated SHAs.
- [x] Third-party sources, versions, licenses and permission boundaries are documented.
- [x] External plugins remain independently installed; no code copying, relicensing or permission bypass.
- [x] Gate 0 uses canonical identities and records actual availability.
- [x] Missing companion capabilities become fallback/`blocked`, never simulated.
- [x] Internal marketplace ID restored to stable `one-c-erp-diagnostics-marketplace`.
- [x] Visible title remains `1C ERP Diagnostics Ecosystem` through `interface.displayName`.
- [x] External commit pins use the verified `sha` selector, not a commit hash in `ref`.
- [x] Primary plugin/package version bumped to `0.2.2` so the installed cache receives behavior changes.

## Marketplace/plugin smoke tests

- [x] The private repository marketplace was added locally.
- [x] Variant A icon renders in the local ChatGPT plugin list.
- [x] Gate 0 capability inventory completed in a clean independent chat.
- [x] Unica and both 1C Skills runtimes were detected and probed read-only.
- [x] OpenSandbox was correctly reported unavailable and was not simulated.
- [x] Under-evidenced case did not produce an invented final cause.
- [x] Gate 7 rejected unsupported `УСТАНОВЛЕНО`.
- [x] Analysis-only work was classified `R0`; Gate 9 was `not_required`.
- [x] Unapproved closed-period/mass-reposting proposal was classified `R3` and received `NO-GO`.
- [ ] Merge the v0.2.2 refresh hotfix after CI passes.
- [ ] Refresh the existing marketplace in place and confirm the error is gone.
- [ ] Confirm the marketplace shows four plugins.
- [ ] Confirm the primary card reports version `0.2.2`, unified-ecosystem description and Variant A icon.
- [ ] Repeat the R3 scoped-closure test and confirm canonical statuses with `Current goal: closed; linked incident: open`.

## GitHub identity and presentation

- [x] Final username: `akim-kaneyev`.
- [x] Repository URLs and public documentation use `akim-kaneyev`.
- [x] New public-candidate commits use the GitHub ID-based `noreply` address.
- [x] Variant A profile avatar, name and professional bio are configured.
- [ ] Create public profile repository `akim-kaneyev/akim-kaneyev` with profile README.
- [ ] Set repository description: `Evidence-first 1C:ERP diagnostics — dynamic Gate 0–10 orchestration and a verified Unica/1C Skills companion ecosystem.`
- [ ] Add topics: `1c`, `1c-erp`, `1c-enterprise`, `erp`, `accounting`, `diagnostics`, `chatgpt`, `codex`, `ai-agents`, `skills`, `plugins`, `unica`, `month-close`, `cost-accounting`.
- [ ] Enable a `main` ruleset with pull requests, required Python 3.10/3.12 checks, resolved conversations, no force-push and no deletion.
- [ ] Confirm every public URL anonymously after visibility change.
- [ ] Enable private vulnerability reporting after the repository becomes public.
- [ ] Pin `1c-erp-diagnostics` in the public profile.

## Public repository and release

- [ ] Change repository visibility to Public.
- [ ] Create annotated tag `v0.2.2` on the approved release commit.
- [ ] Publish `1C ERP Diagnostics v0.2.2 — Marketplace Refresh Hotfix` as a pre-release.

## Global ChatGPT Plugin Directory

- [ ] Use the ChatGPT/workspace **Create or Import plugin** flow after the repository is public.
- [ ] Review listing metadata, skills and companion requirements.
- [ ] Select **Publish/Submit** where offered and complete OpenAI review.
- [ ] Verify the plugin appears in the global directory rather than only the personal marketplace.
- [ ] Install the public listing in a clean account/session and repeat all smoke tests.

## Stop condition

Do **not** publish the repository or global listing while any critical CI/self-audit control fails, while the ecosystem marketplace cannot be refreshed/re-imported, or if any real customer/company data, credentials, personal commit email, production database artifact or private development history is present.
