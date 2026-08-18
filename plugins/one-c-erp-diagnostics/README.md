# 1C ERP Diagnostics plugin

Skills-only plugin for ChatGPT and Codex.

## Explicit invocation

- ChatGPT/Codex plugin: `@one-c-erp-diagnostics`
- Direct Codex skill, when installed separately: `$one-c-erp-diagnostics`

The plugin packages one orchestrator and focused companion skills. The user should not manually chain them. The orchestrator owns Gate 1–10 and may apply companion skills as refinements.

## Why skills-only in v0.1

The workflow primarily needs instructions, uploaded evidence, built-in analysis tools and whichever apps are already available to the user. A custom MCP server would add hosting, authentication, domain verification and review surface without being necessary for the core diagnostic method. Add MCP only when a controlled server-side capability is actually required.

## Safety

Do not include production `.dt`, plaintext credentials, confidential full database backups or unnecessary personal data. A sandbox does not replace data minimization.
