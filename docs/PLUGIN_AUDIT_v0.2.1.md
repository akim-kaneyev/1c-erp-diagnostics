# Plugin and ecosystem self-audit — v0.2.1

Audit target: `one-c-erp-diagnostics` plugin, Gate 0–10 contract and `.agents/plugins/marketplace.json`.

Audit result: **PASS with four non-critical product/runtime warnings**. No critical control is `FAIL`.

## Controls

| # | Control | Status | Evidence |
|---|---|---|---|
| 1 | Manifest identity/version are consistent | PASS | Plugin manifest and `pyproject.toml` declare `0.2.1`; CI validates semver and matching versions. |
| 2 | Public metadata and policy URLs are present | PASS | Author, homepage, repository, MIT license, website, privacy and terms URLs are declared and validated. |
| 3 | Brand assets are valid | PASS | `composerIcon`, `logo` and `logoDark` exist and pass PNG signature/chunk/dimension/CRC validation. |
| 4 | One primary entrypoint owns the workflow | PASS | Root and packaged master skills require one user invocation and ordered Gate 0–10 execution. |
| 5 | Internal capability coverage is substantial and bounded | PASS | 31 packaged skills cover ERP domains, evidence, verification, risk, artifacts, releases and orchestration; normal plans remain bounded. |
| 6 | Marketplace exposes the intended ecosystem | PASS | Exact order: `one-c-erp-diagnostics`, `unica`, `1c-skills`, `1c-skills-py`. |
| 7 | Unica source is canonical and immutable | PASS | Source `IngvarConsulting/unica-marketplace`, path `plugins/unica`, release `v0.12.0` resolved to commit `aefc880f9bab606a5c55ed11af563b740054a549`. |
| 8 | 1C Skills sources are canonical and immutable | PASS | PowerShell ref `8cb7868145281d8e353831512cc1ffa72f1b5c89`; Python ref `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`. |
| 9 | External plugins require explicit installation | PASS | Every marketplace policy is `AVAILABLE` + `ON_INSTALL`; none is silently installed by default. |
| 10 | Third-party code/licensing boundaries are honest | PASS | External code is not copied or relicensed; LGPL/MIT sources and independent lifecycles are documented. |
| 11 | Runtime availability is not invented | PASS | Gate 0 distinguishes `available`, `confirmation_required`, `unavailable`, `prohibited`; marketplace presence is not treated as installation. |
| 12 | Companion selection is methodical | PASS | Exact task, evidence IDs, capability, version/ref, output/provenance, risk, falsifier and fallback are required. |
| 13 | Conflicting companion outputs remain visible | PASS | Inputs, versions, scopes and analytic keys are compared; majority voting is prohibited. |
| 14 | Case-specific causality remains evidence-first | PASS | External code/tool output is a hypothesis until linked to document → movement → register → consuming mechanism → result → symptom. |
| 15 | Gate 7 protects final causality | PASS | Final `УСТАНОВЛЕНО` is forbidden without a distinct adversarial review of original evidence. |
| 16 | Gate 9 protects result validation | PASS | Identical analytics before/after are required; disappearance of a UI error is insufficient. |
| 17 | High-impact actions are controlled | PASS | Production/accounting/access/closed-period actions are `R3` and require exact approval, rollback and validation plan. |
| 18 | Optional executable adapters are pinned | PASS | CI installs/imports `v8unpack==1.2.6` and `opensandbox==0.1.14` on Python 3.10/3.12. |
| 19 | Public package rejects sensitive artifacts | PASS | Validator blocks case input/work files, `.dt`, `.1CD`, backups, key material and obvious credential assignments. |
| 20 | Publication documentation is complete | PASS | README, privacy, terms, security, support, ecosystem architecture, release notes and publication checklist exist. |
| 21 | CI validates the complete contract | PASS | Run `32127125862` passed package validation, ecosystem validation and regression tests on Python 3.10 and 3.12. |

## Product/runtime warnings

### WARNING 1 — marketplace re-import pending

Repository CI validates the marketplace file and immutable refs, but does not prove that the current ChatGPT/Codex UI will import and render all four entries. Re-import `main` after merge and visually verify the plugin cards.

### WARNING 2 — cross-plugin invocation is host-dependent

A unified marketplace creates one installation/discovery space; it does not guarantee that every ChatGPT surface permits one plugin to invoke another. Gate 0 must report actual runtime capability and use fallback/`blocked` when cross-plugin delegation is unavailable.

### WARNING 3 — public repository not yet enabled

The repository remains private during this audit. Privacy/policy URLs and anonymous installation cannot be considered publicly reachable until visibility is changed and anonymous checks pass.

### WARNING 4 — global Plugin Directory submission pending

The personal/workspace marketplace is not the global Plugin Directory. OpenAI-side Create/Import and Publish/Submit review must be completed after public repository release.

## Conclusion

The v0.2.1 package materially expands the 1C workflow: it provides one verified marketplace for the primary diagnostics plugin, Unica and both 1C Skills runtimes, while retaining explicit permissions, source provenance and evidence/risk controls. The branch is technically eligible for merge. Public repository release, tag creation and global directory submission remain blocked until the documented product-side smoke tests pass.
