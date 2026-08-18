# 1C ERP Diagnostics plugin

A single dynamic entrypoint for ChatGPT and Codex:

- ChatGPT: `@one-c-erp-diagnostics`
- Codex: `$one-c-erp-diagnostics <task or case>`

## What is bundled in the primary plugin

- Gate 0–10 master orchestration;
- 31 packaged 1C:ERP and control skills;
- capability discovery and bounded dynamic planning;
- evidence synthesis, contradiction handling and adversarial verification;
- `R0–R3` risk controls and same-analytics validation;
- artifact/open-source intake rules;
- deterministic Python helpers.

## What is exposed by the ecosystem marketplace

The repository marketplace also references three independently maintained companions:

- `unica` — Unica `0.12.0` from `IngvarConsulting/unica-marketplace@v0.12.0`;
- `1c-skills` — PowerShell runtime pinned to immutable ref `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- `1c-skills-py` — Python runtime pinned to immutable ref `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

They are discoverable from one marketplace but remain separate plugins. They are not silently installed, copied, relicensed or granted permissions by `one-c-erp-diagnostics`.

## Runtime coordination

Gate 0 records whether Unica, 1C Skills, document plugins, GitHub/Drive, Computer Use and OpenSandbox are actually available and permitted. Only then may the orchestrator delegate a bounded task. Missing capabilities become a fallback or `blocked`, never a simulated result.

## Why no fabricated app/MCP binding

The public manifest contract does not provide a generic field for embedding arbitrary third-party plugins as hidden dependencies. The portable implementation is a verified multi-plugin marketplace plus runtime capability discovery and explicit provenance—not a guessed `.app.json`, copied private code or permission bypass.

## Safety

Do not include production `.dt`, plaintext credentials, full confidential database backups or unnecessary personal data. External tool output is evidence to verify, not truth by itself. Production/accounting/access actions remain `R3` and require exact approval, rollback and Gate 9 validation.
