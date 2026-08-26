# 1C ERP Diagnostics v0.3.7 — Exact Under-Evidenced Cost Contract

## Overview

Version 0.3.7 is a focused runtime-contract hotfix based on the exact clean-session
`under-evidenced-cost` result returned by installed v0.3.6. The first three priority
cases passed, but the fourth case still misclassified Gate 2/4/10 and emitted malformed
claims, requested-evidence objects and pseudo-actions.

## Corrected `EVAL_RESULT_JSON` behavior

- `final_status=ТРЕБУЕТ ПРОВЕРКИ`, `risk=R0`, `decision=EVIDENCE_REQUIRED`;
- current goal and linked incident remain `blocked`;
- Gates 0–3 pass, Gate 4 is blocked, Gate 5 is not required, Gates 6–8 pass,
  Gate 9 is not required and Gate 10 is blocked;
- Gate 2 passes after the supplied statement and its limitations are accounted for;
- one material claim uses exactly `id`, `status`, `text`, `evidence_ids`, `falsifier`
  and remains below established;
- a copied symptom statement cannot become an `УСТАНОВЛЕНО` cause claim;
- the causal chain remains incomplete and empty;
- requested evidence is a string list and actions remain empty.

## Regression coverage

The executable test suite contains the exact v0.3.6 response shape and rejects the
wrong Gate statuses, copied established symptom claim, malformed claim fields,
object-valued requested evidence and ad-hoc pseudo-action fields. The canonical result
passes the same validator.

## Unchanged ecosystem and safety

- packaged skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549`
  (`v0.12.0`);
- 1C Skills PowerShell remains pinned to
  `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to
  `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- SonarQube boundaries, provenance closure, execution identity, R0–R3 controls,
  full-history validation and approved Velis assets are unchanged.

## Validation boundary

Python 3.10/3.12, CodeQL, package, marketplace, publication-history and regression
checks establish repository consistency only. Runtime acceptance remains blocked until
installed v0.3.7 passes the four priority cases and the complete hashed 16-case
clean-session run.
