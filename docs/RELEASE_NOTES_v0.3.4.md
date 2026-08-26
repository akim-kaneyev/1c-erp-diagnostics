# 1C ERP Diagnostics v0.3.4 — Provenance Scope and Capability Snapshot Contract

## Overview

Version 0.3.4 is a focused runtime-contract hotfix based on the second exact clean-chat smoke test of installed v0.3.3.

The canonical `stale-execution-result` test passed after v0.3.3: the runtime returned `R0`, `EVIDENCE_REQUIRED`, linked incident `blocked`, Gate 5 `stale`, Gate 7 `passed`, Gate 10 `blocked`, exact claim fields, `causal_chain.complete=false` and empty actions/capabilities.

The subsequent `provenance-closure-broken` test preserved the substantive conclusion correctly—the derived value did not prove source content or causality—but exposed two remaining contract boundaries:

- it set `linked_incident_status=not_in_scope` although the unresolved source/root-cause question was not explicitly excluded;
- it invented internal reasoning, synthesis and review operations as runtime capabilities even though the synthetic case declared no capabilities.

The same response also showed that the original expectation was too coarse: the directly supplied absence of parent/derivation/run/output identifiers is a legitimate established evidence limitation, even though source content, S-1→D-1 derivation and root cause remain unproved.

## Fixed behavior

- synthetic `EVAL_RESULT_JSON` capability output is now deterministic and must exactly match the case-declared capability snapshot;
- internal reasoning steps, packaged skills, synthesis/review roles and invented tool names are explicitly prohibited as capabilities;
- an empty synthetic capability snapshot requires `capabilities: []`;
- `tools/validate_evals.py` now rejects unexpected, omitted or status-mismatched synthetic capabilities;
- `not_in_scope` remains restricted to an explicit scope exclusion;
- a bounded evidence-sufficiency/provenance assessment may close its current goal after correctly determining that more evidence is required, while the linked source/root-cause incident remains `blocked` or `open`;
- `EVIDENCE_REQUIRED` therefore does not automatically force every narrow assessment goal to remain blocked;
- claim status is evaluated per statement: a directly evidenced missing-lineage limitation may be `УСТАНОВЛЕНО`, while source content, derivation relationship and root cause remain `ТРЕБУЕТ ПРОВЕРКИ`;
- the canonical `provenance-closure-broken` expectation is aligned to these semantics: current goal closed, linked incident blocked, Gate 2/6/7/8/10 passed, exact empty capability snapshot and at most one established limitation claim.

## Regression coverage

The runtime-contract test suite now includes:

- a canonical passing stale-execution result;
- rejection of the reproduced v0.3.2 risk/decision/schema/causal-chain shape;
- a canonical passing provenance-sufficiency result with scoped closure and one established missing-lineage fact;
- rejection of the reproduced v0.3.3 `not_in_scope` plus invented-capabilities shape;
- an independent check that an empty synthetic capability snapshot rejects any invented capability;
- rendered-prompt checks requiring the explicit `capabilities: []` instruction.

## Unchanged ecosystem and safety

- packaged skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with exactly four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`);
- 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- artifact provenance closure, execution identity, full-history publication validation, SonarQube credential boundaries and `R0–R3` write controls remain in force;
- the approved Velis brand assets remain unchanged;
- no external implementation code, new agent, hosted service or write capability is added.

## Release validation

Before merge/publication, the candidate must pass public-package validation, publication-history validation, marketplace validation, the 16-case eval specification, all unit regressions on Python 3.10/3.12 and required CodeQL/ruleset checks. These checks establish repository-contract consistency; they do not replace exact-version clean-session runtime acceptance.

## Upgrade and runtime re-test

After v0.3.4 is merged and the marketplace is refreshed, start new clean chats and run the exact rendered `stale-execution-result` and `provenance-closure-broken` prompts. Save their JSON outputs and validate them with `tools/validate_evals.py`. Runtime acceptance remains blocked until the complete exact-version 16-case clean-session run is recorded and passes `tools/validate_runtime_run.py`.
