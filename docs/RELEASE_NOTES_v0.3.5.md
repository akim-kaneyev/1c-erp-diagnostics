# 1C ERP Diagnostics v0.3.5 — Capability Inventory Output Contract

## Overview

Version 0.3.5 is a focused runtime-contract hotfix based on the exact clean-session `capability-inventory` result returned by installed v0.3.4.

The v0.3.4 runtime correctly preserved the four supplied capability statuses, `risk=R0`, `decision=NO_ACTION` and `causal_chain.complete=false`. It nevertheless failed the official `EVAL_RESULT_JSON` contract in six material ways:

- returned `final_status=УСТАНОВЛЕНО` instead of `ТРЕБУЕТ ПРОВЕРКИ`;
- returned Gate 10 `not_required` although the bounded inventory goal was closed;
- emitted `evidence_id` inside capability rows instead of mandatory `simulated=false`;
- emitted malformed claim objects using `claim/status/evidence_ids`;
- promoted six capability observations to `УСТАНОВЛЕНО` claims although the case permits zero established claims;
- combined `УСТАНОВЛЕНО` with Gate 7 `not_required`, Gate 10 `not_required` and an incomplete causal chain.

Runtime acceptance therefore remains **BLOCKED** until the exact installed v0.3.5 case is rerun and validated.

## Fixed behavior

The authoritative, packaged, portable, capability-discovery and final-review contracts now define an explicit inventory-only acceptance profile:

- `final_status=ТРЕБУЕТ ПРОВЕРКИ` because a capability inventory is not a 1C/root-cause conclusion;
- `risk=R0`, `decision=NO_ACTION`;
- `current_goal_status=closed`, `linked_incident_status=not_in_scope`;
- Gate 0 and Gate 10 are `passed`; Gates 1–9 are `not_required`;
- each capability item is exactly `{name, status, simulated}` with `simulated=false`;
- `evidence_id`, category, purpose, provenance and other extra capability fields are forbidden in strict output;
- snapshot evidence is recorded only in top-level `evidence_ids_used`;
- capability rows are not diagnostic claims, so `claims=[]`;
- `causal_chain={complete:false,links:[]}`, `requested_evidence=[]`, `actions=[]`.

The contract now states the cross-field invariants directly: a closed current goal requires Gate 10 `passed`; `final_status=УСТАНОВЛЕНО` requires Gate 7 `passed`, Gate 10 `passed`, a closed goal and a complete six-stage causal chain.

## Evaluation and regression coverage

The canonical `capability-inventory` case now renders the complete expected semantic profile and requires all eleven Gate statuses explicitly.

The runtime regression suite adds:

- a canonical validator-conformant capability-inventory result;
- an exact reproduction of the observed v0.3.4 result shape;
- assertions rejecting the wrong final status and Gate 10 state;
- assertions rejecting `evidence_id` in capability items and missing `simulated`;
- assertions rejecting malformed claim objects and six established claims;
- assertions rejecting `УСТАНОВЛЕНО` without Gate 7, Gate 10 and complete causality;
- rendered-prompt checks for the inventory-only contract.

## Unchanged ecosystem and safety

- packaged skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with exactly four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`);
- 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- artifact provenance closure, execution identity, deterministic skill locking, full-history publication validation, SonarQube credential boundaries and `R0–R3` controls remain in force;
- approved Velis assets remain unchanged;
- no new agent, packaged skill, dependency, hosted service or write capability is added.

## Release validation

Before merge, the candidate must pass public-package validation, skill governance and deterministic lock validation, publication-history validation, marketplace validation, the 16-case eval specification, all unit regressions on Python 3.10/3.12 and required CodeQL/ruleset checks.

These checks prove repository-contract consistency only. They do not prove runtime behavior of an installed plugin/model/session combination.

## Upgrade and runtime re-test

After v0.3.5 is merged and the marketplace installation is refreshed, run the exact rendered `capability-inventory` prompt in a new clean session. Save the single JSON result and validate it with `tools/validate_evals.py`.

Then repeat the priority `stale-execution-result` and `provenance-closure-broken` cases to confirm no regression. Complete runtime acceptance remains blocked until all 16 clean-session results are hashed, recorded and accepted by `tools/validate_runtime_run.py`.
