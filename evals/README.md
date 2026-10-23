# Executable evaluation suite

This directory contains synthetic, data-free regression cases for the evidence-first Gate 0–10 contract. It is an acceptance framework, not evidence that a model or plugin version has passed the cases.

## Integrity rules

- Keep every tracked case synthetic and mark it with `"synthetic": true`.
- Do not place customer, company or production 1C data in this directory.
- Render prompts without exposing the `expect` block to the model.
- Do not manually shorten or rewrite a rendered prompt; the strict output instructions, capability block and skeleton are acceptance inputs.
- Treat each case `capabilities` array as an exact synthetic snapshot: results must contain the same names/statuses and no extras; an empty snapshot means `capabilities: []`.
- Internal reasoning steps, packaged skills and synthesis/review roles are not capabilities.
- Keep current-goal closure separate from linked-incident status. A bounded evidence-sufficiency assessment may close while the linked source/root-cause incident remains blocked/open.
- Assign claim status per statement. A directly evidenced limitation may be established without promoting source content or root cause.
- Store complete clean-session results and full Codex logs together in a new external run directory outside the repository. Hash both artifacts in schema-2 `run.json`; never reuse a failed or contaminated run ID.
- The rendered prompt must use the exact primary `plugin://` mention. Runtime cases use `web_search="disabled"`, a separate empty external working directory and the `no-tools` policy; any model tool call invalidates the case.
- Treat a structurally valid suite and a passed runtime run as different claims.
- Keep accounting helper/state-validator outputs as separate derived Evidence; never add their fields to the closed top-level `EVAL_RESULT_JSON` schema.
- The required suite contains 26 cases, including ten accounting/state/artifact/security regressions. Adding a case changes the complete clean-session acceptance set.
- The ten semantic regressions declare hidden `required_summary_markers`, per-marker `required_claim_statuses` and `required_claim_evidence_ids`. The rendered prompt exposes marker names but neither expected values, statuses nor Evidence mapping. `summary` must be the canonical marker-only assertion block, while `claims` must contain exactly one independently evidenced material conclusion per marker in the same order and preserve its own epistemic status and provenance. Result validation rejects missing, extra, wrong, contradictory, improperly promoted/demoted or misattributed totals, effect flags, state outcomes and safety decisions instead of checking only JSON shape.

## Commands

Validate case specifications and mandatory coverage:

```text
python tools/validate_evals.py
```

Render one prompt without its expected answer:

```text
python tools/validate_evals.py --render under-evidenced-cost
```

Validate one or more returned JSON results:

```text
python tools/validate_evals.py --results <external-run-dir>
python tools/validate_evals.py --results <external-run-dir> --require-complete
```

The strict release check additionally requires a schema-2 clean-session run manifest, exact source/plugin identity, per-case result and log hashes, and no-tools log validation; see `docs/RUNTIME_ACCEPTANCE.md`.
