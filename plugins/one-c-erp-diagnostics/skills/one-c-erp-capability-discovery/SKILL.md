---
name: one-c-erp-capability-discovery
description: Build a current-session capability map before selecting tools, skills, plugins or execution paths for a 1C:ERP case.
---

# Capability discovery

Use at Gate 0.

For every candidate capability record:

- exact host-visible name;
- category: evidence reader, 1C development, execution, source control, official source, browser/computer or communication;
- status: `available | confirmation_required | unavailable | prohibited`;
- read/write risk;
- case-specific purpose;
- provenance expected from its output;
- fallback and stop condition.

A capability is a host-visible external/plugin/tool surface. Internal reasoning steps, packaged skills, synthesis/review roles, or names invented to describe what the model can do are not capabilities and must not be emitted in a capability map.

Visual Explanation and its `diagram`/`sticky` modes are internal presentation concepts, not runtime capabilities. Never inventory them at Gate 0 or emit them in a synthetic capability snapshot. They require no image-generation capability and are governed only as optional normal-response presentation after Gate 6/7.

## Strict synthetic inventory output

In `EVAL_RESULT_JSON` cases, the synthetic case capability snapshot is authoritative. Report exactly the declared capability names/statuses in their supplied order and no additional inferred entries.

Every strict capability item is exactly:

`{name, status, simulated}`

`simulated` is always `false`. Do not add `evidence_id`, `evidence_ids`, category, purpose, reason, provenance, fallback or other fields to the strict result item. Reference the snapshot evidence only in the top-level `evidence_ids_used` array.

Capability rows are inventory data, not diagnostic claims. Do not create claims that merely restate `available`, `confirmation_required`, `unavailable` or `prohibited` statuses.

When the synthetic case declares no capabilities, return `capabilities: []`; Gate 0 may still pass after recording that no runtime capability is required for the read-only evidence assessment.

For the inventory-only `capability-inventory` acceptance case:

- `final_status = ТРЕБУЕТ ПРОВЕРКИ`;
- `risk = R0`, `decision = NO_ACTION`;
- `current_goal_status = closed`, `linked_incident_status = not_in_scope`;
- Gate 0 and Gate 10 are `passed`; Gates 1–9 are `not_required`;
- `claims = []`;
- `causal_chain.complete = false` with empty links;
- no requested evidence and no actions.

Successful inventory completion is represented by Gate 10/current-goal closure. It is not a proved 1C/root-cause conclusion and must not produce `final_status = УСТАНОВЛЕНО`.

Candidate companions may include Unica, 1C Skills (Python), 1C Skills (PowerShell), PDF, Spreadsheets, Documents, GitHub, Google Drive, Computer Use and OpenSandbox. Candidate host adapters may include `sonarqube-bsl-local`. This list is not proof that any candidate is installed.

For `sonarqube-bsl-local`, do not infer availability from marketplace presence and do not infer unavailability from the absence of a dedicated SonarQube tool. When local process execution and loopback HTTP are exposed, apply `one-c-erp-local-static-analysis` and perform its factual read-only endpoint/scanner preflight. `available` requires an `UP` loopback server, a working scanner, authenticated confirmation of the `communitybsl` plugin, `bsl` language, active quality profile, pre-created project and safe scoped authentication. A host permission block, missing token or stopped reviewed server is `confirmation_required`; a missing component after an actual probe is `unavailable`; unsanitized input or any non-loopback endpoint is `prohibited` for this capability. Preserve observed server/scanner facts across `401/403`, and keep a reason such as `host_execution_confirmation_required`, `authentication_required` or `compatibility_unverified` separate from the four canonical statuses.

Select the minimum sufficient capability set. Do not use a tool merely because it exists. If two capabilities overlap, prefer the one with lower write risk and clearer reproducibility.

Output a compact capability map and feed it into the dynamic plan.
