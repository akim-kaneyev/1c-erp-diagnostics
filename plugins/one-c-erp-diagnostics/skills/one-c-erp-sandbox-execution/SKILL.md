---
name: one-c-erp-sandbox-execution
description: Decide when isolated execution such as OpenSandbox materially helps a 1C:ERP diagnostic and control it safely.
---

# Sandbox execution

Use for Gate 5 only when executable validation adds value: parser testing, repeatable comparisons, running Codex/scripts on sanitized case files, or evaluating an untrusted tool.

Controls:
- minimum sanitized data only;
- never production `.dt` or plaintext secrets;
- restrict outbound network where practical;
- sandbox output is evidence to evaluate, not truth;
- expire/destroy disposable environments when finished.

## Execution identity contract

Every executable result later used as evidence must be tied to the exact run that produced it. Record:

- unique `run_id` and current `case_id`;
- input Evidence IDs plus their hashes/stable identifiers;
- tool/runtime identity and version/ref;
- command/operation without secrets;
- start/completion timestamp when exposed;
- output location plus SHA-256 or stable output identifier;
- exit/status and material limitations.

Before reusing an earlier result, compare its case and input identities with the current state. A result from another case, different input hash, older artifact generation or execution performed before a material input change is `stale`. Do not silently reuse it: rerun the operation or prove deterministic equivalence. Mark downstream evidence/claims and Gate 5 `stale`/`blocked` as appropriate until refreshed.

If no executable validation is needed, mark `not_required`. If it is required for the claimed result and unavailable, mark `blocked`.
