---
name: one-c-erp-companion-plugins
description: Safely coordinate optional installed plugins and runtimes such as Unica and 1C Skills without making them hard or fabricated dependencies.
---

# Optional companion coordination

Use only after Gate 0 confirms actual availability.

## Typical roles

- **Unica** — optional 1C developer workflow, code navigation, implementation review or static-development assistance. Its result is a code hypothesis until linked to case evidence.
- **1C Skills (Python)** — optional cross-platform parsing, indexing, comparison and reproducible scripts.
- **1C Skills (PowerShell)** — optional Windows-first automation and 1C tooling. Default to read-only; never alter a working information base implicitly.
- **PDF / Spreadsheets / Documents** — artifact extraction and structured comparison.
- **GitHub / Drive** — source and evidence retrieval when the user has referenced those locations.
- **Computer Use** — UI observation or explicitly approved interaction; production-changing operations require the applicable risk gate.
- **OpenSandbox** — isolated execution when Gate 5 establishes value.

## Boundary

External plugins are invoked, not copied into this package. Their versions, permissions, licenses and availability remain host-managed. Do not declare an app binding or canonical dependency without a verified portable connector ID.

For every companion call capture:

- exact capability/tool name;
- input evidence IDs;
- operation performed;
- output location/hash where possible;
- limitations and errors;
- whether the result was independently reproduced.

A missing companion triggers a documented fallback or `blocked`, never a simulated result.
