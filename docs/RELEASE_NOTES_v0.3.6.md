# 1C ERP Diagnostics v0.3.6 — Exact Stale-Execution Runtime Contract

## Overview

Version 0.3.6 is a focused runtime-contract hotfix based on the exact clean-session
`stale-execution-result` returned by installed v0.3.5. The preceding
`capability-inventory` test passed in v0.3.5, but the stale-result case still returned
Gate 5 `passed`, Gate 7 `not_required`, Gate 10 `passed`, linked incident
`not_in_scope`, malformed claims/causal links/requested evidence/actions and three
unsupported `УСТАНОВЛЕНО` claims.

## Corrected behavior

- `final_status=ТРЕБУЕТ ПРОВЕРКИ`, `risk=R0`, `decision=EVIDENCE_REQUIRED`;
- current goal and linked incident remain `blocked`;
- Gates 0–4 pass, Gate 5 is `stale`, Gates 6–8 pass, Gate 9 is `not_required`, Gate 10 is `blocked`;
- capability snapshot remains empty;
- one material claim uses exactly `id`, `status`, `text`, `evidence_ids`, `falsifier` and remains below established;
- input/run/report identity facts are not copied into separate established claims;
- the logical execution graph is not emitted as the six-stage 1C causal chain;
- requested evidence is one string and actions remain empty.

## Regression coverage

The test suite now includes the exact v0.3.5 runtime shape and verifies independent
rejection of the wrong scope, Gate statuses, claim fields/statuses, causal-link fields,
object-valued evidence request and pseudo-action fields. The rendered synthetic prompt
states every required Gate and collection shape explicitly.

## Unchanged ecosystem and safety

- packaged skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`);
- 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- SonarQube, evidence lineage, execution identity, R0–R3 controls, full-history validation and Velis assets are unchanged.

## Acceptance boundary

Repository CI, CodeQL and publication checks prove package consistency only. Runtime
acceptance remains blocked until installed v0.3.6 passes `capability-inventory`,
`stale-execution-result`, `provenance-closure-broken` and then the complete hashed
16-case clean-session run.
