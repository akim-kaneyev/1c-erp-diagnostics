# Plugin self-audit — v0.3.9

## Scope and escaped finding

The audit covers the v0.3.9 local candidate derived from public tag v0.3.8. The escaped defect was a package-boundary mismatch: the repository contained and tested `templates/case/STATE.json`, while the installed plugin did not contain it. The owning skill used an unlinked code path, so local-link governance did not detect the absence.

No known critical control remains failed in the local candidate. External CI/CodeQL, merge/publication and exact installed-v0.3.9 runtime acceptance remain separate warnings and blockers for their corresponding claims.

## Controls

| # | Status | Evidence | Remediation / remaining action |
|---:|:---:|---|---|
| 1 | PASS | `.codex-plugin/plugin.json`, `pyproject.toml`, `tools/validate_public_release.py` | None after synchronized v0.3.9 validation. |
| 2 | PASS | `validate_public_release.py` performs PNG structure/CRC validation for manifest assets. | None. |
| 3 | PASS | Root and packaged orchestrators retain Gate 0–10; contract tests cover Gate ownership. | None. |
| 4 | PASS | Capability-discovery and companion skills require observed availability. | None. |
| 5 | PASS | `one-c-erp-dynamic-plan` bounds actions and dependencies. | None. |
| 6 | PASS | Gate 7 adversarial verification remains mandatory before final `УСТАНОВЛЕНО`. | None. |
| 7 | PASS | Gate 9 and post-change skill require same-analytics comparison. | None. |
| 8 | PASS | Gate 10 separates current goal and linked incident and uses canonical statuses. | None. |
| 9 | PASS | Domain skills and evals retain the no-invented-metadata contract. | None. |
| 10 | PASS | Release-difference workflow requires official/current source verification. | None. |
| 11 | PASS | Unavailable capability is fallback/`blocked`, never simulated. | None. |
| 12 | PASS | `R0–R3` controls remain in root, packaged and action-decision surfaces. | None. |
| 13 | PASS | Marketplace validator requires exactly the reviewed four entries. | None. |
| 14 | PASS | Unica remains pinned to canonical `v0.12.0`. | None. |
| 15 | PASS | Both 1C Skills variants remain pinned to reviewed immutable refs. | None. |
| 16 | PASS | Marketplace entries retain explicit installation, license and permission boundaries. | None. |
| 17 | PASS | Ecosystem documentation states no companion implementation is embedded or relicensed. | None. |
| 18 | PASS | Open-source intake requires source, license, immutable identity, tests and fallback. | None. |
| 19 | PASS | SonarQube remains an optional host adapter with actual runtime discovery. | None. |
| 20 | PASS | Static-analysis and security contracts prohibit credential persistence and echo. | None. |
| 21 | PASS | Static findings remain non-causal without runtime/case linkage and Gate 7. | None. |
| 22 | PASS | Manifest/public validator rejects unsupported dependency and interface claims. | None. |
| 23 | PASS | Current-tree, history and archive validators cover confidential artifacts and credentials. | None. |
| 24 | WARNING | Historical public v0.3.8 run passed 26/26; v0.3.9 changes installed contents. | Run and hash all 26 cases against exact installed public v0.3.9. |
| 25 | WARNING | This is a local candidate; protected PR CI/CodeQL, merge, tag/release and Plugin Directory checks are not yet executed. | Complete each product-side gate without reusing repository validation as proof. |
| 26 | PASS | Accounting helper/evals cover raw rows, reconciliation, observed allocation and independent before/after review. | None. |
| 27 | PASS | State validator and tests enforce global ID uniqueness and invalidation closure. | None. |
| 28 | PASS | Artifact profile and evals keep property-tree metadata separate from primary rows. | None. |
| 29 | PASS | Security validators scan current tree, reachable history and actual archive with redacted output. | None. |
| 30 | PASS | `one-c-erp-case-state/assets/STATE.json`, validated links, public-release requirement and equality regression close the installable package boundary. | Preserve this control for every future packaged resource. |

## Decision

Repository candidate: **PASS with two external warnings**. Merge/publication/runtime-acceptance decision: **BLOCKED** until the focused Pull Request checks and exact installed-v0.3.9 clean-session run exist.
