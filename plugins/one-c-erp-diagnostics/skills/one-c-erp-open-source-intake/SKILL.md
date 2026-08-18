---
name: one-c-erp-open-source-intake
description: Review an open-source 1C or agent tool before adding it to the diagnostics ecosystem.
---

# Open-source capability intake

Before adopting a repository, skill, CLI or MCP:

1. verify the authoritative source and license;
2. record checked commit/release and date;
3. define the exact problem it solves;
4. identify execution, network, credential and data risks;
5. prefer read-only use and pinned versions;
6. create a minimal sanitized regression fixture;
7. define failure/rollback behavior;
8. document whether it is bundled, optional, external or rejected;
9. do not copy private or non-licensed plugin implementation;
10. require CI and self-audit before merging.

OpenYellow may be used as a discovery catalog, never as proof of quality or safety by itself.
