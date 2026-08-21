# Executable evaluation suite

This directory contains synthetic, data-free regression cases for the evidence-first Gate 0–10 contract. It is an acceptance framework, not evidence that a model or plugin version has passed the cases.

## Integrity rules

- Keep every tracked case synthetic and mark it with `"synthetic": true`.
- Do not place customer, company or production 1C data in this directory.
- Render prompts without exposing the `expect` block to the model.
- Store actual clean-session outputs under `evals/runs/`; that directory is ignored by Git.
- Treat a structurally valid suite and a passed runtime run as different claims.

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
python tools/validate_evals.py --results evals/runs/<run-id>
python tools/validate_evals.py --results evals/runs/<run-id> --require-complete
```

The strict release check additionally requires a clean-session run manifest and SHA-256 hashes; see `docs/RUNTIME_ACCEPTANCE.md`.
