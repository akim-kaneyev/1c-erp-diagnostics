# 1C ERP Diagnostics v0.3.2 — Provenance and Publication Integrity

## Overview

Version 0.3.2 strengthens the evidence-first harness without adding a new agent topology or copying external implementation code. The patch adds explicit artifact derivation lineage, provenance closure for material conclusions, execution identity for tool/runtime evidence, stale-result handling, behavioral eval coverage, and a full-history publication-integrity check.

## Diagnostic correctness changes

- derived evidence must identify its parent Evidence ID(s), transformation, tool/version/ref, execution run when applicable and output identity/hash;
- material claims use provenance closure `closed | open | broken` across `source artifact → inspected/derived evidence → claim premise → causal link → conclusion`;
- preliminary/final `УСТАНОВЛЕНО` cannot depend on an unanchored material derivation;
- executable evidence records `run_id`, `case_id`, material input identities/hashes, tool/runtime version/ref and output identity;
- a report from another case, changed input generation or otherwise mismatched execution identity becomes `stale` until rerun or deterministic equivalence is proven;
- Gate 7 independently checks evidence coverage, provenance closure and execution freshness.

## Release-integrity changes

- CI now checks out full Git history (`fetch-depth: 0`);
- `tools/validate_publication_history.py` verifies that the `git archive HEAD` file set matches the tracked release tree;
- the publication validator scans historical paths for prohibited database/backups, private-key/environment artifacts and case data;
- manageable historical text blobs are scanned for plaintext credential assignments and user-machine absolute paths;
- a shallow checkout blocks the history-safety claim instead of silently reducing coverage.

## Evaluation coverage

The executable Gate 0–10 suite grows from 14 to 16 synthetic cases. New required controls are:

- `provenance_closure` — an unanchored derived table cannot establish source content or a final cause;
- `execution_identity` — an old tool report from a different input generation cannot prove the current state.

## Unchanged ecosystem and safety boundaries

- packaged specialist skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with exactly four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549`;
- 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- `R0–R3`, Gate 7, validation ladder and SonarQube credential/data boundaries remain in force;
- no code from `grok-bot-0.18-reconstructed`, its renderer, inference router or proprietary reconstructed artifacts is copied into this repository.

## Upgrade

After v0.3.2 is merged/published, refresh the existing marketplace installation and start a new clean task so the host loads the updated master skill and version. Exact-version clean-session runtime acceptance remains a separate release evidence step.
