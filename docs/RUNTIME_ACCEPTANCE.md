# Clean-session runtime acceptance

Static validation proves that the package and evaluation contract are internally consistent. It does not prove that a particular plugin/model/runtime combination follows the contract. Publication readiness therefore requires a separate complete clean-session run.

## Release gate

A runtime run passes only when all conditions are true:

1. the exact candidate plugin version is installed;
2. every case from `evals/suite.json` is executed in a clean session;
3. the runner sees the exact prompt rendered by `tools/validate_evals.py`, including the strict output instructions, deterministic capability block and skeleton, but not the case `expect` block;
4. every response is exactly one JSON object and is saved as one `*.result.json` file;
5. every result passes the exact field/type/status/scope/capability/semantic checks in `tools/validate_evals.py`;
6. `run.json` identifies the source commit, host, surface, installed version and timestamp;
7. every result hash matches and every case-specific/global control passes;
8. no case is missing, duplicated or unreferenced.

The suite exercises provenance closure and execution-identity freshness. A prior tool result for different material inputs must not be accepted as current evidence.

Version 0.3.3 made strict JSON conformance runtime behavior rather than formatting polish. Version 0.3.4 made the synthetic capability snapshot and scoped current-goal/linked-incident closure deterministic. Version 0.3.5 additionally separates capability inventory from diagnostic proof and enforces the exact capability item shape, Gate 10 closure and final-status cross-field invariants.

A semantically plausible response still fails when it invents internal reasoning/skills as capabilities, omits or changes a declared capability, replaces `simulated` with `evidence_id`, promotes capability rows into claims, closes a goal without Gate 10 passed, or returns `УСТАНОВЛЕНО` without Gate 7/Gate 10/complete causality.

Version 0.3.6 fixes the subsequently reproduced stale-execution output: Gate 5 must be `stale`, Gate 7 `passed`, Gate 10 `blocked`, the linked incident remains blocked, and claim/link/request/action arrays must use the exact schema.

Version 0.3.7 fixes the next clean-session failure in `under-evidenced-cost`: Gate 2 passes after all supplied evidence is accounted for, Gate 4 and Gate 10 remain blocked, Gate 7 passes by rejecting an unsupported cause, and claim/request/action collections use the exact schema.

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
  "run_id": "v0-3-7-clean-example",
  "suite": "1C ERP Diagnostics Gate 0-10 acceptance",
  "plugin_version": "0.3.7",
  "source_commit": "0000000000000000000000000000000000000000",
  "executed_at": "2026-08-26T10:00:00+03:00",
  "environment": {
    "surface": "Codex desktop",
    "host": "clean test host identifier",
    "clean_session": true,
    "installed_plugin_version": "0.3.7",
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

## Priority re-test after 0.3.7 installation

Before running all 16 cases, validate these three exact rendered prompts in separate clean tasks.

### 1. `capability-inventory`

Required result:

- `final_status=ТРЕБУЕТ ПРОВЕРКИ`;
- `risk=R0`, `decision=NO_ACTION`;
- `current_goal_status=closed`, `linked_incident_status=not_in_scope`;
- Gate 0 and Gate 10 `passed`; Gates 1–9 `not_required`;
- four capabilities in supplied order, each exactly `{name,status,simulated:false}`;
- `E-CAP-1` only in `evidence_ids_used`, never as a capability field;
- `claims=[]`;
- `causal_chain.complete=false`, links empty;
- `requested_evidence=[]`, `actions=[]`.

### 2. `stale-execution-result`

Required result:

- `risk=R0`;
- `decision=EVIDENCE_REQUIRED`;
- `current_goal_status=blocked`;
- `linked_incident_status=blocked`;
- Gate 5 `stale`, Gate 7 `passed`, Gate 10 `blocked`;
- exact schema-valid claims;
- `capabilities=[]`;
- `causal_chain.complete=false`;
- `actions=[]`.

### 3. `provenance-closure-broken`

Required result:

- `risk=R0`, `decision=EVIDENCE_REQUIRED`;
- `current_goal_status=closed` because the evidence-sufficiency assessment completed;
- `linked_incident_status=blocked` because source content/causality remain unresolved and were not excluded;
- Gate 2/6/7/8/10 `passed`;
- exact synthetic capability snapshot `capabilities=[]`;
- at most one `УСТАНОВЛЕНО` claim, limited to the directly evidenced missing-lineage fact;
- source-content/derivation/root-cause claims below established;
- `causal_chain.complete=false`;
- `actions=[]`.

### 4. `under-evidenced-cost`

Required result:

- `final_status=ТРЕБУЕТ ПРОВЕРКИ`, `risk=R0`, `decision=EVIDENCE_REQUIRED`;
- current goal and linked incident `blocked`;
- Gates 0–3 `passed`, Gate 4 `blocked`, Gate 5 `not_required`, Gates 6–8 `passed`, Gate 9 `not_required`, Gate 10 `blocked`;
- Gate 2 `passed` because the supplied symptom statement is fully accounted for;
- exactly one non-established exact-schema claim using `E-COST-1`;
- incomplete empty causal chain;
- string-only minimal requested evidence and `actions=[]`.

Passing these four priority tests does not equal complete runtime acceptance. It only
confirms that the reproduced strict-contract defects are closed before spending time
on the full suite.

## Result interpretation

- `EVAL SUITE VALIDATION: PASS` — specifications and mandatory coverage are valid.
- `EVAL RESULT VALIDATION: PASS` — supplied result files satisfy their contracts.
- `RUNTIME ACCEPTANCE: PASS` — one complete, hashed clean-session run satisfies the strict release gate.
- `RUNTIME ACCEPTANCE: BLOCKED` — the plugin version must not be described as runtime-accepted.

Repository/publication integrity is separate: `python tools/validate_publication_history.py` proves archive/history hygiene, not model/runtime behavior. Both claims must remain distinct.
