# UI SDK integration and user scope

Reviewed source: [vercel-labs/ui](https://github.com/vercel-labs/ui) at commit `724a7d6c2d0ca1251a8eb6172462ae220c484714`, reviewed 2026-11-14. The repository uses Apache-2.0 and describes UI SDK as beta.

## What is installed

The upstream `ui-sdk` skill is a standalone user skill. Its entrypoint and seven references are installed at the user-scoped location `~/.agents/skills/ui-sdk`. All eight installed source files were checked against Git blob identities from the reviewed commit. It contains instructions and references, not a running frontend or server.

The user-facing installer command, with global Codex scope, is:

```text
npx skills add vercel-labs/ui --skill ui-sdk --global --agent codex --yes
```

The setup environment did not have `npx`, so the equivalent installation used the bundled Codex skill installer with the immutable commit, the source path `packages/core/skills/ui-sdk`, and the user skill directory as destination. This avoids installing an unrelated Node toolchain just to copy the requested skill.

Global installation makes the skill discoverable for this user's local projects and subsequent turns in local chats. It does not rewrite chat history, restart a running turn or deploy a skill into remote/cloud environments. Codex watches local skills; if the new entry does not appear after the next turn, refresh/restart the client. See [official local skill scope](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

Use `$ui-sdk` explicitly when building an interface, or let its task description select it. The installation does not install `@ui-sdk/core` or an adapter into every project. Add those dependencies only to the UI project that needs them, using its package manager and lockfile.

## How the 1C plugin uses it

The packaged `one-c-erp-ui-design` skill applies the SDK approach to requested diagnostic interfaces:

- choose existing accessible components and compose behaviors for missing components;
- keep UI state, styling and ERP evidence separate;
- name controls and expose deliberate browser-agent interactions;
- verify actual state/DOM, keyboard behavior, focus and agent actions;
- preserve evidence/run identities, exact diagnostic states and backend authorization;
- treat UI acceptance and accounting acceptance as different claims.

Ordinary diagnosis stays a diagnostic workflow. Native managed forms stay native 1C forms. The exact `EVAL_RESULT_JSON` contract has no added UI fields or inferred capabilities. No SDK implementation, upstream skill copy, hidden MCP backend, hosted UI, database connection or bridge installation is bundled into this plugin.

`createAgent` is a browser-side component API. WebMCP registration requires browser support and explicit task scope; neither becomes a Codex tool merely because a skill is installed. The 1C test bridge remains separate and deferred unless a later task requests it.

## Verification and limits

Installation verification compares all installed files against the pinned upstream tree. User-scope discovery is checked through Codex `skills/list` with `forceReload: true` in the repository and a separate unrelated working directory. That check creates no chat and runs no model.

Repository lint, package links and the deterministic lock cover the packaged 1C skill. The exact-version 26-case clean-session suite checks that UI routing does not alter the diagnostic contract. Separate planning smoke checks can assess the new UI instructions. This instruction-only change does not claim tests of a rendered application, real browser accessibility or live ERP accounting.

Rollback: uninstall the standalone skill through the chosen skill manager or remove that exact user skill directory after checking its identity; revert the plugin candidate separately. Do not remove unrelated user/project skills or alter existing project settings.
