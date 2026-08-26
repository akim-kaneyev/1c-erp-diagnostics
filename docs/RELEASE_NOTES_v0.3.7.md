# 1C ERP Diagnostics v0.3.7 — Verified Visual Explanation

## Overview

Version 0.3.7 adds an optional Visual Explanation sidecar for normal narrative results. It supports exactly `diagram` and `sticky` and runs only after Gate 6 and Gate 7 have passed.

The change is presentation-only. Gate 0–10 semantics, claim statuses, risk/decision rules, causal completeness, provenance closure and the strict evaluation schema are unchanged.

## Presentation contract

- `diagram` projects only Gate 7-reviewed Claim/Evidence relationships or canonical causal stages and leaves unsupported transitions as visible gaps;
- `sticky` projects compact reviewed-result, decisive-evidence and uncertainty/falsifier cards;
- every statement retains existing Claim IDs, Evidence IDs and final statuses;
- the view creates no fact, Evidence item, claim support, causal edge or provenance closure;
- every view is labelled `Presentation only — not evidence`;
- the modes are plain-language requests, not slash commands, packaged skills, runtime capabilities or image-generation dependencies;
- an incomplete Gate 6/7 prerequisite omits the sidecar without changing or reopening a Gate.

## Strict evaluation boundary

Literal `EVAL_RESULT_JSON` disables Visual Explanation unconditionally. The result remains exactly the supplied JSON skeleton: no Visual-Explanation-derived field, trailing prose, capability, pseudo-claim, action or Evidence ID is permitted.

Regression coverage verifies that `visual_explanation` is absent from `evals/result.schema.json`, the validator result keys and rendered skeleton, and that an extra visual field or invented visual capability is rejected. Existing eval cases and Gate semantics are unchanged.

The deterministic skill-lock writer now emits LF on every platform, preventing a Windows-only line-ending rewrite from obscuring the actual runtime-surface hash changes.

## Documentation and examples

The authoritative, packaged and portable orchestrators plus final review and capability discovery now carry the same boundary. README, architecture, evidence model, quick-start examples, plugin smoke tests and privacy text document the two modes and their non-evidentiary role.

## Unchanged ecosystem and safety

- packaged skill count remains 32;
- marketplace ID remains `one-c-erp-diagnostics-marketplace` with four entries;
- Unica remains pinned to `aefc880f9bab606a5c55ed11af563b740054a549` (`v0.12.0`);
- 1C Skills PowerShell remains pinned to `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python remains pinned to `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`;
- SonarQube boundaries, R0–R3 controls, full-history validation, privacy policy and approved Velis assets are unchanged.

## Acceptance boundary

Repository validation, protected Pull Request CI and CodeQL establish package consistency only. Runtime acceptance remains blocked until installed v0.3.7 passes the priority strict cases, the normal `diagram`/`sticky` smoke checks and the complete hashed 16-case clean-session run.
