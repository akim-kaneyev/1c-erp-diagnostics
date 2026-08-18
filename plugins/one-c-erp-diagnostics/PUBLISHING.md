# Publishing and validation

## Required package checks

- manifest version matches `pyproject.toml`;
- author/homepage/repository/license/interface metadata are valid;
- `composerIcon`, `logo` and `logoDark` exist and pass PNG CRC validation;
- at least 31 packaged skills are present, including all dynamic-control skills;
- public-package validator and regression tests pass on Python 3.10 and 3.12;
- no secrets, real case data, production databases or unsupported dependency claims exist.

## Clean-session smoke tests

1. plugin is discoverable after marketplace re-import;
2. Variant A icon renders in GitHub and the plugin selector;
3. Gate 0 reports actual companion availability;
4. an under-evidenced case cannot end as final `УСТАНОВЛЕНО`;
5. an unavailable Unica/1C Skills request becomes fallback/`blocked`, not simulated;
6. Gate 7 challenges the original evidence and causal chain;
7. analysis-only work is `R0` and may mark Gate 9 `not_required`;
8. R3 action requires exact approval, rollback and validation plan.

## External companion rule

Do not publish `.app.json` or `mcpServers` unless the connector/server exists, is portable, is licensed for this use and has verified identifiers. Host-managed Unica and 1C Skills remain optional runtime companions.

## Release gate

Run `one-c-erp-plugin-audit`. Any critical `FAIL` blocks merge/release. Repository publication and Plugin Directory submission remain separate product actions.
