# v0.3.12 — UI SDK workflow for diagnostic interfaces

This candidate adds `one-c-erp-ui-design`, a scoped UI authoring workflow for diagnostic evidence viewers, dashboards and components. It applies UI SDK's behavior composition, named controls, shared state callbacks and agent-readable interactions while preserving evidence identity and backend authorization. Ordinary diagnoses and native 1C forms retain their existing workflows; strict `EVAL_RESULT_JSON` remains unchanged.

The package contains 35 skills and preserves the 26-case diagnostic suite, five-plugin marketplace, exact Claim status enum and approved Velis assets. The upstream `ui-sdk` skill is installed separately at user scope from reviewed commit `724a7d6c2d0ca1251a8eb6172462ae220c484714` under Apache-2.0. UI SDK code and upstream skill contents are not copied into the MIT plugin. JavaScript packages are selected and pinned within each actual UI project.

Unchanged companion pins:

| Companion | Immutable commit |
|---|---|
| Unica 0.12.3 | `c02e38d44a7dc238310172b9d790487f81aa4fb4` |
| 1C Skills PowerShell | `8cb7868145281d8e353831512cc1ffa72f1b5c89` |
| 1C Skills Python | `c1f79f5ac9f31c620b8508f75464f8c42c559ae4` |
| Jev 0.1.0 | `cf7e76607d4ec70592b24becadd0296dcda8177a` |

Validation covers source-file identities, global skill discovery, packaged references/lock, regression tests, PR CI/CodeQL and exact-version diagnostic runtime acceptance. Their actual outcomes are recorded on the candidate PR; source review alone does not imply a passed runtime run.

No web application, external model connection, WebMCP service or database bridge is started by this change. UI planning acceptance must not be described as browser or accounting validation. Rollback is reverting this plugin candidate and managing the independent user skill separately.
