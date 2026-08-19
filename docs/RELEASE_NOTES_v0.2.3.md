# 1C ERP Diagnostics v0.2.3 — Velis Branding and Repository Hardening

## Overview

Version 0.2.3 is a public-preview patch release. It aligns the distributed package with the approved Velis mascot identity and records the completed GitHub security controls without changing the Gate 0–10 diagnostic contract, companion sources, permissions or production-risk model.

## Included

- plugin and project version synchronized at `0.2.3`;
- approved white-dog Velis mascot artwork for `composerIcon`, `logo` and `logoDark`;
- exactly one Velis medallion on the collar; the redundant draft medallion is excluded;
- original visual identity without reproduction of the corporate 1C graphic logo;
- stable marketplace installation ID `one-c-erp-diagnostics-marketplace`;
- unchanged verified ecosystem: 1C ERP Diagnostics, Unica, 1C Skills PowerShell and 1C Skills Python;
- unchanged immutable companion SHAs and independent permissions/licenses;
- active `main` ruleset requiring Pull Request, squash merge, linear history, resolved conversations, current branch state, Python 3.10/3.12 checks and CodeQL results;
- deletion and force-push protection for `main`;
- private vulnerability reporting, dependency graph, Dependabot alerts/security updates, secret scanning and push protection;
- CodeQL default setup for GitHub Actions and Python with a successful initial scan and zero open alerts at release preparation time.

## Diagnostic behavior

No accounting, warehouse, production, access-rights or closed-period behavior changed in this patch. The evidence standard remains:

`document → movement → register/record → consuming mechanism → accounting/stock/access result → symptom`

Final `УСТАНОВЛЕНО` still requires Gate 7 adversarial review. Production/accounting/access/closed-period actions remain `R3` and require exact scope, explicit approval, rollback and Gate 9 validation.

## Marketplace refresh

Existing marketplace installations should be refreshed after `0.2.3` is available. The patch version bump is intentional so host caches receive the approved assets and aligned package metadata rather than retaining the previous `0.2.2` card/icon.

The internal marketplace ID remains unchanged for upgrade compatibility:

```text
one-c-erp-diagnostics-marketplace
```

The visible marketplace title remains:

```text
1C ERP Diagnostics Ecosystem
```

## Verified companion sources

- Unica: `IngvarConsulting/unica-marketplace`, SHA `aefc880f9bab606a5c55ed11af563b740054a549`, path `plugins/unica`.
- 1C Skills PowerShell: `Nikolay-Shirokov/cc-1c-skills`, SHA `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- 1C Skills Python: `Nikolay-Shirokov/cc-1c-skills`, SHA `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Validation required before release

- public-package validator passes;
- ecosystem-marketplace validator passes;
- regression tests pass on Python 3.10 and 3.12;
- CodeQL result is present for the release Pull Request;
- no critical self-audit control is `FAIL`;
- marketplace refresh succeeds;
- Gate 0, under-evidenced-case and scoped `R3 / NO-GO` smoke tests are repeated in a clean session.

## Distribution boundary

The public GitHub repository and repository marketplace do not automatically create a global Plugin Directory listing. Directory publication remains a separate supported OpenAI-side publish action. A skills-only or local/Codex-specific plugin may require import or workspace publication before it can be selected broadly in ChatGPT.
