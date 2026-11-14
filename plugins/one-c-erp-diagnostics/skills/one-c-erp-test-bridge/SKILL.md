---
name: one-c-erp-test-bridge
description: Capture and verify read-only HTTP evidence from an explicitly selected local 1C test contour, or plan external report and print-form validation through CodexTestBridge.
---

# Local test-contour evidence

## When to use

Use at Gate 0/5/9 when an identified, sanitized local test base already exposes CodexTestBridge. This is an optional host adapter named `codex-test-bridge-local`, not an installed marketplace companion. See the [contract and commands](references/bridge-contract.md).

## When NOT to use

Do not use for a production base, remote publication, artifact inspection that can be done offline, or an inferred/default database. Do not install CFE, change VRD/Apache, start a UI worker or run upstream scripts merely to discover availability. A loopback address alone does not make a base a test contour.

## Required inputs

Require the exact publication URL, explicit test-contour identification, expected metadata name, case and Evidence IDs, analytic key, approved query scope, and a fresh local output directory outside Git. Resolve credentials through a separately reviewed adapter if required; this adapter has no authentication options and never tries default credentials.

## The framework

`Health → assert expected configuration → allowlisted read → save raw request/response and hashes → offline integrity/context check → independent business reconciliation`.

The packaged [adapter](scripts/test_bridge.py) supports only `Health`, `Metadata`, `Describe` and `Query`. It rejects remote/DNS addresses, credentials in URLs, redirects, proxies, malformed JSON, oversized responses and writes. The selected query runs on the test server; its row limit does not limit server workload. A socket timeout does not cancel a server query. No automatic retry.

## Workflow

1. At Gate 0 verify the selected contour and authorization; run `capture health`. A matching configuration name is not a unique infobase identity. Record contour provenance separately.
2. Map status to `available` only for the observed read surface with a valid response; authentication or missing scope/permission is `confirmation_required`; a failed connection or missing service is `unavailable`; production/remote endpoint is `prohibited`. Missing credentials are never proof that the service is absent. Preserve the reason separately from the canonical status.
3. Read approved metadata before naming ERP objects. Use the narrowest read/query that can falsify the hypothesis. Risk is `R0` for reads from an authorized test contour; local evidence-file creation is `R1`. Installation, arbitrary BSL, object writes, posting, rendering and UI execution require their own reviewed scope and risk gate.
4. Run offline `verify` with the current case/Evidence IDs and analytic key. Link the capture directory, run ID, request/response hashes and timestamps into case state. Do not reuse old evidence as proof of the current base state.
5. Independently reconcile document/movement/register rows, periods, analytic dimensions and totals. Even a sample below the limit is not proof of population coverage. Health/metadata do not satisfy functional or business validation.
6. For reports/print forms read the reference's execution checklist. Rendering executes external code and is deliberately outside the read adapter.

## Failure patterns

- A JSON `ok: true`, HTTP 200, successful CFE build or returned output path is insufficient acceptance evidence.
- The protocol-reference commit records reviewed documentation, not the installed CFE revision. Health cannot attest that revision.
- Failures may leave an incomplete output directory; only a final manifest that passes verification is a valid capture. Keep it for inspection, select a new directory for a deliberate rerun.
- Hash verification detects damage, not malicious rewriting of both data and hashes. It proves neither server authenticity nor freshness.
- The reviewed upstream snapshot has no root license file; do not vendor its code or CFE into this MIT package. No marketplace entry or automatic installation is supplied.

## Output format

Report capability status/reason, contour identity source, operation, risk, input Evidence IDs, analytic key, run ID, hashes, row/limit observations, integrity status, current-state limitations, independent acceptance result and fallback. A test observation alone cannot establish production ERP causality; retain Gate 7 and the six-stage factual chain.

## Reference files

- [Bridge contract, CLI examples and rendering checks](references/bridge-contract.md).
- [Packaged read-only adapter and verifier](scripts/test_bridge.py).
