# Local diagnostic workbench

Version 0.5.0 adds a separate **Подключение и проверки** screen. The original file viewer still opens files entirely in browser memory, without starting a database connection. The workbench is opt-in:

```text
python plugins/one-c-erp-diagnostics/ui/serve_ui.py --workbench --open
```

No Node.js installation is needed to use the packaged build. The server binds to literal IPv4 loopback, chooses an available port, verifies bundled asset hashes and requires exact Host/Origin plus a random CSRF token for API writes. Close it with Ctrl+C. Closing the browser alone does not stop it.

## Connect and collect

1. Add a profile with a literal loopback bridge URL, expected metadata name and an explicit test-contour declaration. The server/base must already have been selected and authorized; no profile is selected automatically.
2. Sign in with an existing user of that test base. The password is cleared from the form after the attempt, is hidden from UI SDK snapshots and is kept only in server memory. The session expires automatically after 15 minutes, including while idle. Disconnect immediately removes it from the session registry; an already running request can finish. No browser storage, saved credentials or automatic retry is used.
3. Create/select a case. Health, metadata, a fixed connectivity probe and descriptions of observed metadata objects can be saved into it. A case is bound to its first selected contour; mixing contours is refused.
4. With VelisReadOnlyBridge, two explicitly supplied document UUIDs can be compared. This covers standard header fields only. It does not select a first document, read movements or compare tabular sections.
5. Save notes independently, open the collected case in the viewer, or export a JSON bundle, Markdown report or ZIP of verified sources. ZIP export uses an explicit file allowlist, verifies hashes and never walks unrelated private files.

By default profiles/cases are stored under the current user's local application-data directory `VelisDiagnostics`; `--data-dir` can select another private directory. Raw captures may contain confidential metadata or business rows: keep this directory and exports outside Git. JSON export is a viewer bundle containing canonical `state` and annotations. Notes are in the Markdown/ZIP exports, separate from evidence.

Only one running workbench can own a material directory. An OS file lock refuses a second process before it can change profiles or cases, preventing concurrent instances from overwriting evidence indexes. The lock releases on normal shutdown or process termination; its small `.workbench.lock` file stays in the directory and must not be deleted while a workbench is running. Use a different `--data-dir` for an independent workspace.

An existing credential-free profile can be imported with `--profile <selected.json> --test-contour`. Import does not sign in, publish a service or install an extension. `bridge_doctor.py --profile <selected.json>` tests unauthenticated endpoint behavior; optional `--apache-config`, `--vrd` and `--web-module` inspect explicitly supplied local files. A PASS is limited to the listed checks.

## Reproducible row checks

Choose one scenario and import JSON (maximum 4 MB, 1,000 rows per input). **Загрузить учебные строки** provides a clearly marked synthetic example of the selected contract:

- **Сравнение строк:** explicit `key_fields`, `value_fields`, `left`, `right`, optional `numeric_fields`. Duplicate analytic keys are refused. Missing/changed rows are reported; at most 2,000 differences are displayed with truncation stated.
- **Отрицательные остатки:** explicit analytic keys and quantity field. Only the supplied population is checked.
- **Распределение расходов:** delegates the packaged accounting-invariants validator; decimal amounts must be strings to preserve exact arithmetic. A balanced total alone does not prove the allocation is correct.

The input and derived result are saved separately with hashes and parent links. No scenario closes a Gate or establishes a business cause. Completeness, periods, movement chains and case-specific acceptance remain independent work.

Numeric checks accept decimal strings or integers, with magnitude up to `1e20` and exponent from -80 to 80. This bounds exact rational arithmetic before processing; binary floats, non-finite values and extreme exponents are refused. Allocation checks apply these limits to source and observed amounts as well as the allocation input.

## Boundaries

The browser calls only its own local API. No external model, CDN, analytics, automatic WebMCP registration, arbitrary query text, BSL execution, posting or database-write action is exposed by the workbench. Legacy CodexTestBridge can still have a wider server surface; the UI states that distinction and permits only fixed reads. The first-party bridge source and installation contract are in [bridge/README.md](../plugins/one-c-erp-diagnostics/bridge/README.md).

SDK confirmation markers and secret controls assist interface automation; backend checks remain authoritative. UI tests, offline scenario checks, live bridge reads and strict Codex acceptance are reported separately for each release candidate.
