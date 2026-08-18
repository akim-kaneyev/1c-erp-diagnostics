# 1C ERP Diagnostics v0.2.1 — Unified Ecosystem Preview

## Overview

Version 0.2.1 turns the repository marketplace into a verified 1C companion ecosystem while keeping `1C ERP Diagnostics` as the single evidence-first entrypoint.

## Included

- dynamic Gate 0–10 orchestration;
- 31 packaged diagnostic/control skills;
- bounded specialist graph and claim-to-evidence synthesis;
- Gate 7 adversarial verification;
- `R0–R3` action-risk controls;
- Variant A branding with validated PNG assets;
- immutable Unica `0.12.0` marketplace reference;
- immutable 1C Skills PowerShell and Python plugin references;
- OpenSandbox and `v8unpack` optional adapters with exact pins;
- XLSX, PDF and deterministic case-indexing helpers;
- ecosystem source/license/provenance documentation;
- public privacy, terms, security and support policies;
- CI on Python 3.10 and 3.12.

## Architecture change

The external companion plugins are not copied into `one-c-erp-diagnostics`. The repository marketplace exposes them together, while Gate 0 discovers what is actually installed and permitted. This preserves explicit installation, third-party licenses, permissions and independent release lifecycles.

## Companion sources

- Unica: `IngvarConsulting/unica-marketplace`, release tag `v0.12.0` resolved to commit `aefc880f9bab606a5c55ed11af563b740054a549`, path `plugins/unica`.
- 1C Skills PowerShell: `Nikolay-Shirokov/cc-1c-skills`, commit `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- 1C Skills Python: `Nikolay-Shirokov/cc-1c-skills`, commit `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Safety boundaries

- no production `.dt`, backups or credentials;
- no silent third-party installation or permission bypass;
- no external output treated as proof without evidence-chain linkage;
- no final `УСТАНОВЛЕНО` without Gate 7;
- production/accounting/access/closed-period actions are `R3` and require exact approval, rollback and Gate 9 validation.

## Preview limitations

- actual cross-plugin availability depends on the ChatGPT/Codex host, plan, workspace, installation and permissions;
- global Plugin Directory publication is an OpenAI-side submission after public repository release;
- live information-base MCP access is not bundled and remains prohibited by default;
- the marketplace and global listing require clean-session smoke tests after re-import/publication.

## Release procedure

After CI and self-audit pass:

1. merge the reviewed v0.2.1 pull request;
2. re-import `main` and complete ecosystem smoke tests;
3. change repository visibility to Public;
4. create annotated tag `v0.2.1`;
5. publish this release as a pre-release;
6. use the ChatGPT/workspace Create/Import plugin flow and submit the public listing;
7. install the global listing in a clean session and repeat all tests.
