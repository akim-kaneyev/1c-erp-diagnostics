---
name: one-c-erp-local-static-analysis
description: Discover, run and capture provenance from local SonarQube BSL analysis without exposing credentials or treating static findings as ERP causality.
---

# Local BSL static analysis

Use this skill through Gate 0 and Gate 5 under the capability name `sonarqube-bsl-local`. SonarQube is an optional host execution adapter, not a marketplace plugin or hidden dependency.

## Gate 0 — read-only discovery

Default to the loopback endpoint `http://127.0.0.1:9000`. Record the explicitly selected endpoint and verify:

1. `/api/system/status` reports `UP`;
2. `/api/server/version` returns the exact server build;
3. the scanner executable returns its exact version;
4. authenticated API discovery confirms plugin key `communitybsl`, language key `bsl`, an active BSL quality profile and the pre-created project key;
5. `/api/webservices/list` confirms the endpoint contract exposed by that server version;
6. authentication can use scoped tokens without exposing their values.

The reviewed local baseline is SonarQube Community Build `26.8.0.126808`, SonarScanner CLI `8.0.1.6346` and `communitybsl` `1.20.0` with JAR SHA-256 `595F741AFD49BC7F1869B3F82F623821D519CECB399C56F154E55EA83DC7057B`. A different version is `compatibility_unverified`, not silently equivalent.

Map the result to the canonical capability status:

- `available` — loopback server is `UP`, scanner works, BSL plugin/language/profile/project are confirmed and scoped authentication is ready;
- `confirmation_required` — the reviewed components exist but the server must be started, a scoped token must be created/provided, or version compatibility must be reviewed;
- `unavailable` — a required component, BSL language/profile or source format is absent;
- `prohibited` — source is not sanitized, the endpoint is not loopback, or safe authentication cannot be used. `sonarqube-bsl-local` never changes to `available` for a remote endpoint.

Keep the canonical status separate from a machine-readable reason such as `authentication_required`, `compatibility_unverified`, `sonarqube_unavailable`, `bsl_analyzer_unavailable` or `remote_out_of_scope`. Never emit a reason code as a fifth capability status.

Do not start the server automatically, try default credentials, reuse a browser cookie, create a project, generate a token or change a quality profile during discovery.

## Risk boundary

- Reading an existing, identified analysis from the approved loopback instance is `R0`.
- Scanning a sanitized BSL tree into the pre-created loopback project is `R1`: it creates local derived files and persistent analysis state.
- Creating/deleting a local project or token, or changing a quality profile, is `R2` and requires separate confirmation plus rollback.
- Sending source to a remote SonarQube instance or writing to an external instance would be `R3`, but is outside this local capability. It requires a separately reviewed workflow, exact approval, approved data scope, HTTPS with certificate validation and a rollback/retention plan. Reading an already existing remote report may be `R0` only through a separately approved read capability; it does not make `sonarqube-bsl-local` available.

Only run a new scan when the current goal explicitly authorizes executable validation. Static analysis never authorizes code edits, Git writes or 1C changes.

## Authentication controls

- Use a project analysis token restricted to the selected project for the scanner.
- Use a separate least-privilege user token with `Browse Project` for API evidence retrieval; grant source visibility only when the case requires it.
- Give the scanner token only through the child process environment named `SONAR_TOKEN`; use `SONAR_HOST_URL` for the endpoint.
- Send API tokens only in the `Authorization: Bearer` header. Normalize origin as scheme, host and effective port; reject userinfo, build API URLs from the configured base URL and disable redirects for every authenticated request.
- Never place a token in command arguments, `sonar-project.properties`, `.env`, `STATE.md`, case artifacts, logs, Git or chat. Do not use the deprecated `sonar.login` credential path.
- Do not enable debug/trace or verbose scanner logging by default. Clear child-process credentials after the operation and record only token type/scope and expiration metadata.

## Safe scan contract

Resolve one approved source root and accept only `.bsl` and `.os` files inside it. A CF/CFE/EPF must first be safely extracted; do not pass the binary artifact to SonarQube. Reject external symlink/reparse targets and pseudonymize the project key.

