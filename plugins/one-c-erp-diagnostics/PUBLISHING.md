# Publishing and validation

## Required package checks

- manifest version matches `pyproject.toml`;
- author/homepage/repository/license/interface/policy URLs are valid;
- `composerIcon`, `logo` and `logoDark` exist and pass PNG CRC validation;
- at least 32 packaged skills are present, including the local static-analysis and all dynamic-control skills;
- public-package and ecosystem-marketplace validators pass;
- regression tests pass on Python 3.10 and 3.12;
- CodeQL results are present for the release Pull Request;
- no secrets, real case data, production databases or unsupported dependency claims exist.
- `.scannerwork/` and runtime SonarQube evidence are excluded; no token assignment exists anywhere in the candidate.

## Required ecosystem checks

- marketplace contains exactly `one-c-erp-diagnostics`, `unica`, `1c-skills`, `1c-skills-py` in documented order;
- Unica is pinned to canonical marketplace release `v0.12.0` and subdirectory `plugins/unica`;
- 1C Skills PowerShell/Python use reviewed immutable generated commit refs;
- every plugin remains `AVAILABLE`, not silently `INSTALLED_BY_DEFAULT`;
- third-party licenses, sources, refs, permissions and update policy are documented;
- no third-party code is copied or relicensed in this repository.

## Clean-session smoke tests

1. marketplace refresh/re-import shows all four plugins;
2. 1C ERP Diagnostics `0.3.0` and the approved Velis icon render in GitHub and the plugin selector;
3. Gate 0 reports actual companion availability;
4. an installed companion call records canonical identity, inputs, operation, output and limitations;
5. an under-evidenced case cannot end as final `УСТАНОВЛЕНО`;
6. an unavailable companion request becomes fallback/`blocked`, not simulated;
7. Gate 7 challenges the original evidence and causal chain;
8. analysis-only work is `R0` and may mark Gate 9 `not_required`;
9. a scoped `R3` safety-only test returns `NO-GO`, `Current goal: closed; linked incident: open` and no decorated gate statuses;
10. Gate 0 reports `sonarqube-bsl-local` from actual loopback/server/scanner/BSL/auth state rather than marketplace presence;
11. an available sanitized local scan records `R1`, source/tool/analysis provenance and complete paginated evidence without retaining a token;
12. a static finding without runtime and ERP-chain evidence remains below `УСТАНОВЛЕНО` after Gate 7;
13. the installed plugin details/card reports `0.3.0` when the current surface exposes a version field.

## External companion rule

Do not publish a fabricated `.app.json`, `mcpServers` declaration or hidden dependency. The repository marketplace may reference verified public plugins, but each remains independently installed and subject to its own permissions, terms and confirmations. SonarQube remains a separately installed host adapter and is not a fifth marketplace plugin.

## Repository publication

Before a versioned release:

1. confirm Python 3.10/3.12 CI, CodeQL and self-audit are green on the release Pull Request;
2. merge only through the protected `main` ruleset;
3. verify the complete Git history uses privacy-safe commit identities and contains no confidential artifacts;
4. confirm repository description, topics, policies and brand assets are current;
5. verify private vulnerability reporting, dependency monitoring, secret scanning and push protection remain enabled;
6. perform an anonymous review of README, privacy, terms, support and license URLs.

## ChatGPT/Codex Plugin Directory publication

Public GitHub visibility does not itself create a global listing. After the repository release is available:

1. use the supported ChatGPT/workspace plugin import or publication flow;
2. import the public marketplace/plugin source;
3. review listing metadata, skills and any optional app/plugin requirements;
4. select **Publish** where offered;
5. complete any required OpenAI review or workspace configuration;
6. refresh the workspace plugin whenever a newer marketplace version should be pulled from its original source;
7. install the resulting listing in a clean account/session and repeat all smoke tests.

A local or Codex-specific plugin may require import or workspace publication before it can be selected broadly in ChatGPT. Directory availability, installation and invocation can also depend on plan, role, workspace settings, supported surface and included capabilities.

## Release gate

Run `one-c-erp-plugin-audit`. Any critical `FAIL` blocks merge, tag/release creation and Plugin Directory publication.
