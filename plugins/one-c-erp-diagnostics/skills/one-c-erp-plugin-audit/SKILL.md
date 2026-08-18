---
name: one-c-erp-plugin-audit
description: Audit the dynamic 1C ERP Diagnostics plugin for manifest integrity, orchestration completeness, external dependency honesty and safety controls.
---

# Plugin self-audit

Audit before release:

1. manifest, version and asset paths are valid;
2. PNG assets pass structural/CRC checks;
3. master orchestrator owns Gate 0–10;
4. capability discovery never assumes installed companions;
5. dynamic plan is bounded and records dependencies;
6. Gate 7 forbids final `УСТАНОВЛЕНО` without adversarial verification;
7. Gate 9 validates identical analytics before/after;
8. domain skills do not invent metadata names;
9. official/current claims require source checks;
10. unavailable tools become blocked, not simulated;
11. risk levels protect production/accounting/access writes;
12. Unica, 1C Skills and other plugins are optional external companions, not copied or fabricated dependencies;
13. open-source additions have source, license, pin and tests;
14. no undeclared MCP/app/backend is claimed;
15. clean-session smoke tests cover under-evidenced, blocked and analysis-only cases.

Report `PASS | FAIL | WARNING`, evidence and remediation. Any critical FAIL blocks release.