Allow only the required non-secret scanner properties:

- validated `sonar.projectKey` for an existing project;
- resolved `sonar.projectBaseDir`, relative `sonar.sources` and `sonar.inclusions` limited to `**/*.bsl,**/*.os`;
- `sonar.sourceEncoding=UTF-8` and `sonar.bsl.languageserver.enabled=true`;
- an adapter-owned unique `sonar.working.directory` and `sonar.scanner.metadataFilePath`;
- a run ID in `sonar.buildString`;
- `sonar.qualitygate.wait=true` and an explicit bounded `sonar.qualitygate.timeout` value.

The scanner removes its working directory before analysis. Use a dedicated empty leaf beneath a newly created adapter-owned temporary root. Immediately before invocation and cleanup, resolve the root/leaf again, reject reparse/symlink targets and prove leaf containment. Never accept an arbitrary user/project directory.

SonarScanner has no generic “disable project auto-creation” switch. Enforce the boundary procedurally: authenticated preflight must confirm the exact existing project key, the scanner must use only a project analysis token for that key, and the operation must abort before invocation on any missing/mismatched project. Run without shell interpolation.

## Evidence capture

After execution:

1. preserve `report-task.txt` even when the scanner exits non-zero; accept its URLs only after normalized same-origin validation;
2. resolve `ceTaskId` through `/api/ce/task` and record each state until `SUCCESS`, `FAILED` or `CANCELED`, or until the bounded timeout;
3. require CE `SUCCESS` plus a non-empty `analysisId` before calling the quality-gate API; CE `FAILED`/`CANCELED` is an unsuccessful analysis, while timeout is `submitted`/incomplete and must not trigger an automatic retry;
4. retrieve the quality-gate result by `analysisId`; a Quality Gate `ERROR` can coexist with CE `SUCCESS` and a non-zero scanner exit, so preserve all three statuses independently;
5. retrieve BSL issues with the fixed query `componentKeys=<projectKey>&languages=bsl&p=<n>&ps=<bounded-size>`, plus the selected measures and project-analysis metadata;
6. record the exact query, page number/size, returned count and `total` for every page; deduplicate by issue key and set `complete=true` only when the stable total equals the unique collected count and the server-advertised result window was not exceeded;
7. set `complete=false` on an HTTP error, repeated/missing page, changing `total`, duplicate conflict, timeout or result-window limit;
8. hash the sanitized exports and source manifest.

Record at minimum: run/timestamp; server, scanner and BSL plugin versions; plugin JAR identity; quality-profile identity; project key; source scope/commit/dirty state/manifest hash; inclusions/exclusions; redacted command properties; CE task and analysis IDs/dates; build string; quality-gate conditions; API endpoints, retrieval times, pages read, completeness; artifact paths and hashes; errors and limitations.

For every issue preserve its issue/rule key, message, relative path, line/range, status, effort and dates. Keep MQR impacts separate from Standard Experience type/severity. Do not retain absolute local paths or source text by default. Current issues/measures are a retrieval-time view, so never present them as an immutable analysis snapshot without the recorded IDs, date and source commit.

## Interpretation and fallback

Phrase a finding as: “the analyzer reported rule X at file/line Y.” Its functional impact is a hypothesis until the executed path and the factual `document → movement → register/record → mechanism → result → symptom` chain are proven. A clean quality gate does not prove accounting correctness; a disappeared issue does not replace Gate 9. Gate 7 must challenge every material code conclusion.

Fallbacks:

- server unavailable — use status `unavailable`, reason `sonarqube_unavailable`; do not auto-start it;
- `401/403` — use status `confirmation_required`, reason `authentication_required`; do not try standard passwords;
- missing BSL plugin/language/profile — use status `unavailable`, reason `bsl_analyzer_unavailable`;
- version mismatch — use status `confirmation_required`, reason `compatibility_unverified`;
- no extracted `.bsl`/`.os` — route through artifact extraction;
- API drift — inspect `/api/webservices/list`, then fall back to `report-task.txt` without scraping HTML;
- analysis unavailable — use a reviewed BSL Language Server report or manual code review and keep the limitation visible.
