# Plugin and ecosystem self-audit — v0.2.3 Public Preview

Audit target: public repository `akim-kaneyev/1c-erp-diagnostics`, plugin `one-c-erp-diagnostics`, Gate 0–10 contract, approved Velis assets, unified marketplace, repository security controls and the published v0.2.3 pre-release.

Post-release audit result: **PASS with two non-critical distribution/runtime warnings**. No critical control is `FAIL`.

## Controls

| # | Control | Status | Evidence |
|---|---|---|---|
| 1 | Public repository identity is correct | PASS | Repository is public under `akim-kaneyev/1c-erp-diagnostics`; private development history remains separate. |
| 2 | Manifest and project versions match | PASS | Plugin manifest and `pyproject.toml` declare `0.2.3`; CI checks equality and semver. |
| 3 | Public metadata and policy URLs are present | PASS | Author, repository, website, privacy and terms URLs are declared. |
| 4 | Approved brand assets are packaged | PASS | `composerIcon`, `logo` and `logoDark` use the approved white-dog Velis identity and pass PNG structural/CRC validation. |
| 5 | Trademark boundary is explicit | PASS | The visual artwork does not reproduce the corporate 1C graphic logo; descriptive product references and independence notice remain. |
| 6 | One primary entrypoint owns the workflow | PASS | Root and packaged skills require a single invocation and ordered Gate 0–10 processing. |
| 7 | Internal coverage is substantial and bounded | PASS | 31 packaged skills cover principal ERP domains, evidence, verification, risk, artifacts, releases and orchestration. |
| 8 | Marketplace identity is upgrade-compatible | PASS | Stable internal ID `one-c-erp-diagnostics-marketplace`; visual title remains `1C ERP Diagnostics Ecosystem`. |
| 9 | Marketplace exposes the intended ecosystem | PASS | Primary plugin, Unica, 1C Skills PowerShell and 1C Skills Python are declared. |
| 10 | External plugin sources are immutable | PASS | Unica and both 1C Skills entries use reviewed 40-character SHA selectors. |
| 11 | External plugins retain independent permissions and licenses | PASS | Every companion is separately installable with `AVAILABLE` / `ON_INSTALL`; no code is copied or relicensed. |
| 12 | Runtime availability is not invented | PASS | Gate 0 distinguishes `available`, `confirmation_required`, `unavailable` and `prohibited`; marketplace presence is not treated as installation. |
| 13 | Case causality remains evidence-first | PASS | External output is a hypothesis until linked to document → movement → register → mechanism → result → symptom. |
| 14 | Under-evidenced cases are blocked safely | PASS | Missing evidence cannot produce final `УСТАНОВЛЕНО`; the workflow requests the smallest sufficient evidence set. |
| 15 | Gate 7 protects final causality | PASS | Unsupported final `УСТАНОВЛЕНО` is prohibited by the master and packaged contracts. |
| 16 | Analysis-only work is controlled | PASS | Read-only analysis is `R0`; Gate 9 may be `not_required` when no change occurred. |
| 17 | High-impact operations are controlled | PASS | Closed-period, production, accounting and access writes remain `R3` and require exact approval, rollback and post-change validation. |
| 18 | Scoped closure is unambiguous | PASS | Current-goal closure and linked-incident status are separate; decorated statuses such as `passed*` are prohibited. |
| 19 | Sensitive artifacts are rejected | PASS | Validators and policies prohibit `.dt`, `.1CD`, backups, keys, credentials and raw case input/work files. |
| 20 | CI validates the complete package | PASS | Public-package, ecosystem and regression workflows passed on Python 3.10 and 3.12 for release PR #12. |
| 21 | `main` is protected | PASS | Active ruleset requires Pull Request, squash merge, linear history, resolved conversations, current branch state, Python 3.10/3.12 checks and CodeQL results; force-push and deletion are blocked. |
| 22 | Code scanning is operational | PASS | CodeQL default setup completed for GitHub Actions and Python; the initial `main` scan succeeded with zero open alerts. |
| 23 | Vulnerability intake is private | PASS | Private vulnerability reporting is enabled. |
| 24 | Dependency monitoring is enabled | PASS | Dependency graph, Dependabot alerts and Dependabot security updates are enabled; version updates remain governed by `.github/dependabot.yml`. |
| 25 | Secret controls are enabled | PASS | Secret scanning and push protection are enabled. |
| 26 | Public documentation is aligned | PASS | README, privacy, changelog, release notes, audit, publishing guide, validators and tests describe `0.2.3`. |
| 27 | Versioned release is immutable and reproducible | PASS | Annotated tag `v0.2.3` resolves to approved commit `97cebacfe6a8755b89f7fd9231ffdd639febc33c`; GitHub pre-release metadata was verified. |
| 28 | Public release artifacts are externally accessible | PASS | Anonymous checks without an authorization token verified tagged policies/docs, Velis PNG assets and both GitHub source archives. |

## Distribution/runtime warnings

### WARNING 1 — clean-session v0.2.3 smoke tests are pending

After marketplace refresh, repeat Gate 0, the under-evidenced case and the scoped `R3 / NO-GO` test. The R3 result must state `Current goal: closed; linked incident: open` and use only canonical gate statuses.

### WARNING 2 — Plugin Directory publication is separate

The public repository and personal/workspace marketplace do not automatically create a global listing. OpenAI-side publication/import must be completed where the supported Publish action is available, followed by installation and smoke testing in a clean ChatGPT session.

## Conclusion

The v0.2.3 package, annotated tag and GitHub pre-release are published and externally retrievable. Repository engineering and GitHub distribution are complete. Remaining work is limited to refreshing the installed marketplace, repeating the clean-session runtime tests, optional GitHub-profile presentation and separate ChatGPT Plugin Directory publication.
