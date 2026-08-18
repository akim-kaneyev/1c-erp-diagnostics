# Publishing and validation

## Required package checks

- manifest version matches `pyproject.toml`;
- author/homepage/repository/license/interface/policy URLs are valid;
- `composerIcon`, `logo` and `logoDark` exist and pass PNG CRC validation;
- at least 31 packaged skills are present, including all dynamic-control skills;
- public-package and ecosystem-marketplace validators pass;
- regression tests pass on Python 3.10 and 3.12;
- no secrets, real case data, production databases or unsupported dependency claims exist.

## Required ecosystem checks

- marketplace contains exactly `one-c-erp-diagnostics`, `unica`, `1c-skills`, `1c-skills-py` in documented order;
- Unica is pinned to canonical marketplace release `v0.12.0` and subdirectory `plugins/unica`;
- 1C Skills PowerShell/Python use reviewed immutable generated commit refs;
- every plugin remains `AVAILABLE`, not silently `INSTALLED_BY_DEFAULT`;
- third-party licenses, sources, refs, permissions and update policy are documented;
- no third-party code is copied or relicensed in this repository.

## Clean-session smoke tests

1. marketplace re-import shows all four plugins;
2. 1C ERP Diagnostics `0.2.1` and Variant A icon render in GitHub and the plugin selector;
3. Gate 0 reports actual companion availability;
4. an installed companion call records canonical identity, inputs, operation, output and limitations;
5. an under-evidenced case cannot end as final `УСТАНОВЛЕНО`;
6. an unavailable companion request becomes fallback/`blocked`, not simulated;
7. Gate 7 challenges the original evidence and causal chain;
8. analysis-only work is `R0` and may mark Gate 9 `not_required`;
9. an `R3` action requires exact approval, rollback and validation plan.

## External companion rule

Do not publish a fabricated `.app.json`, `mcpServers` declaration or hidden dependency. The repository marketplace may reference verified public plugins, but each remains independently installed and subject to its own permissions, terms and confirmations.

## Repository publication

Before changing visibility to Public:

1. confirm CI and self-audit are green on `main`;
2. verify the complete Git history uses privacy-safe commit identities and contains no confidential artifacts;
3. configure repository description, topics and `main` ruleset;
4. perform an anonymous review of README, privacy, terms, support and license URLs;
5. enable private vulnerability reporting after visibility changes.

## Global ChatGPT Plugin Directory submission

Public GitHub visibility does not itself create a global listing. After the repository is public:

1. use the ChatGPT/workspace **Create or Import plugin** flow;
2. import the public marketplace/plugin source;
3. review listing metadata, skills and any optional app/plugin requirements;
4. select **Publish/Submit** where offered;
5. complete OpenAI review requirements;
6. install the resulting public listing in a clean account/session and repeat all smoke tests.

The global submission is an OpenAI-side action and cannot be completed by GitHub commits alone.

## Release gate

Run `one-c-erp-plugin-audit`. Any critical `FAIL` blocks merge, repository publication, tag/release creation and Plugin Directory submission.
