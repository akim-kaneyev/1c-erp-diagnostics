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
8. Gate 10 separates the current goal from the linked incident and never uses decorated statuses such as `passed*`;
9. domain skills do not invent metadata names;
10. official/current claims require source checks;
11. unavailable tools become fallback/`blocked`, not simulated;
12. `R0–R3` controls protect production/accounting/access/closed-period actions;
13. marketplace contains exactly the reviewed primary and companion plugins;
14. Unica source/path/ref matches the canonical `0.12.0` marketplace release;
15. 1C Skills variants use reviewed immutable generated commit refs;
16. every companion requires explicit installation and retains its own permissions/license;
17. no external implementation is copied, relicensed or represented as embedded;
18. open-source additions have source, license, reviewed version/identity, tests and fallback;
19. SonarQube remains an optional host adapter rather than a marketplace dependency, and Gate 0 verifies the actual loopback server/scanner/BSL runtime;
20. scanner/API credentials are never stored in files, commands, logs, state, reports or Git;
21. static findings retain complete provenance and cannot establish ERP causality without runtime/case linkage and Gate 7;
22. no undeclared MCP/app/backend or unsupported manifest field is claimed;
23. repository history and package contain no confidential case data or credentials;
24. clean-session smoke tests cover capability inventory, installed/unavailable companions, under-evidenced cases, static-analysis non-causality, analysis-only work, scoped closure and `R3` blocking;
25. public repository, release and Plugin Directory submission are not marked complete before their separate product-side checks pass.
26. accounting/proportional paths require executable raw-row coverage, per-analytic reconciliation, observed allocation and independent before/after Gate 7;
27. machine case state rejects duplicate/global IDs and propagates supersession/invalidation through Evidence, Runs, Claims, reports and downstream Gates;
28. MXL/property-tree metadata cannot pass as row values without the required tabular profile;
29. secret response scans current tree, full history and the actual archive without echoing values.
30. every local resource referenced by a packaged skill resolves inside the installable plugin boundary; repository-root fixtures cannot substitute for package contents.

Report each control as `PASS | FAIL | WARNING` with exact evidence and remediation. Any critical `FAIL` blocks merge, repository publication, tag/release creation and global Plugin Directory submission.
