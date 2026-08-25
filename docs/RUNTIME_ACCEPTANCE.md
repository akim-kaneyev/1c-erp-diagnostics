# Clean-session runtime acceptance

Static validation proves that the package and evaluation contract are internally consistent. It does not prove that a particular plugin/model/runtime combination follows the contract. Publication readiness therefore requires a separate complete clean-session run.

## Release gate

A runtime run passes only when all conditions are true:

1. the exact candidate plugin version is installed;
2. every case from `evals/suite.json` is executed in a clean session;
3. the runner sees the exact prompt rendered by `tools/validate_evals.py`, including the strict output instructions and skeleton, but not the case `expect` block;
4. every response is exactly one JSON object and is saved as one `*.result.json` file;
5. every result passes the exact field/type/status/semantic checks in `tools/validate_evals.py`;
6. `run.json` identifies the source commit, host, surface, installed version and timestamp;
7. every result hash matches and every case-specific/global control passes;
8. no case is missing, duplicated or unreferenced.

The suite exercises provenance closure and execution-identity freshness. A prior tool result for different material inputs must not be accepted as current evidence.

Version 0.3.3 additionally treats strict JSON conformance as runtime behavior, not formatting polish. A semantically plausible response still fails when it uses the wrong action risk/decision, noncanonical Gate values, wrong linked-incident scope, renamed/missing claim fields, string arrays instead of structured objects, or false six-stage causal-chain completeness.

Until this command passes, runtime acceptance is `blocked`:

```text
python tools/validate_runtime_run.py evals/runs/<run-id>
```

## Procedure

Create a local ignored directory under `evals/runs/`. Render each prompt without expectations:

```text
python tools/validate_evals.py --render <case-id>
```

Do not shorten or manually rewrite the rendered prompt. Run it in a clean task with the exact candidate installed. Save the single returned JSON object as `<case-id>.result.json`, then validate it immediately:

```text
python tools/validate_evals.py --results evals/runs/<run-id>/<case-id>.result.json
```

Calculate SHA-256 for each result file and create `run.json`:

```json
{
  "schema_version": 1,
  "run_id": "v0-3-3-clean-example",
  "suite": "1C ERP Diagnostics Gate 0-10 acceptance",
  "plugin_version": "0.3.3",
  "source_commit": "0000000000000000000000000000000000000000",
  "executed_at": "2026-08-25T10:00:00+03:00",
  "environment": {
    "surface": "Codex desktop",
    "host": "clean test host identifier",
    "clean_session": true,
    "installed_plugin_version": "0.3.3",
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

## Priority re-test after 0.3.3 installation

Before running all 16 cases, validate these two exact rendered prompts in separate clean tasks:

1. `stale-execution-result` — must produce `R0`, `EVIDENCE_REQUIRED`, `linked_incident_status=blocked`, `Gate 5=stale`, `Gate 7=passed`, `Gate 10=blocked`, schema-valid claims, `causal_chain.complete=false` and `actions=[]`.
2. `provenance-closure-broken` — must preserve the derived observation but block final establishment without source/derivation closure, while using canonical Gate-procedure statuses.

Passing these two smoke tests does not equal complete runtime acceptance; it only confirms the reproduced v0.3.2 defect is closed before spending time on the full suite.

## Result interpretation

- `EVAL SUITE VALIDATION: PASS` — specifications and mandatory coverage are valid.
- `EVAL RESULT VALIDATION: PASS` — supplied result files satisfy their contracts.
- `RUNTIME ACCEPTANCE: PASS` — one complete, hashed clean-session run satisfies the strict release gate.
- `RUNTIME ACCEPTANCE: BLOCKED` — the plugin version must not be described as runtime-accepted.

Repository/publication integrity is separate: `python tools/validate_publication_history.py` proves archive/history hygiene, not model/runtime behavior. Both claims must remain distinct.
