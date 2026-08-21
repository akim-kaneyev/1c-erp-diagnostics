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

Candidate companions may include Unica, 1C Skills (Python), 1C Skills (PowerShell), PDF, Spreadsheets, Documents, GitHub, Google Drive, Computer Use and OpenSandbox. Candidate host adapters may include `sonarqube-bsl-local`. This list is not proof that any candidate is installed.

For `sonarqube-bsl-local`, do not infer availability from marketplace presence and do not infer unavailability from the absence of a dedicated SonarQube tool. When local process execution and loopback HTTP are exposed, apply `one-c-erp-local-static-analysis` and perform its factual read-only endpoint/scanner preflight. `available` requires an `UP` loopback server, a working scanner, authenticated confirmation of the `communitybsl` plugin, `bsl` language, active quality profile, pre-created project and safe scoped authentication. A host permission block, missing token or stopped reviewed server is `confirmation_required`; a missing component after an actual probe is `unavailable`; unsanitized input or any non-loopback endpoint is `prohibited` for this capability. Preserve observed server/scanner facts across `401/403`, and keep a reason such as `host_execution_confirmation_required`, `authentication_required` or `compatibility_unverified` separate from the four canonical statuses.

Select the minimum sufficient capability set. Do not use a tool merely because it exists. If two capabilities overlap, prefer the one with lower write risk and clearer reproducibility.

Output a compact capability map and feed it into the dynamic plan.
