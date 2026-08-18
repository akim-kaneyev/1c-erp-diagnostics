<p align="center">
  <img src="plugins/one-c-erp-diagnostics/assets/composer-icon.png" alt="1C ERP Diagnostics" width="180" />
</p>

<h1 align="center">1C ERP Diagnostics</h1>

<p align="center">
  <a href="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml"><img alt="Validation" src="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml/badge.svg" /></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-gold.svg" /></a>
  <img alt="Version 0.1.2" src="https://img.shields.io/badge/version-0.1.2-0D1B2A.svg" />
  <img alt="1C ERP" src="https://img.shields.io/badge/domain-1C%3AERP-F5B800.svg" />
</p>

<p align="center"><strong>Evidence-first diagnostics for 1C:ERP with Gate 1–10 orchestration and independent conclusion verification.</strong></p>

<p align="center">ChatGPT plugin • Codex skill • diagnostic playbooks • reproducible evidence workflow</p>

> Independent community project. Not affiliated with or endorsed by 1C Company or OpenAI. Product names and trademarks belong to their respective owners.

## Why this project exists

Complex 1C:ERP incidents are often diagnosed from the last visible symptom: an error in month close, an unexpected posting, a split balance, a VAT entry, or a missing quantity. This project enforces a stricter method: **do not guess the cause; prove the chain that creates the result**.

Core chain:

`document → movement → register/record → consuming mechanism → accounting/stock/access result → symptom`

A cause cannot become final `УСТАНОВЛЕНО` until it survives a separate adversarial verification pass.

## What it covers

- cost calculation and month close;
- post-item expenses and allocation;
- settlements, advances and offsets;
- VAT records, books and period corrections;
- warehouse, series and assignments;
- production, stages, returns and repair;
- access rights, profiles and organization restrictions;
- comparison of correct vs problematic documents/states;
- supplied 1C code/query/СКД analysis;
- official-source checks for release, methodology and regulatory claims.

## Gate 1–10 workflow

1. Define a verifiable goal.
2. Inventory evidence and blind spots.
3. Route the case to one primary domain.
4. Build the primary diagnosis and earliest proven divergence.
5. Use isolated execution/OpenSandbox only when it adds verifiable value.
6. Produce a preliminary conclusion.
7. Run an independent adversarial verification pass.
8. Choose the smallest safe reversible action.
9. Validate the same analytics before/after.
10. Close only when every required gate passed or is explicitly not required.

If a required tool, connector or evidence source is unavailable, the gate becomes `blocked`; the workflow must not simulate success.

## Use in ChatGPT

After installing the plugin marketplace/source:

`@one-c-erp-diagnostics`

The master orchestrator routes internally to the relevant companion skills. Users should not need to manually chain them.

## Use in Codex

Repository-local discovery:

`.agents/skills/one-c-erp-diagnostics/SKILL.md`

Global invocation after installation:

`$one-c-erp-diagnostics <task or case>`

Windows and Linux/macOS installers are in `install/`.

## Evidence standard

Priority is given to the actual case materials:

1. document movements;
2. exact register records;
3. postings and OSV drill-down;
4. report exports;
5. supplied code/queries;
6. screenshots;
7. current official documentation;
8. general theory only as a source of hypotheses.

The project must never invent 1C metadata objects, fields, roles, registers or settings that are not established by the evidence, metadata, code or official documentation.

## Supported files

The repository includes helpers for XLSX and PDF plus case indexing/hashing. `.mxl` is handled conservatively: there is no pretend universal parser; use a verified export to XLSX/XML/HTML/TXT and PDF for visual control when appropriate.

## Security and privacy

Do not commit or upload production `.dt`, database backups, credentials, tokens or broad confidential exports merely for convenience. Minimize and pseudonymize case data. See `SECURITY.md` and `PRIVACY.md`.

## Project structure

- `SKILL.md` — authoritative Gate 1–10 workflow;
- `plugins/one-c-erp-diagnostics/` — skills-only ChatGPT/Codex plugin;
- `skills/` — distributable skills;
- `playbooks/` — 1C:ERP diagnostic domains;
- `prompts/` and `checklists/` — verification controls;
- `templates/case/STATE.md` — resumable case state;
- `tools/` — local evidence preparation;
- `sandbox/` — optional isolated execution;
- `docs/` — methodology, release and profile materials.

## Status

Current package version: **0.1.2 — Public Preview candidate**.

This repository is prepared from a clean public snapshot with privacy-safe commit identity. Local marketplace import has been validated; the remaining launch gates are the clean-session plugin smoke test, public visibility, tag/release creation and Plugin Directory submission described in `docs/PUBLIC_RELEASE_CHECKLIST.md`.

## Русский

Проект предназначен для доказательной диагностики 1С:ERP: сначала цель и факты, затем сравнение и причинная цепочка, после чего обязательная независимая проверка вывода. Исчезновение сообщения об ошибке само по себе не считается доказательством исправления учета.

## Contributing

Contributions are welcome if they preserve the evidence-first standard and contain no confidential/customer data. See `CONTRIBUTING.md`.

## License

MIT. See `LICENSE`.
