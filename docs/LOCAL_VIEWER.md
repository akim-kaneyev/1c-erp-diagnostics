# Local diagnostic viewer

Version 0.4.0 includes a ready React/Vite interface built with `@ui-sdk/core` and `@ui-sdk/react` 0.1.0-beta.1. The installed plugin includes the production build, local server, synthetic example, dependency licenses and build identity. Node.js and a package manager are needed only to develop/rebuild it.

## Open it

Ask the primary plugin: **«Открой локальный веб-интерфейс материалов диагностики»**. It resolves the launcher inside its installed package and opens the printed loopback URL. No repository checkout or 1C bridge is needed.

From a source checkout:

```text
python plugins/one-c-erp-diagnostics/ui/serve_ui.py --open
```

On Windows the installed package also contains [launch.ps1](../plugins/one-c-erp-diagnostics/ui/launch.ps1). Run it in PowerShell or use the Python command. The server binds only to `127.0.0.1`, chooses an available port, verifies every bundled asset hash before starting, and stops with Ctrl+C. It serves static application files; it has no upload, case-storage or database endpoint. Close the server when finished; closing the browser alone does not stop it.

## Work with a case

Choose **Открыть JSON** and select the existing [STATE.json](../templates/case/STATE.json) of a sanitized case. This opens its evidence, claims, runs, exact statuses, source hashes and Gate 0–10 state. The page performs structural/reference checks; it does not replace the canonical case-state validator or independently accept the accounting conclusion.

For descriptive labels, open a viewer bundle with `viewer_schema_version: 1`, the complete original object in `state`, and optional `annotations`. The [complete synthetic example](../plugins/one-c-erp-diagnostics/ui/dist/example.json) shows the format. Annotations can supply `title`, `goal`, a `synthetic` flag, per-ID `records` with `title`, `description`, `source`, ISO `date`, and `coverage` with a nullable `total` and explicit `limitation`. They do not replace the original state or change statuses.

Search by ID/text/source, filter by exact status and date, or switch sections. Date filtering uses the date written in the file without timezone conversion; undated records are excluded by active date filters and counted explicitly. Status filters reset when the section changes. Results are paged by 25; all loaded records remain searchable. An empty view means no matches in the selected file/view. Coverage warnings and stale-record counts remain visible.

Open a record to inspect lineage, limitations and its original JSON. **Сверить файл** reads a user-selected source locally, computes SHA-256 and compares it with the declared hash. Matching bytes do not establish ERP causality or change a record status. Text preview is bounded to 12 KB. **Сохранить копию JSON** downloads the exact original bytes, including records excluded by filters. No edits are persisted; reloading the page clears the open case. Import limit: 10 MB / 5,000 records per category. Source hash check limit: 64 MB.

## UI agent and data boundary

The browser exposes `window.diagnosticsAgent`, created from the version-matched React `/agent` entrypoint. It offers the SDK's local snapshot/query/action API for named components. Inputs and filters share the same change callbacks for people and agents; invalid ranges are refused and disabled actions remain disabled. This is not a model-provider connection, host-visible MCP installation or 1C capability. WebMCP tools are not registered automatically.

The production application loads its code/styles locally, uses no CDN, analytics, remote model, browser storage or background data transmission, and keeps loaded files only in page memory. Native 1C forms and database changes remain separate workflows. The 1C bridge is not installed or started.

## Development and checks

Use Node.js 24 and pnpm 11.25.0. Dependencies and integrity hashes are committed in `web/pnpm-lock.yaml`.

```text
cd web
pnpm install --frozen-lockfile
pnpm test
pnpm build
```

The build typechecks the actual application, emits the installable assets and includes all runtime dependency license texts. `build.json` records source/dependency identities and SHA-256 for served assets. CI rebuilds on Linux and requires the committed bundle to match. The Python regression suite checks the actual packaged server and native synthetic case. Browser checks cover real popups/focus, filtering, responsive layout and color; those outcomes are recorded on the release PR alongside exact-installed Codex acceptance. UI tests do not establish live 1C/accounting correctness.

Rollback is reverting/updating the plugin through Codex and stopping the owned viewer process. It requires no database rollback: the viewer has no database write surface.
