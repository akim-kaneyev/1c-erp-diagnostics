---
name: one-c-erp-plugin-audit
description: Audit the 1C ERP Diagnostics plugin itself for workflow completeness, self-consistency, unsupported claims and missing verification controls.
---

# Plugin self-audit

Use before release and when the user asks to check/improve this plugin.

Audit:
1. manifest points to the expected skills directory;
2. master orchestrator exists and owns Gate 1–10;
3. Gate 7 forbids final established cause without adversarial verification;
4. Gate 9 validates identical analytics before/after;
5. domain skills do not invent fixed metadata names;
6. current-law/vendor claims require official-source checks;
7. unavailable tools are blocked rather than simulated;
8. sandbox guidance includes minimization and secret controls;
9. no companion skill requires manual chaining by the user;
10. plugin does not claim undeclared MCP/dependencies.

Report each control `PASS | FAIL | WARNING`, evidence, and exact remediation. Do not self-certify a release as complete while any critical control is FAIL.
