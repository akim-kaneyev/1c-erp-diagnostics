---
name: one-c-erp-ui-design
description: Build requested web interfaces for 1C diagnostic evidence with UI SDK, accessible behavior and agent-readable controls. Use for an explicit UI task; native 1C forms and ordinary diagnostic answers use their existing workflows.
---

# UI SDK for diagnostic interfaces

## When to use

Use when the user asks for a web interface, interactive evidence viewer, diagnostic dashboard or UI component for a 1C workflow. Coordinate through the primary diagnostic skill when the interface presents case conclusions. The globally installed `ui-sdk` skill supplies the SDK authoring workflow when available; this skill supplies the 1C evidence and permission boundaries.

## When NOT to use

Do not turn an ordinary diagnostic answer into an application. In strict `EVAL_RESULT_JSON` mode return the existing exact JSON contract; do not add HTML, UI fields or UI capabilities. Native managed 1C forms remain a Unica/form workflow. Selecting this skill alone does not authorize starting a server or deployment. Launch the packaged local viewer when the user requests it; database bridges and 1C changes remain separate scopes.

## Required inputs

Identify the requested user task, existing UI framework and package manager, input format, case/Evidence IDs, current run/source identity, data sensitivity and allowed actions. For real case data, keep source bytes local and use a sanitized slice. If no dataset is supplied, label demonstration data as synthetic.

## Ready local viewer

For viewing an existing case, use the packaged [viewer launcher](../../ui/serve_ui.py) or the [Windows launcher](../../ui/launch.ps1). Resolve its absolute path from this installed skill before running it; the repository checkout is not required. Run the Python launcher with `--open` to open the printed loopback URL, or omit that flag when a host browser tool will open it. The server verifies bundled asset hashes before listening and stops with Ctrl+C.

The viewer accepts the existing `STATE.json` or a version-1 viewer bundle with optional annotations. The [synthetic example](../../ui/dist/example.json) demonstrates the format. Ask the user to choose their local file in the viewer; never upload it or inspect unrelated cases. Preserve exact source bytes when saving a copy. Use the canonical case-state validator separately when validating diagnostic meaning: the viewer performs structural checks and preserves declared statuses. The browser UI agent is local component control, not a model/provider connection or a database tool.

The viewer provides evidence/claim/run tabs, search/status/date filters, bounded pagination, details, local source-file SHA-256 comparison and immutable JSON export. Native 1C forms continue through Unica. Do not install a database bridge for viewing files. Prefer this ready viewer over generating another application when it already meets the user's task.

## The framework

`user task → named controls → UI SDK components/behaviors → explicit state callbacks → agent-readable interaction → observable verification`.

Use existing components for keyboard navigation, focus, selection, dismissal and ARIA. Create a primitive from core behaviors only when the installed component catalog lacks the required behavior. Keep presentation styling separate from state and domain decisions. See the [diagnostic interface contract](references/diagnostic-interface.md).

## Workflow

1. Inspect the actual project. Read its installed UI SDK documentation index and only relevant component pages. Preserve its framework; install core and the matching adapter with its package manager only when implementing the requested UI. Record resolved versions in the project lockfile. UI SDK is beta; a reviewed source snapshot is not proof that another installed version has the same API.
2. If the `ui-sdk` skill is available, use it for the SDK details. Otherwise use the pinned [upstream entrypoint](https://github.com/vercel-labs/ui/blob/724a7d6c2d0ca1251a8eb6172462ae220c484714/packages/core/skills/ui-sdk/SKILL.md) and version-matched package docs. The ready viewer includes its bundled SDK runtime. It does not install authoring dependencies into other projects or include the upstream skill; global skill installation also does not supply JavaScript packages in a project.
3. Model UI state explicitly. Route changes through component change callbacks, including programmatic agent changes. Validate through the shared state path; pointer and key handlers alone cannot enforce a rule. Filters, sorting and selection must not change the canonical evidence or its verification status.
4. Name every control and preserve stable evidence/row identifiers. Use the SDK's documented parts and entrypoints, controlled values when the app owns state, and state attributes for styling. Verify keyboard reachability, focus recovery and the selected/disabled/invalid states actually rendered.
5. When agent interaction is part of the requested interface, use the documented framework `createAgent` entrypoint in browser code. Test snapshot labels and actions against visible results. Register WebMCP only when the browser exposes that capability and the task includes it; otherwise report it unavailable. SDK installation alone is not a host-visible MCP capability.
6. Default diagnostic interfaces to reading evidence. For an authorized action surface, mark confirmation/secret/hidden controls as documented and enforce the same policy in callbacks and the backend. UI flags and an SDK `allow` callback cannot replace the host's authorization, Gate 7, `R0–R3`, authentication or rollback controls. Never attach arbitrary BSL, posting, close-month or bridge-install commands to a viewer.
7. Typecheck the actual application target. Test the interactions the task needs through both human input and agent actions, including rejected changes, Cancel, disabled controls and focus return. Verify state/DOM and any backend effect, not just an `ok` response. Use a real browser for layout, focus and contrast. Keep UI acceptance separate from accounting acceptance.

## Failure patterns

- A polished screen, accessible snapshot or passing UI test is not evidence of correct ERP accounting.
- A filter returning fewer rows does not prove completeness; preserve total/returned counts, limit and scope limitations.
- The UI SDK browser agent bridge and the 1C HTTP test bridge are different capabilities. Do not start or publish either merely because this skill is selected.
- Loading code from a public CDN in a page that opens confidential case evidence introduces an external code dependency. Prefer locally bundled, lockfile-pinned packages for those interfaces; review any external data destination before use.
- An absent package or renderer triggers a documented implementation requirement or a plain report fallback; do not fabricate a running interface. The primary diagnosis can continue without UI SDK.

## Output format

Return the actual artifact/preview, framework and resolved SDK versions, implemented controls and allowed actions, evidence/run/source identities, commands with exit codes, observed human/agent checks, unchecked limitations and a local rollback path. Report UI behavior separately from any Gate 7/9 or business-accounting conclusion.

## Reference files

- [Diagnostic interface contract and acceptance scenarios](references/diagnostic-interface.md).
- [Reviewed upstream skill](https://github.com/vercel-labs/ui/blob/724a7d6c2d0ca1251a8eb6172462ae220c484714/packages/core/skills/ui-sdk/SKILL.md) and [Apache-2.0 license](https://github.com/vercel-labs/ui/blob/724a7d6c2d0ca1251a8eb6172462ae220c484714/LICENSE).

## Ready local workbench

When the user explicitly requests connections, capture or persistent case work, launch the installed `../../ui/serve_ui.py --workbench --open`. The original default remains the static file viewer. Use an explicitly selected test profile and existing sign-in; no automatic first base/document or credential persistence. The workbench provides private cases, separate notes, source packages and three deterministic row scenarios. It never promotes scenario output into a causal conclusion or closes Gates. The UI exposes no arbitrary BSL, query text or write commands. The first-party bridge has a fixed server contract; legacy bridge limitations remain visible. See the packaged [bridge contract](../../bridge/README.md); repository users can also read `docs/WORKBENCH.md`.
