# 1C ERP Diagnostics plugin

A single dynamic entrypoint for ChatGPT and Codex:

- ChatGPT: `@one-c-erp-diagnostics`
- Codex: `$one-c-erp-diagnostics <task or case>`

## What is bundled

- Gate 0–10 master orchestration;
- 1C:ERP domain specialists;
- capability discovery and bounded dynamic planning;
- evidence synthesis and adversarial verification;
- risk controls and same-analytics validation;
- artifact/open-source intake rules;
- deterministic Python helpers.

## Optional companions

Unica, 1C Skills (Python/PowerShell), document plugins, GitHub/Drive, Computer Use and OpenSandbox are discovered at runtime and used only when the host exposes them and the case needs them. They are not copied into this package, and their unavailable state is never hidden.

## Why no fabricated app/MCP binding

A portable plugin dependency requires verified public connector metadata. None was available for the user's locally installed Unica/1C Skills packages during this review. The safe implementation is capability discovery plus explicit provenance, not a guessed `.app.json` or copied private code.

## Safety

Do not include production `.dt`, plaintext credentials, full confidential database backups or unnecessary personal data. External tool output is evidence to verify, not truth by itself.
