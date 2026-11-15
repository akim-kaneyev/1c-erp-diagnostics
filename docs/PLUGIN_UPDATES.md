# Windows plugin updates

Use the packaged [update procedure](../plugins/one-c-erp-diagnostics/skills/one-c-erp-companion-plugins/references/plugin-updates.md) for the primary diagnostic plugin and Unica.

It refreshes the catalog separately, preserves enabled flags, skips byte-identical installed versions and installs changed versions into their version directories. It addresses a running-bootstrap cache lock without granting new permissions or stopping 1C. A fresh Codex task loads the updated MCP contract. The 1C bridge remains deferred.
