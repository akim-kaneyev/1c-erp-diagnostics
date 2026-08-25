---
name: one-c-erp-companion-plugins
description: Safely coordinate the verified 1C companion ecosystem—Unica and 1C Skills—plus host-managed document, repository, UI and sandbox capabilities without fabricating availability or dependencies.
---

# Verified companion coordination

Use only after Gate 0 confirms actual installation, permissions and runtime availability.

## Canonical companion identities

The ecosystem marketplace exposes these independently maintained plugins:

- `unica` — Unica `0.12.0`, source `IngvarConsulting/unica-marketplace`, immutable ref `aefc880f9bab606a5c55ed11af563b740054a549` (release tag `v0.12.0`).
- `1c-skills` — 1C Skills PowerShell, source `Nikolay-Shirokov/cc-1c-skills`, immutable generated ref `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- `1c-skills-py` — 1C Skills Python, source `Nikolay-Shirokov/cc-1c-skills`, immutable generated ref `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

They are offered from one marketplace but remain separate plugins with their own licenses, permissions, updates and confirmation rules. Never claim that their implementation is embedded in `one-c-erp-diagnostics`.

## Typical roles

- **Unica (`unica`)** — metadata/BSL navigation, development workflows, controlled build/test operations and implementation review. A code finding is not an accounting root cause until linked to the exact document/movement/register chain.
- **1C Skills PowerShell (`1c-skills`)** — Windows-first XML/configurator/web-client tooling, MXL/СКД/form/report operations and controlled 1C automation. Default to read-only inspection; any base-changing operation is `R3` unless proven otherwise.
- **1C Skills Python (`1c-skills-py`)** — cross-platform XML/configuration artifact parsing, deterministic comparison and controlled automation.
- **PDF / Spreadsheets / Documents** — artifact extraction and structured comparison.
- **GitHub / Drive** — retrieval only when the user has identified the source and has access.
- **Computer Use** — observation or explicitly approved UI interaction; production-changing operations require the applicable risk gate.
- **OpenSandbox** — isolated executable validation when Gate 5 establishes value.
- **Local SonarQube (`sonarqube-bsl-local`)** — a separately installed host adapter for sanitized static BSL analysis. It is not a marketplace companion; coordinate it through `one-c-erp-local-static-analysis` only when Gate 0 confirms the actual loopback runtime.

## Dynamic selection

For each requested capability, record:

1. canonical plugin/tool name;
2. Gate 0 status: `available | confirmation_required | unavailable | prohibited`;
3. exact task assigned and evidence IDs;
4. read/write surface and `R0–R3` risk;
5. tool version/ref where available;
6. execution identity when the operation produces executable evidence: `run_id`, `case_id`, input evidence hashes/identifiers, timestamps when available, output location/hash;
7. limitations, errors and fallback;
8. whether another method independently reproduced the material result.

Never reuse a companion result merely because its filename, issue ID or report title matches. If its execution identity does not match the current case and current material inputs, classify it as stale until rerun or proven equivalent.

Use the smallest sufficient companion set. Prefer one primary specialist and no more than two secondary specialists unless the dependency graph proves additional value.

## Conflict handling

When companion outputs disagree:

- preserve both outputs and provenance;
- compare inputs, versions, run identities, scope and analytic keys;
- do not vote by majority;
- seek the earliest factual divergence in the case evidence;
- downgrade the conclusion until the contradiction is resolved.

## Boundary

External plugins and host adapters are invoked, not copied. Their runtime availability is host-managed. The marketplace entry makes the three canonical companion plugins discoverable from one source; it does not include SonarQube or bypass installation, permissions, authentication or action confirmation.

A missing companion triggers a documented fallback or `blocked`, never a simulated result.
