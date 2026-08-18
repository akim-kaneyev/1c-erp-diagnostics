---
name: one-c-erp-release-difference
description: Compare 1C platform/configuration releases and determine whether a documented change can explain the observed case behavior.
---

# Release difference analysis

1. Establish the exact platform and configuration releases from evidence.
2. Verify current release notes, vendor documentation or supplied source diff.
3. Separate documented mechanism change from case-specific proof.
4. Identify the first changed module/object only when confirmed by source or metadata.
5. Compare the same test scenario on both releases when feasible.
6. Record alternative causes such as NSI, extensions, rights, data state and posting chronology.

A release difference is `УСТАНОВЛЕНО` as the cause only when the behavior is reproducible or the changed mechanism is connected to the user's exact record chain.
