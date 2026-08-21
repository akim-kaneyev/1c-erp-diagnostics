# Plugin and ecosystem self-audit — v0.3.1 Release Candidate

Audit target: the factual Gate 0 discovery correction, plugin `one-c-erp-diagnostics`, the optional `sonarqube-bsl-local` adapter and the unchanged four-plugin marketplace.

Pre-release audit result: **No critical control is `FAIL`; GitHub publication and exact-version clean-session evidence are pending**.

| # | Control | Status | Evidence |
|---:|---|---|---|
| 1 | Manifest and package versions are synchronized at 0.3.1 | PASS | Manifest, pyproject, validators and tests share one patch version. |
| 2 | Named-tool absence cannot establish SonarQube unavailability | PASS | Local-static-analysis and capability-discovery skills require factual endpoint/scanner probes. |
| 3 | Host permission and authentication states are honest | PASS | Blocked execution and `401/403` map to separate `confirmation_required` reasons. |
| 4 | Discovery remains read-only | PASS | No service start, default login, token/project/profile creation or scan is authorized by Gate 0. |
| 5 | Static output remains non-causal | PASS | Runtime ERP evidence and Gate 7 remain mandatory. |
| 6 | Credential isolation is unchanged | PASS | Tokens remain excluded from commands, properties, files, logs, state, Git and chat. |
| 7 | Marketplace identity and composition are stable | PASS | The marketplace retains four entries and the existing installation ID. |
| 8 | Companion provenance is immutable | PASS | Unica `aefc880f9bab606a5c55ed11af563b740054a549`, PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`, Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`. |
| 9 | Brand and public policy assets remain present | PASS | Approved Velis assets and policy files are unchanged. |
| 10 | Local validators and tests pass | PASS | Public-release validator: 32 skills at 0.3.1; marketplace validator: four stable entries; eval validator: 14 cases; unit suite: 31 tests. |
| 11 | Python 3.10/3.12 CI and CodeQL pass | PENDING | Requires the protected release Pull Request. |
| 12 | Annotated tag and GitHub pre-release are published | PENDING | No v0.3.1 publication is claimed. |
| 13 | Clean-session runtime acceptance passes | PENDING | Must reproduce the reported cross-project Gate 0 path with the installed v0.3.1 package. |

## Known installation conflict

The inspected host has both `one-c-erp-diagnostics@one-c-erp-diagnostics-local` v0.1.2 and `one-c-erp-diagnostics@one-c-erp-diagnostics-marketplace` v0.3.0 enabled. They share the same plugin name. The obsolete local copy should be removed or disabled through Codex plugin management before clean-session acceptance; configuration files must not be hand-edited as an installation workaround.

## Conclusion

The patch directly closes the observed false-unavailable inference without weakening authentication, risk or causality controls. Local validation is complete; publication remains blocked until the protected GitHub checks pass. Runtime acceptance remains pending until a fresh task loads exactly one marketplace copy at v0.3.1 and performs the factual loopback/scanner preflight.
