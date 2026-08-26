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

Identical source across releases proves only source identity in the inspected scope. It does not prove that an unestablished defect persists. Similar vendor-card conditions do not prove the same technical cause. A clean cross-release test or official fixed status is counterevidence Gate 7 must consider, but without matching movements it is not a complete accounting protocol.
