# Public release checklist

## Repository package

- [x] Gate 1–10 master workflow exists.
- [x] Independent adversarial verification is mandatory for final `УСТАНОВЛЕНО`.
- [x] Domain skills exist for the main 1C:ERP incident classes.
- [x] Plugin manifest and local marketplace are present.
- [x] Variant A branding is configured.
- [x] LICENSE, PRIVACY, SECURITY, SUPPORT, CONTRIBUTING and notices are present.
- [x] `.gitignore` excludes secrets, databases and raw case input/work directories.
- [x] Automated public-package validator and regression tests are present.
- [x] GitHub Actions validation workflow is present.
- [x] Clean public repository was initialized from a root commit without the private development history.
- [x] Root and subsequent public-candidate commits use the GitHub `noreply` identity.
- [x] Public snapshot provenance and reviewed artifact digest are recorded.
- [x] Current-tree search found no known internal credentials/company names.
- [x] Release review PR passed all required CI checks on Python 3.10 and 3.12.
- [x] Plugin self-audit has no critical `FAIL`; see `docs/PLUGIN_AUDIT_v0.1.2.md`.

## Marketplace/plugin smoke test

- [x] Local marketplace source can be added from the private GitHub repository.
- [ ] Re-import marketplace from `akim-kaneyev/1c-erp-diagnostics` and verify the 0.1.2 card/icon.
- [ ] Install/select `@one-c-erp-diagnostics` in a clean independent chat.
- [ ] Run an under-evidenced case and confirm it cannot finish as final `УСТАНОВЛЕНО`.
- [ ] Confirm Gate 7 explicitly challenges the preliminary conclusion.
- [ ] Confirm a missing required capability becomes `blocked` / `ТРЕБУЕТ ПРОВЕРКИ`.
- [ ] Confirm an analysis-only case can mark Gate 9 `not_required`.

## GitHub identity

- [x] Final GitHub username confirmed: `akim-kaneyev`.
- [x] Repository URLs, plugin manifest, marketplace metadata and documentation updated to `akim-kaneyev`.
- [x] New public-candidate commits use `290311329+akim-kaneyev@users.noreply.github.com`.
- [ ] Confirm a public support email that is separate from private credentials/accounts.
- [ ] Consider joining the GitHub Developer Program after a support email is available.

## GitHub presentation — manual UI steps

- [x] Variant A profile avatar uploaded.
- [x] Name and professional bio configured.
- [ ] Enable anonymized private contributions if desired.
- [ ] Decide whether to enable `Available for hire`.
- [ ] Create public profile repository `akim-kaneyev/akim-kaneyev` and place `README.md` in its root.
- [ ] Repository description: `Evidence-first diagnostics for 1C:ERP — Gate 1–10 orchestration, movements/registers/postings analysis, adversarial verification, ChatGPT & Codex skills/plugin.`
- [ ] Suggested topics: `1c`, `1c-erp`, `1c-enterprise`, `erp`, `accounting`, `diagnostics`, `chatgpt`, `codex`, `ai-agents`, `skills`, `plugins`, `month-close`, `cost-accounting`.
- [ ] Enable a `main` ruleset with pull requests, required CI checks, resolved conversations, no force-push and no deletion.
- [ ] Enable GitHub security/private vulnerability reporting when the repository becomes public.
- [ ] Change repository visibility to Public only after all required checks pass.
- [ ] Pin `1c-erp-diagnostics` after it becomes public.

## Public release

- [x] Run `one-c-erp-plugin-audit` and resolve every critical `FAIL`.
- [ ] Create annotated tag `v0.1.2` on the approved release commit.
- [ ] Publish `1C ERP Diagnostics v0.1.2 — Public Preview` as a pre-release.
- [ ] Submit/publish through the available ChatGPT Plugin Directory flow.
- [ ] Install the public listing in a clean chat and repeat smoke tests.

## Stop condition

Do **not** make the repository public if any real customer/company case data, credentials, personal commit email, production database artifacts or private development history are present in the public repository.
