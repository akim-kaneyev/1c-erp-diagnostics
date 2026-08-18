# 1C ERP Diagnostics v0.1.2 — Public Preview

## Overview

The first public preview packages an evidence-first 1C:ERP diagnostic workflow for ChatGPT and Codex.

## Included

- mandatory Gate 1–10 orchestration;
- independent adversarial verification before final root-cause status;
- domain skills for cost/month close, post-item expenses, settlements, VAT, warehouse/series/assignments, production, access rights and supplied-code analysis;
- resumable case state;
- conservative XLSX/PDF preparation tools;
- optional OpenSandbox decision controls;
- privacy, security and public contribution policies;
- automated plugin/package validation and regression tests on Python 3.10 and 3.12;
- skills-only ChatGPT/Codex plugin with Variant A branding.

## Installation entry points

- ChatGPT: `@one-c-erp-diagnostics`
- Codex: `$one-c-erp-diagnostics <task or case>`

## Important limitations

- The project never treats general 1C theory as proof of a case-specific cause.
- It does not include a universal MXL parser.
- It must not receive production databases, credentials or unnecessary confidential exports.
- The first public release remains a preview until clean-session plugin smoke tests are completed.

## Release procedure

Create the annotated tag `v0.1.2` only on the final clean public-repository commit after CI and plugin smoke tests pass. Publish a GitHub Release titled `1C ERP Diagnostics v0.1.2 — Public Preview` and mark it as a pre-release.
