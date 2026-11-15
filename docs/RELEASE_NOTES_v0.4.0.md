# v0.4.0 — ready local diagnostic interface

The plugin now includes a production React/Vite viewer on UI SDK. It opens STATE.json or annotated bundles locally, shows evidence/claims/runs and Gate 0–10, filters and paginates without changing canonical records, opens source/lineage details, compares local source hashes and exports original JSON bytes. The installed skill launches its packaged viewer without a source checkout or Node.js. The approved Velis assets are reused unchanged.

The package contains 35 skills and preserves the exact EVAL_RESULT_JSON diagnostic contract, 26-case runtime suite and five-plugin marketplace. The local server exposes static bundled assets only and is restricted to loopback. No 1C bridge is installed or started. UI SDK browser component actions do not imply Codex MCP or ERP authority.

Runtime UI dependencies are lockfile-pinned. Their Apache-2.0/MIT license texts ship in the bundle; the original global ui-sdk skill remains independently installed. CI typechecks, runs human/agent interaction tests, rebuilds the committed bundle and runs Python/CodeQL checks. Final exact-installed Codex and real-browser results are recorded on the PR, not inferred from source review.

Unchanged companion pins:

| Companion | Immutable commit |
|---|---|
| Unica 0.12.3 | `c02e38d44a7dc238310172b9d790487f81aa4fb4` |
| 1C Skills PowerShell | `8cb7868145281d8e353831512cc1ffa72f1b5c89` |
| 1C Skills Python | `c1f79f5ac9f31c620b8508f75464f8c42c559ae4` |
| Jev 0.1.0 | `cf7e76607d4ec70592b24becadd0296dcda8177a` |

The UI acceptance covers file-based diagnostic work. It does not claim live ERP accounting acceptance. Revert the plugin change and stop the viewer to roll back; no database state is changed.
