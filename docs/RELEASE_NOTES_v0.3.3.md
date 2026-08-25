# 1C ERP Diagnostics v0.3.3 — Strict Runtime Eval Contract

## Overview

Version 0.3.3 is a focused runtime-contract hotfix. The first clean-chat smoke test of installed v0.3.2 correctly rejected a stale report semantically, but its `EVAL_RESULT_JSON` violated the published machine-readable contract: it returned `R3 / NO-GO` for a read-only evidence decision, used the wrong linked-incident scope, malformed claim/link/action items and marked a logical freshness argument as a complete six-stage 1C causal chain.

The hotfix strengthens the authoritative, packaged and portable orchestrator instructions without changing the 16 synthetic cases or their hidden expectations.

## Fixed behavior

- literal `EVAL_RESULT_JSON` activates a strict one-JSON-object mode with no Markdown or extra text;
- a supplied skeleton is an exact schema contract: keys, types and field names cannot be added, removed or renamed;
- Gate statuses are restricted to `pending | passed | blocked | failed | stale | not_required` in lower case;
- Gate status now explicitly describes whether the Gate procedure completed correctly, not whether a hypothesis was proved;
- a Gate may pass because it correctly rejects an unsupported cause or stale-evidence reuse;
- action risk is separated from evidentiary severity: read-only rejection of stale evidence is `R0`, while `R3` remains reserved for production/accounting/access/closed-period/configuration/external writes;
- missing current evidence, rerun or proved equivalence produces `EVIDENCE_REQUIRED`; `NO-GO` remains reserved for an unsafe/prohibited/unapproved in-scope action;
- `linked_incident_status = not_in_scope` is permitted only when the prompt explicitly excludes the underlying incident;
- claim items must use exact fields `{id, status, text, evidence_ids, falsifier}` and contain material conclusions rather than copied Evidence summaries;
- `causal_chain.complete` can be true only for all six canonical 1C stages in order, with structured `{stage, evidence_ids}` links;
- `actions` is empty when no in-scope action exists and otherwise uses the exact structured action contract.

## Regression coverage

The dynamic-contract regression suite now checks that the authoritative, packaged, portable, final-review, risk-control and action-decision skills all preserve the strict evaluation semantics. The existing `stale-execution-result` case continues to require `Gate 5 = stale`, `Gate 7 = passed`, `Gate 10 = blocked`, `R0`, `EVIDENCE_REQUIRED` and an unresolved current-state conclusion.

## Unchanged ecosystem and safety

- packaged skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with exactly four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`);
- 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- artifact provenance closure, execution identity, full-history publication validation, SonarQube credential boundaries and `R0–R3` write controls remain unchanged;
- the approved Velis brand assets remain unchanged;
- no external implementation code is copied.

## Release validation

Before merge/publication, the candidate must pass public-package validation, publication-history validation, marketplace validation, the 16-case eval specification, all unit regressions on Python 3.10/3.12 and required CodeQL/ruleset checks. These checks establish repository-contract consistency; they do not replace exact-version clean-session runtime acceptance.

## Upgrade and runtime re-test

After v0.3.3 is merged and the marketplace is refreshed, start a new clean chat and run the canonical rendered `stale-execution-result` and `provenance-closure-broken` prompts. Save their exact JSON outputs and validate them with `tools/validate_evals.py`. Runtime acceptance remains blocked until the complete exact-version clean-session suite is recorded and passes `tools/validate_runtime_run.py`.
