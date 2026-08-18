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
- record commands, versions, inputs and outputs;
- sandbox output is evidence to evaluate, not truth;
- expire/destroy disposable environments when finished.

If no executable validation is needed, mark `not_required`. If it is required for the claimed result and unavailable, mark `blocked`.
