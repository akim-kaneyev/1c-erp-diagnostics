# Clean-session runtime acceptance

Static validation proves that the package and evaluation contract are internally consistent. It does not prove that a particular plugin/model/runtime combination follows the contract. Publication readiness therefore requires a separate complete clean-session run.

## Release gate

A runtime run passes only when all conditions are true:

1. the exact candidate plugin version is installed;
2. every case from `evals/suite.json` is executed in a clean session;
3. the runner sees the rendered prompt and evidence, but not the case `expect` block;
4. every response is saved as one `*.result.json` file;
5. `run.json` identifies the source commit, host, surface, installed version and timestamp;
6. every result hash matches and every case-specific/global control passes;
7. no case is missing, duplicated or unreferenced.

For v0.3.2, the suite also exercises provenance closure and execution-identity freshness. A prior tool result for different material inputs must not be accepted as current evidence.

Until this command passes, runtime acceptance is `blocked`:

```text
python tools/validate_runtime_run.py evals/runs/<run-id>
```

## Procedure

Create a local ignored directory under `evals/runs/`. Render each prompt without expectations:

```text
python tools/validate_evals.py --render <case-id>
```

Run the rendered prompt in a clean task with the exact candidate installed. Save the single returned JSON object as `<case-id>.result.json`. Calculate SHA-256 for each file and create `run.json`:

```json
{
  "schema_version": 1,
  "run_id": "v0-3-2-clean-example",
  "suite": "1C ERP Diagnostics Gate 0-10 acceptance",
  "plugin_version": "0.3.2",
  "source_commit": "0000000000000000000000000000000000000000",
  "executed_at": "2026-08-25T10:00:00+03:00",
  "environment": {
    "surface": "Codex desktop",
    "host": "clean test host identifier",
    "clean_session": true,
    "installed_plugin_version": "0.3.2",
    "expectations_visible_to_runner": false
  },
  "results": [
    {
      "case_id": "capability-inventory",
      "file": "capability-inventory.result.json",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  ]
}
```

The zero values are examples of required shape, not valid release evidence. The strict validator rejects incomplete suites, placeholder hashes, hash mismatches, wrong versions and non-clean runs.

## Result interpretation

- `EVAL SUITE VALIDATION: PASS` — specifications and mandatory coverage are valid.
- `EVAL RESULT VALIDATION: PASS` — supplied result files satisfy their contracts.
- `RUNTIME ACCEPTANCE: PASS` — one complete, hashed clean-session run satisfies the strict release gate.
- `RUNTIME ACCEPTANCE: BLOCKED` — the plugin version must not be described as runtime-accepted.

Repository/publication integrity is separate: `python tools/validate_publication_history.py` proves archive/history hygiene, not model/runtime behavior. Both claims must remain distinct.
