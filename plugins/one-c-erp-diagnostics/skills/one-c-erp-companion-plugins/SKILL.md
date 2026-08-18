---
name: one-c-erp-companion-plugins
description: Safely coordinate the verified 1C companion ecosystem—Unica and 1C Skills—plus host-managed document, repository, UI and sandbox capabilities without fabricating availability or dependencies.
---

# Verified companion coordination

Use only after Gate 0 confirms actual installation, permissions and runtime availability.

## Canonical companion identities

The ecosystem marketplace exposes these independently maintained plugins:

- `unica` — Unica `0.12.0`, source `IngvarConsulting/unica-marketplace`, ref `v0.12.0`.
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

## Dynamic selection

For each requested capability, record:

1. canonical plugin/tool name;
2. Gate 0 status: `available | confirmation_required | unavailable | prohibited`;
3. exact task assigned and evidence IDs;
4. read/write surface and `R0–R3` risk;
5. output location/hash and tool version where available;
6. limitations, errors and fallback;
7. whether another method independently reproduced the material result.

Use the smallest sufficient companion set. Prefer one primary specialist and no more than two secondary specialists unless the dependency graph proves additional value.

## Conflict handling

When companion outputs disagree:

- preserve both outputs and provenance;
- compare inputs, versions, scope and analytic keys;
- do not vote by majority;
- seek the earliest factual divergence in the case evidence;
- downgrade the conclusion until the contradiction is resolved.

## Boundary

External plugins are invoked, not copied. Their runtime availability is host-managed. The marketplace entry makes them discoverable from one source; it does not bypass installation, permissions, authentication or action confirmation.

A missing companion triggers a documented fallback or `blocked`, never a simulated result.
