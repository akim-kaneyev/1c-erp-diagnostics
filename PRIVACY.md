# Privacy

## Scope

`1C ERP Diagnostics` v0.2.3 is a skills-first plugin and marketplace package. The project does not operate a developer-owned MCP server, API endpoint, analytics backend, user database, telemetry service or custom OAuth service.

The marketplace also references independently maintained companion plugins such as Unica and 1C Skills. Those companions are not operated, copied or controlled by this project and retain their own privacy policies, permissions and data-handling behavior.

## Data handling

The plugin instructions may ask ChatGPT or Codex to analyze evidence the user provides or to use tools/apps that the user has already enabled when they are relevant to the task. Those host products and third-party services have their own data-handling policies and permissions.

The `1C ERP Diagnostics` package itself does not intentionally collect or transmit case data to a developer-operated service.

## Data minimization

Users should not provide production `.dt` files, full database backups, plaintext credentials, tokens, unnecessary personal data or broad confidential exports merely for convenience. Prefer the smallest evidence slice that can answer the diagnostic question and pseudonymize organizations, counterparties and people when possible.

Before sharing a file, review hidden spreadsheet sheets, document properties, embedded metadata, comments, connection strings and credentials.

## Companion plugins and connected tools

Installing the ecosystem marketplace does not silently install or enable every companion. Each plugin remains independently installed and permissioned. Gate 0 records what is actually available in the current session; marketplace presence is not treated as runtime availability.

When Unica, 1C Skills, GitHub, Google Drive, Computer Use or another connected capability is used, its own permissions and provider policies apply. The project cannot override host confirmations or source-system access controls.

## Isolated execution

OpenSandbox or another isolated executor may be used only when executable validation adds measurable value. Isolation does not replace data minimization. Secrets should be injected through supported secret-management mechanisms rather than stored in files. Sandbox output is evidence to verify, not truth by itself.

## Repository security controls

The public repository uses protected-branch rules, required CI and CodeQL results, private vulnerability reporting, Dependabot alerts/security updates, secret scanning and push protection. These GitHub controls reduce distribution risk but do not replace user-side data minimization or review of every material conclusion.

## Public issues and examples

Do not publish credentials, customer/company identifiers, real primary documents, production database artifacts or confidential register exports in GitHub Issues or repository examples. Public examples must be synthetic or irreversibly sanitized.

## Changes

If a future version adds a developer-operated MCP server, hosted service, telemetry, authentication flow or persistent data store, this privacy document must be updated before that version is published.
