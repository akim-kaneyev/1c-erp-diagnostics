# Publishing and validation

## Local plugin smoke test

This repository includes `.agents/plugins/marketplace.json` pointing to `plugins/one-c-erp-diagnostics`.

Expected local tests:
- plugin is discoverable from the local marketplace;
- `@one-c-erp-diagnostics` selects the plugin when the host supports local plugin installation;
- a diagnostic request routes through the master orchestrator;
- domain companion skills refine the analysis without user-side manual chaining;
- a deliberately under-evidenced test case cannot end with final `УСТАНОВЛЕНО`;
- an analysis-only case may mark post-change validation `not_required` explicitly;
- unavailable required capabilities become `blocked` rather than silently skipped.

## Pre-release audit

Invoke/apply `one-c-erp-plugin-audit` and require no critical FAIL.

## Public submission

Public listing/review is an OpenAI Platform/Plugin Directory action and cannot be completed by repository commits alone. Prepare manifest, public metadata, privacy/support information and any required review materials in accordance with the current OpenAI plugin submission flow.

This v0.1 is skills-only: no custom MCP server, no custom OAuth, no external action endpoint declared.
