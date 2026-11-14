# Diagnostic interface contract

Reviewed 2026-11-14 against `vercel-labs/ui` commit `724a7d6c2d0ca1251a8eb6172462ae220c484714`, Apache-2.0. This reference is an independently authored 1C workflow mapping. Upstream implementation and skill contents are not vendored. The installed `ui-sdk` skill is an independently installed user resource.

## Pick components by the task

| Diagnostic task | Candidate UI SDK component | Required observable behavior |
|---|---|---|
| Switch between Evidence, Claims and Runs | Tabs | Keyboard selection and the active panel agree |
| Filter by period, organization or state | Field with Input/Select/Date Picker | Named controls update one shared filter state; clearing restores the original dataset |
| Search evidence by stable ID | Combobox or Command | Choices come from the loaded evidence; missing IDs do not select an unrelated row |
| Inspect an Evidence or Run | Dialog or Drawer | A named detail view shows source/hash/scope; closing restores focus |
| Expand a provenance chain | Tree or Accordion | Keyboard navigation and expanded state work without changing lineage |
| Compare before/after | Tabs or a component-supported view | Both sides preserve the same analytic keys and cutoff; missing coverage remains visible |
| Request an already authorized external action | Button and Alert Dialog | Cancel has no domain effect; confirmation still requires backend policy |

These are candidate components, not promised exports. Read the installed adapter's component pages before choosing import names or parts. Use semantic native tables for tabular evidence unless the installed SDK supplies the required table behavior. Do not invent a data-grid component or recreate a supplied composite with ad-hoc ARIA roles.

## State and evidence

Keep source evidence immutable and view state separate: selected Evidence ID, filter values, ordering and open details belong to the interface. An empty filtered list means no matches in that view; it does not mean the base has no records.

The view must preserve:

- case, Evidence, Claim and Run IDs, parent/derived links and source hashes;
- period, organization and other analytic keys actually present in the input;
- retrieval/run timestamps, source version and completeness/limit information;
- exact Gate states `pending | passed | blocked | failed | stale | not_required`;
- exact Claim statuses `УСТАНОВЛЕНО | ВЕРОЯТНО | ТРЕБУЕТ ПРОВЕРКИ`;
- current-goal status separately from linked-incident status.

Use text as well as color for statuses. Do not infer missing fields, silently normalize an invalid status to `passed`, or promote a hypothesis when someone clicks a card. A view may display an existing verified claim; it cannot create verification merely by rendering it.

## Agent-ready interaction

Follow the upstream skill's agent-ready and testing references for version-matched details. At the reviewed revision:

- `createAgent` comes from the framework's `/agent` entrypoint and belongs in browser code. It exposes UI snapshot/query/action operations, not 1C access.
- Label controls with the SDK's label/title parts or an accessible name. Include the task's actual controls in the agent test so an invisible plain input does not silently escape coverage.
- Agent actions may call component APIs without pointer/key handlers. Validate through the same change callback; check the rendered value after an attempted change.
- `data-agent-confirm`, `data-agent-secret` and `data-agent-hidden` express UI intent. They do not secure the backend or authorize transmission of case data. A client secret marker is not redaction of a server log or export.
- `registerTools` depends on `document.modelContext`; it is not a Codex MCP installation. Keep model/provider configuration and data-transfer consent separate from local component behavior.

For a read-only evidence viewer, expose only viewing/filtering/selection actions. Approval buttons for real database operations are outside that viewer's scope. If a later task authorizes them, the backend must independently check the exact target, scope, risk gate and confirmation; a changed client flag must not enable them.

## Acceptance scenarios

Use the applicable scenarios when implementing a real interface. These are design/verification criteria, not evidence that a UI has already been built or tested.

1. **Read-only evidence viewer.** Load a sanitized fixture with two Evidence IDs and one stale Run. Find the period/status filters by accessible name; change them using real keyboard input and the UI agent API. Both paths must produce the same visible rows. Clearing filters restores the original IDs. The stale Run remains stale throughout.
2. **Detail dialog.** Open one Evidence by its actual loaded ID. Check the displayed source/hash/limitations, close with Escape and Cancel, and verify focus returns to its trigger. Repeat via the agent action path.
3. **Rejected change.** Attempt a disallowed filter value or disabled action through the agent API. Assert that the callback/backend rejects it and that the observed value/domain state did not change. `ok: true` alone cannot pass this test.
4. **Completeness.** Present an explicitly truncated dataset and an empty filtered view. Both must retain the original coverage warning; neither may claim the entire base is empty or fully covered.
5. **No UI request.** An ordinary 1C incident with no interface requirement continues through Gate 0–10 and the normal report. No JavaScript package install, server, generated app or UI capability is introduced.
6. **Strict JSON.** A synthetic `EVAL_RESULT_JSON` request returns only the original exact JSON schema. UI definitions, preview URLs and SDK availability do not appear in its capability array unless the supplied snapshot explicitly declares a real external capability.
7. **Native 1C form.** A managed `Form.xml` task uses native 1C form tooling. React/Web Components are not inserted into the configuration.

Record real command exit codes and observed values when these scenarios are executed. If only a plan was requested, report a plan and do not invent screenshots, browser tests, agent snapshots or deployed URLs.
