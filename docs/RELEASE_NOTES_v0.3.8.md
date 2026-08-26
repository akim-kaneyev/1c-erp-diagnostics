# 1C ERP Diagnostics v0.3.8 — Deterministic Accounting and State Integrity

## Overview

Version 0.3.8 adds executable accounting, effect-classification and case-state controls derived from the reviewed 1C cost-allocation case. It preserves the evidence-first Gate 0–10 contract: arithmetic validation can reject inconsistent data, but it cannot establish a 1C root cause without independent Gate 7 evidence.

## Accounting and state controls

- exact fact/plan equality, share sum, deterministic allocation, residual, row coverage and observed-allocation checks without float arithmetic;
- independent before/after flags for completeness, allocation proportion, analytic key, cardinality and no material change;
- explicit `business_basis_required` when a proposal changes allocation proportions;
- executable cross-entity identity, run/input/tool/output freshness, lineage and downstream invalidation validation;
- MXL/XLSX property trees remain metadata until explicitly bound row evidence is available.

## Security and regression coverage

- bounded fail-closed XLSX/ZIP metadata and package scanning, including local/central header differences, credentials and user-machine paths;
- release-tree and complete reachable-history checks for unsafe paths, credentials, containers and symlinks;
- 10 new accounting/state/security regressions, expanding the validated synthetic `EVAL_RESULT_JSON` suite to 26 cases;
- the synchronized v0.3.8 candidate passes 143 repository unit and regression tests locally.

## Preserved ecosystem

- 32 packaged skills and marketplace ID `one-c-erp-diagnostics-marketplace`;
- Unica `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`);
- 1C Skills PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- approved Velis assets and independent-project trademark boundary.

## Validation boundary

Python 3.10/3.12 PR checks, CodeQL, package, marketplace, deterministic lock, publication-history and regression tests establish repository consistency only. Runtime acceptance remains blocked until the exact installed v0.3.8 package passes all 26 cases in fresh clean sessions and `tools/validate_runtime_run.py` validates the complete hashed run.
