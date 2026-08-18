# 1C ERP Diagnostics v0.2.2 — Marketplace Refresh Hotfix

## Purpose

Version 0.2.2 fixes in-place marketplace refresh and ensures the latest packaged Gate 0–10 contract is actually reinstalled instead of being skipped under the previous semantic version.

## Fixed

- restored the stable internal marketplace ID `one-c-erp-diagnostics-marketplace` used by existing installations;
- retained the visible title `1C ERP Diagnostics Ecosystem` separately through `interface.displayName`;
- replaced commit hashes stored in `ref` fields with the official verified `sha` selector;
- bumped the primary plugin/package version from `0.2.1` to `0.2.2` so marketplace refresh updates the installed plugin cache;
- retained the scoped Gate closure correction: a safety-only goal may close while the linked 1C incident remains open;
- prohibited decorated Gate statuses such as `passed*`;
- added regression controls preventing future marketplace-ID drift and unverified commit selectors.

## Root cause of the refresh failure

The configured marketplace was originally installed with internal ID:

```text
one-c-erp-diagnostics-marketplace
```

The v0.2.1 ecosystem change renamed that internal ID to `one-c-erp-diagnostics-ecosystem`. OpenAI's updater clones the new source and rejects it when the upgraded marketplace ID does not match the ID stored in the user's configuration. The repository URL and visual display name were not the cause.

## Verified companion sources

- Unica: `IngvarConsulting/unica-marketplace`, SHA `aefc880f9bab606a5c55ed11af563b740054a549`, path `plugins/unica`.
- 1C Skills PowerShell: `Nikolay-Shirokov/cc-1c-skills`, SHA `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- 1C Skills Python: `Nikolay-Shirokov/cc-1c-skills`, SHA `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Safety boundaries

- no third-party code is copied or relicensed;
- companions still require explicit installation and their own permissions;
- marketplace presence is not runtime availability;
- external output remains a hypothesis until linked to the factual 1C evidence chain;
- production/accounting/access/closed-period actions remain `R3` and require exact approval, rollback and Gate 9 validation.

## Upgrade expectation

After merging this hotfix, the existing marketplace should update in place. The plugin card should report version `0.2.2`; the marketplace should expose the primary plugin, Unica, 1C Skills PowerShell and 1C Skills Python.
