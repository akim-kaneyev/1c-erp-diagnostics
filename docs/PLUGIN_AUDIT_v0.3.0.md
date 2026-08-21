# Plugin and ecosystem self-audit — v0.3.0 Release Candidate

Audit target: plugin `one-c-erp-diagnostics`, Gate 0–10 contract, optional `sonarqube-bsl-local` capability, executable evaluation/runtime-acceptance gates and the unchanged four-plugin ecosystem marketplace.

Pre-release audit result: **No critical control is `FAIL`; external publication and clean-session runtime evidence are pending**. `PASS` below means the local package contract contains the stated control. It does not mean that GitHub CI, a Pull Request, tag, release or clean-session acceptance has completed.

## Controls

| # | Control | Status | Evidence |
|---|---|---|---|
| 1 | Manifest and project versions are synchronized | PASS | The release candidate contract requires both package version sources to declare `0.3.0`; the public validator checks equality and semantic versioning. |
| 2 | One primary entrypoint owns the workflow | PASS | Root and packaged orchestration preserve ordered Gate 0–10 processing. |
| 3 | Internal coverage is substantial and bounded | PASS | The primary plugin packages 32 skills, including the optional SonarQube BSL analysis skill. |
| 4 | SonarQube remains optional and runtime-discovered | PASS | Gate 0 inventories `sonarqube-bsl-local`; absence follows the documented fallback or blocked path and is never fabricated as availability. |
| 5 | Verified local analysis baseline is explicit | PASS | A read-only preflight reported server `UP` at `26.8.0.126808`, SonarScanner CLI `8.0.1.6346` and the reviewed communitybsl JAR. The protected plugin API returned `401` without a token, so full scan availability is not claimed. |
| 6 | Language-plugin provenance is immutable | PASS | Reviewed communitybsl artifact SHA-256 is `595F741AFD49BC7F1869B3F82F623821D519CECB399C56F154E55EA83DC7057B`. |
| 7 | Credentials are environment-only | PASS | Tokens are prohibited in repository files, scanner properties, reports, logs, case state and chat; retained output requires secret review. |
| 8 | Local scan side effects are classified | PASS | Analysis of sanitized local source on an already configured local instance is `R1` and records derived artifacts. |
| 9 | SonarQube administration requires exact approval | PASS | Project, token and administrative changes are `R2`; analysis authorization alone does not permit them. |
| 10 | Remote source transfer is high risk | PASS | Upload to a remote SonarQube destination is `R3` and requires explicit destination/data-scope approval and data minimization. |
| 11 | Static output cannot establish causality alone | PASS | A SonarQube issue remains a hypothesis until linked to runtime ERP evidence and accepted through Gate 7. |
| 12 | Automatic correction remains out of scope | PASS | Static analysis does not authorize code edits, issue acceptance, quality-gate override, administration or GitHub writes. |
| 13 | Analysis provenance is reproducible | PASS | The contract records source scope/identity, tool versions, analysis identifier, rule/location, result identity and limitations. |
| 14 | Marketplace identity is upgrade-compatible | PASS | Internal ID remains `one-c-erp-diagnostics-marketplace`; display identity is separate. |
| 15 | Marketplace composition is unchanged | PASS | Exactly four entries remain: primary plugin, Unica, 1C Skills PowerShell and 1C Skills Python; SonarQube is not a fifth plugin. |
| 16 | Companion sources remain immutable | PASS | Existing reviewed companion SHA selectors and independent permissions/licenses are unchanged. |
| 17 | Under-evidenced cases fail safely | PASS | Missing evidence cannot produce final `УСТАНОВЛЕНО`; the workflow requests the smallest sufficient evidence set. |
| 18 | Gate 7 protects final causality | PASS | Independent/adversarial review remains mandatory before final `УСТАНОВЛЕНО`. |
| 19 | High-impact ERP operations remain controlled | PASS | Closed-period, production, accounting and access writes remain `R3` with exact approval, rollback and Gate 9 validation. |
| 20 | Executable evaluation is a release gate | PASS | The release contract requires the executable evaluation suite and rejects documentation-only assurance. |
| 21 | Runtime acceptance is evidence-bearing | PASS | The release contract requires a version-matched clean-session run record and validates its structure before acceptance. |
| 22 | Sensitive artifacts are rejected | PASS | Public validation prohibits credentials, keys, raw case inputs, database dumps and backup artifacts. |
| 23 | Local validators and regression tests pass for the assembled candidate | PASS | On 2026-08-21 the public-package validator reported 32 skills/version 0.3.0, the ecosystem validator preserved four plugins, the eval validator reported 14 cases, and all 31 unit tests passed. |
| 24 | GitHub CI and CodeQL pass on the release Pull Request | PENDING | No `0.3.0` Pull Request or GitHub check result is claimed. |
| 25 | Protected-branch review and merge complete | PENDING | No review, approval or merge is claimed. |
| 26 | Versioned tag and GitHub release are published | PENDING | No `v0.3.0` tag or GitHub release is claimed. |
| 27 | Clean-session runtime acceptance completes | PENDING | Gate 0, under-evidenced, `R3 / NO-GO` and SonarQube available/unavailable paths still require a clean-session run. |

## Pending release evidence

### WARNING 1 — GitHub release workflow is pending

Create the protected-branch Pull Request, obtain required review, and wait for Python matrix and CodeQL results before merge. Only then create and verify an immutable `v0.3.0` tag and GitHub release.

### WARNING 2 — clean-session runtime acceptance is pending

Install or refresh the exact `0.3.0` candidate in a clean host session and retain the validated runtime-run record. Verify both discovery outcomes for `sonarqube-bsl-local`, safe fallback when unavailable, and absence of tokens from all retained evidence.

## Conclusion

The assembled local v0.3.0 contract and regression suite pass with no identified critical design failure. Its release status remains **candidate** until GitHub CI/CodeQL and protected-branch review complete. Runtime acceptance remains **pending** until a clean-session evidence record is produced and validated. This document does not claim a published tag, GitHub release or completed deployment.
