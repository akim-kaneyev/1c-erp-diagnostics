# Plugin and ecosystem self-audit — v0.2.2 Public Preview

Audit target: public repository `akim-kaneyev/1c-erp-diagnostics`, plugin `one-c-erp-diagnostics`, Gate 0–10 contract and unified marketplace.

Audit result: **PASS with three non-critical distribution/runtime warnings**. No critical control is `FAIL`.

## Controls

| # | Control | Status | Evidence |
|---|---|---|---|
| 1 | Public repository identity is correct | PASS | Repository is public under `akim-kaneyev/1c-erp-diagnostics`; the development repository remains separate. |
| 2 | Manifest and project versions match | PASS | Plugin manifest and `pyproject.toml` declare `0.2.2`; CI checks equality and semver. |
| 3 | Public metadata and policy URLs are present | PASS | Author, repository, website, privacy and terms URLs are declared. |
| 4 | Brand assets are valid | PASS | `composerIcon`, `logo` and `logoDark` pass PNG structural and CRC validation. |
| 5 | One primary entrypoint owns the workflow | PASS | Root and packaged skills require a single invocation and ordered Gate 0–10 processing. |
| 6 | Internal coverage is substantial and bounded | PASS | 31 packaged skills cover principal ERP domains, evidence, verification, risk, artifacts, releases and orchestration. |
| 7 | Marketplace identity is upgrade-compatible | PASS | Stable internal ID `one-c-erp-diagnostics-marketplace`; visual title remains `1C ERP Diagnostics Ecosystem`. |
| 8 | Marketplace exposes the intended ecosystem | PASS | Primary plugin, Unica, 1C Skills PowerShell and 1C Skills Python are declared. |
| 9 | External plugin sources are immutable | PASS | Unica and both 1C Skills entries use reviewed 40-character SHA selectors. |
| 10 | External plugins retain independent permissions and licenses | PASS | Every companion is separately installable with `AVAILABLE` / `ON_INSTALL`; no code is copied or relicensed. |
| 11 | Runtime availability is not invented | PASS | Gate 0 distinguishes `available`, `confirmation_required`, `unavailable` and `prohibited`; marketplace presence is not treated as installation. |
| 12 | Real companion discovery was smoke-tested | PASS | Unica and both 1C Skills runtimes were detected and probed read-only; tool limitations were recorded. |
| 13 | Unavailable capabilities are not simulated | PASS | OpenSandbox was reported unavailable when not exposed. |
| 14 | Case causality remains evidence-first | PASS | External code/tool output is a hypothesis until linked to document → movement → register → mechanism → result → symptom. |
| 15 | Under-evidenced cases are blocked safely | PASS | A month-close/cost symptom without records did not receive an invented cause and requested the smallest sufficient evidence set. |
| 16 | Gate 7 protects final causality | PASS | Unsupported final `УСТАНОВЛЕНО` was rejected in runtime testing. |
| 17 | Analysis-only work is controlled | PASS | Read-only analysis was classified `R0`; Gate 9 was `not_required` when no change occurred. |
| 18 | High-impact operations are controlled | PASS | Closed-period mass reposting was classified `R3` and received `NO-GO` without execution. |
| 19 | Scoped closure is unambiguous | PASS | Current-goal closure and linked-incident status are separated; decorated statuses such as `passed*` are prohibited and regression-tested. |
| 20 | Marketplace refresh works in place | PASS | The internal ID regression was fixed; the existing marketplace refreshed successfully after v0.2.2. |
| 21 | Sensitive artifacts are rejected | PASS | Validators and policies prohibit `.dt`, `.1CD`, backups, keys, credentials and raw case input/work files. |
| 22 | CI validates the complete contract | PASS | Package, ecosystem and regression validation pass on Python 3.10 and 3.12. |
| 23 | Public documentation is aligned | PASS | README, privacy, terms, security, support, release notes and this audit describe the v0.2.2 public preview. |

## Distribution/runtime warnings

### WARNING 1 — global Plugin Directory submission is pending

The public GitHub repository and personal/workspace marketplace do not automatically create a global directory listing. The OpenAI-side Create/Import and Publish/Submit flow must still be completed and reviewed.

### WARNING 2 — cross-plugin invocation is host-dependent

The unified marketplace provides one discovery and installation space. It does not guarantee that every ChatGPT or Codex surface permits one plugin to invoke another. Gate 0 must report the actual session capability and use fallback/`blocked` when delegation is unavailable.

### WARNING 3 — versioned GitHub pre-release is pending

The repository is public, but the annotated `v0.2.2` tag and GitHub pre-release must still be created on the approved launch commit. Until then, `main` is the installation source for the public preview.

## Conclusion

The v0.2.2 public-preview repository is technically and methodologically fit for public use. The implementation preserves evidence-first conclusions, explicit uncertainty, source provenance, companion permission boundaries and production-risk controls. Remaining work is distribution and project-presentation work rather than a blocker in the diagnostic contract.
