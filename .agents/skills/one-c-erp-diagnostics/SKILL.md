---
name: one-c-erp-diagnostics
description: Discover and run the repository's dynamic Gate 0-10 1C:ERP diagnostic orchestrator and verified Unica/1C Skills companion ecosystem.
---

# Repository entrypoint

1. Read repository-root `AGENTS.md`.
2. Read repository-root `SKILL.md`; it is authoritative.
3. Read `docs/ECOSYSTEM_MARKETPLACE.md` for canonical companion identities and boundaries.
4. Read `plugins/one-c-erp-diagnostics/skills/one-c-erp-diagnostics/SKILL.md` for the packaged runtime contract.
5. Resume from `STATE.md` when present.
6. Do not ask the user to manually chain internal skills.
7. Check `unica`, `1c-skills` and `1c-skills-py` at Gate 0; do not infer installation from marketplace presence.
8. Discover `sonarqube-bsl-local` separately as an optional host adapter. Do not add it to the marketplace or call it available until the loopback server, scanner, BSL plugin/profile, project and scoped authentication are confirmed.
9. Route a new static scan through `one-c-erp-local-static-analysis`; keep credentials out of commands/files/logs and never promote a static finding to ERP causality without runtime evidence and Gate 7.
10. For allocation, cost, month close, balances, postings or proportional algorithms, require the packaged raw-row accounting-invariants helper before root-cause or correction design; block build/load/activate until its PASS result and independent semantic Gate 7.
11. If an external capability is unavailable, use a documented fallback or mark the dependent node unavailable/blocked rather than simulating it.
