# Machine-readable case state

Create the persisted integrity surface from the [template bundled with this skill](../assets/STATE.json). Save the working copy in the case workspace. `STATE.md` remains the human investigation journal; material IDs and statuses in it must agree with the JSON state.

Validate before resuming a case and before Gate 10:

```text
python scripts/validate_case_state.py path/to/STATE.json
```

The validator returns exit code `0` only when the state is internally consistent. Exit code `1` means the state or its invalidation projection is inconsistent; argparse errors use `2`.

## Exact entity fields

- Evidence: `id`, `status`, `derived_from`, `run_id`, `artifact_hash`, `transformation`, `tool`, `tool_version`, `limitations`, `superseded_by`, `invalidates_ids`.
- Run: `id`, `case_id`, `status`, `input_evidence_ids`, `input_hashes`, `release`, `extension_set`, `period`, `tool`, `tool_version`, `operation`, `limitations`, `started_at`, `completed_at`, `superseded_by`, `invalidates_ids`.
- Claim: `id`, `status`, `evidence_ids`, `depends_on_claim_ids`, `document_ids`, `historical_document_ids`, `superseded_by`, `invalidates_ids`.
- Document/report: `id`, `status`, `claim_ids`, `superseded_by`, `invalidates_ids`.
- Gate: `id`, `status`, `claim_ids`.
- Active index: `run_id`, `claim_ids`, `document_ids`.

All Evidence, Run, Claim and Document/report IDs are globally unique. `superseded_by` points to the same entity kind. `invalidates_ids` may point to any ID-bearing entity and is normalized as a temporal replacement edge.

All eleven Gate IDs (`0` through `10`) are present exactly once. `artifact_hash` and each run `input_hashes` value are lowercase SHA-256 strings. Every run has at least one positional input pair, and each hash must equal the referenced Evidence `artifact_hash`; otherwise the run and its outputs are stale. A Run also requires non-empty tool, tool version/ref and operation identity, an explicit limitations list and at least one linked output Evidence with an artifact hash. Invalid/missing case, input, release, extension-set, period, tool, operation or timestamp identity invalidates the run. Run timestamps are timezone-aware ISO-8601 values with `completed_at >= started_at`; a superseding run cannot begin before its predecessor completes.

Evidence with `run_id` is output of that Run: its `derived_from` set must exactly equal the Run `input_evidence_ids` set. It records a non-empty transformation and inherits tool identity from the Run. Derived Evidence without a Run records its own non-empty transformation, tool and tool version/ref. Source Evidence uses null derivation-identity fields; every Evidence record carries an explicit limitations list. A Run cannot consume its own output Evidence. A duplicate/mismatched lineage, missing derivation identity or self-certifying Run invalidates the Run or Evidence before closure is propagated.

## Invalidation closure

The validator computes a fixed point across:

`stale/superseded/withdrawn evidence → dependent run → run output/derived evidence → claim → document/report → first affected Gate and downstream required Gates`.

Exactly one Run ID may remain `current`: `active_index.run_id`. Another Run ID is a different execution even when case, hashes, release, extensions and period happen to match. Mixed-run Evidence cannot support one current claim. Filename, order number or equal amount is not execution identity.

In a claim-bearing case, every material Claim status requires at least one known Evidence ID, and every passed downstream Gate 6–10 must cover all active material Claim IDs while referencing no inactive Claim. Empty Evidence, partial Gate coverage or stale-only/empty `claim_ids` cannot bypass invalidation closure. A persisted `stale` Gate invalidates every later required Gate. Claim→Document and Document→Claim links are both dependency edges, so omitting one direction cannot keep a current report alive after its Claim becomes stale. A `historical` document is valid only through `historical_document_ids`; `document_ids` and the active document index accept `current` documents only.

The validator does not silently rewrite input. It emits the invalidated IDs and fails while persisted entities remain `active`, `current`, material-claim status or `passed` instead of the required stale/historical lifecycle. A superseded or withdrawn document may be used only through `historical_document_ids`, never as a current source.

Credential-like content, including structured/escaped assignments and private-key markers, causes an immediate redacted `credential_exposure` failure. The value is never returned; remove/redact accessible copies, rotate the credential and run current-tree, full-history and actual-archive scans.
