---
name: one-c-erp-plugin-audit
description: Audit the dynamic 1C ERP Diagnostics plugin and unified companion marketplace for manifest integrity, orchestration completeness, source provenance, dependency honesty and safety controls.
---

# Plugin and ecosystem self-audit

Audit before release or public submission:

1. manifest, version, policy URLs and asset paths are valid;
2. PNG assets pass structural/CRC checks;
3. master orchestrator owns Gate 0–10;
4. capability discovery never assumes installed companions;
5. dynamic plan is bounded and records dependencies;
6. Gate 7 forbids final `УСТАНОВЛЕНО` without adversarial verification;
7. Gate 9 validates identical analytics before/after;
8. domain skills do not invent metadata names;
9. official/current claims require source checks;
10. unavailable tools become fallback/`blocked`, not simulated;
11. `R0–R3` controls protect production/accounting/access/closed-period actions;
12. marketplace contains exactly the reviewed primary and companion plugins;
13. Unica source/path/ref matches the canonical `0.12.0` marketplace release;
14. 1C Skills variants use reviewed immutable generated commit refs;
15. every companion requires explicit installation and retains its own permissions/license;
16. no external implementation is copied, relicensed or represented as embedded;
17. open-source additions have source, license, pin, tests and fallback;
18. no undeclared MCP/app/backend or unsupported manifest field is claimed;
19. repository history and package contain no confidential case data or credentials;
20. clean-session smoke tests cover capability inventory, installed/unavailable companions, under-evidenced cases, analysis-only work and `R3` blocking;
21. public repository, release and Plugin Directory submission are not marked complete before their separate product-side checks pass.

Report each control as `PASS | FAIL | WARNING` with exact evidence and remediation. Any critical `FAIL` blocks merge, repository publication, tag/release creation and global Plugin Directory submission.
