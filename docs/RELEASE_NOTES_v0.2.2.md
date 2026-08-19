# 1C ERP Diagnostics v0.2.2 — Public Preview

## Overview

Version 0.2.2 is the first public-preview release of the evidence-first 1C:ERP diagnostic ecosystem. It combines the dynamic Gate 0–10 orchestrator, 31 packaged diagnostic/control skills, a verified four-plugin marketplace and the marketplace-refresh compatibility hotfix.

## Included

- one user-facing entrypoint: `@one-c-erp-diagnostics` / `$one-c-erp-diagnostics`;
- dynamic capability discovery and resumable case state;
- specialist routing for cost/month close, expenses, settlements, VAT, warehouse, production, access rights, code and release differences;
- claim-to-evidence synthesis and Gate 7 adversarial verification;
- `R0–R3` action-risk controls and same-analytics Gate 9 validation;
- Variant A branding with validated `composerIcon`, `logo` and `logoDark` assets;
- a unified marketplace exposing 1C ERP Diagnostics, Unica, 1C Skills PowerShell and 1C Skills Python;
- pinned `v8unpack==1.2.6` and `opensandbox==0.1.14` optional adapters;
- XLSX, PDF and deterministic case-indexing helpers;
- public privacy, terms, security, support and contribution policies;
- GitHub Actions validation on Python 3.10 and 3.12.

## Marketplace refresh fix

Version 0.2.2 fixes in-place marketplace refresh and ensures the latest packaged Gate 0–10 contract is reinstalled instead of remaining cached under the previous semantic version.

Fixed behavior:

- restored the stable internal marketplace ID `one-c-erp-diagnostics-marketplace` used by existing installations;
- retained the visible title `1C ERP Diagnostics Ecosystem` separately through `interface.displayName`;
- replaced commit hashes stored in `ref` fields with the verified `sha` selector;
- bumped the primary plugin/package version from `0.2.1` to `0.2.2`;
- retained scoped Gate closure: a safety-only goal may close while the linked 1C incident remains open;
- prohibited decorated Gate statuses such as `passed*`;
- added regression controls preventing future marketplace-ID drift and commit-selector misuse.

## Root cause of the refresh failure

The marketplace was originally installed with internal ID:

```text
one-c-erp-diagnostics-marketplace
```

The v0.2.1 ecosystem change renamed that ID to `one-c-erp-diagnostics-ecosystem`. The updater validates that the upgraded checkout reports the same marketplace ID stored in user configuration, so the rename prevented an in-place refresh. The repository URL and visible display name were not the cause.

## Verified companion sources

- Unica: `IngvarConsulting/unica-marketplace`, SHA `aefc880f9bab606a5c55ed11af563b740054a549`, path `plugins/unica`.
- 1C Skills PowerShell: `Nikolay-Shirokov/cc-1c-skills`, SHA `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- 1C Skills Python: `Nikolay-Shirokov/cc-1c-skills`, SHA `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Runtime validation completed

The public-preview candidate was checked through clean-session smoke tests:

- Gate 0 detected Unica, both 1C Skills runtimes and relevant host capabilities without inventing unavailable tools;
- OpenSandbox was reported unavailable when it was not exposed;
- an under-evidenced month-close case did not receive an invented root cause;
- Gate 7 rejected unsupported final `УСТАНОВЛЕНО`;
- analysis-only work was classified `R0` and Gate 9 was `not_required`;
- a closed-period mass-reposting proposal was classified `R3` and received `NO-GO`;
- the marketplace refresh error was reproduced, diagnosed and fixed.

## Safety boundaries

- no third-party code is copied or relicensed;
- companions require separate installation, permissions and confirmations;
- marketplace presence is not runtime availability;
- external output remains a hypothesis until linked to the factual 1C evidence chain;
- production/accounting/access/closed-period actions remain `R3` and require exact approval, affected scope, rollback and Gate 9 validation;
- production `.dt`, backups, credentials and unsanitized customer/company data are prohibited from public issues and examples.

## Public-preview limitations

- actual companion availability and cross-plugin delegation depend on the ChatGPT/Codex plan, workspace, session and permissions;
- OpenSandbox is optional and may be unavailable in a given session;
- the repository marketplace and the global ChatGPT Plugin Directory are separate distribution channels;
- users remain responsible for reviewing every material conclusion and authorizing any production change.
