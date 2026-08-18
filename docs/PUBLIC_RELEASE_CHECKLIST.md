# Public release checklist

## Repository package

- [x] Gate 1–10 master workflow exists.
- [x] Independent adversarial verification is mandatory for final `УСТАНОВЛЕНО`.
- [x] Domain skills exist for the main 1C:ERP incident classes.
- [x] Plugin manifest and local marketplace are present.
- [x] Variant A branding is configured.
- [x] LICENSE, PRIVACY, SECURITY, CONTRIBUTING and notices are present.
- [x] `.gitignore` excludes secrets, databases and raw case input/work directories.
- [x] Automated public-package validator and regression tests are present.
- [x] GitHub Actions validation workflow is present.
- [x] Current-tree search found no known internal credentials/company names.

## Marketplace/plugin smoke test

- [x] Local marketplace source can be added from the private GitHub repository.
- [ ] Refresh/re-import marketplace and verify plugin card/icon after version 0.1.2.
- [ ] Install/select `@one-c-erp-diagnostics` in a clean independent chat.
- [ ] Run an under-evidenced case and confirm it cannot finish as final `УСТАНОВЛЕНО`.
- [ ] Confirm Gate 7 explicitly challenges the preliminary conclusion.
- [ ] Confirm a missing required capability becomes `blocked` / `ТРЕБУЕТ ПРОВЕРКИ`.
- [ ] Confirm an analysis-only case can mark Gate 9 `not_required`.

## GitHub identity decision

- [x] Final GitHub username confirmed: `akim-kaneyev`.
- [x] Repository URLs, plugin manifest, marketplace metadata and documentation updated to `akim-kaneyev`.
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
- [ ] Confirm no real company/customer data exists in commit history.
- [ ] Confirm no credentials/secrets exist in commit history.
- [ ] Enable GitHub security/private vulnerability reporting if available.
- [ ] Change repository visibility to Public only after all required checks pass.
- [ ] Pin `1c-erp-diagnostics` after it becomes public.

## Public plugin release

- [ ] Re-import/refresh the marketplace after repository/source changes.
- [ ] Run `one-c-erp-plugin-audit` and resolve every critical FAIL.
- [ ] Publish/submit through the available ChatGPT Plugin Directory flow.
- [ ] Install the public listing in a clean chat and repeat the smoke tests.

## Stop condition

Do **not** make the repository public if any real customer/company case data, credentials or production database artifacts are present anywhere in the Git history.
