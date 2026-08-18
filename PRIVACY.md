# Privacy

## Scope

The `1C ERP Diagnostics` v0.1.x plugin is skills-only. It does not operate a developer-owned MCP server, API endpoint, analytics backend, user database, or custom OAuth service.

## Data handling

The plugin instructions may ask ChatGPT/Codex to analyze evidence the user provides or to use tools/apps that the user has already enabled when they are relevant to the task. Those host products and third-party services have their own data-handling policies and permissions.

The plugin package itself does not intentionally collect or transmit case data to a developer-operated service.

## Data minimization

Users should not provide production `.dt` files, full database backups, plaintext credentials, tokens, unnecessary personal data, or broad confidential exports merely for convenience. Prefer the smallest evidence slice that can answer the diagnostic question and pseudonymize organizations, counterparties and people when possible.

## Isolated execution

OpenSandbox or another isolated executor may be used only when executable validation adds value. Isolation does not replace data minimization. Secrets should be injected through supported secret-management mechanisms rather than stored in files.

## Changes

If a future version adds a developer-operated MCP server, hosted service, telemetry or authentication flow, this privacy document must be updated before that version is published.
