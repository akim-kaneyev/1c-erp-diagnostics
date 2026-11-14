# Reviewed open-source integrations

Review date: 2026-10-05.

This project uses open-source components only through an explicit intake process. Discovery catalogs such as OpenYellow, `Untru/1c-mcp`, the Infostart technology map and `Oxotka/StackTechnologies1C` are not treated as security, quality or compatibility certification.

## OpenAI define-goal

Source: `https://github.com/openai/skills/tree/main/skills/.curated/define-goal`

Use: measurable goal-contract quality bar at Gate 1. It is a methodology reference, not a runtime dependency.

## OpenSandbox

Source: `https://github.com/opensandbox-group/OpenSandbox`

License: Apache-2.0.

Reviewed Python package pin: `opensandbox==0.1.14`.

Use: optional isolated execution for sanitized scripts, parsers and reproducible validation. It is not a source of 1C knowledge. Network egress and credentials must be controlled. Repository CI verifies the SDK import and exact package pin, but does not create a remote sandbox or require sandbox credentials.

## v8unpack

Source: `https://github.com/saby-integration/v8unpack`

Reviewed Python package pin: `v8unpack==1.2.6` (MIT).

Use: read-only extraction of sanitized CF/CFE/EPF into BSL/JSON. Rebuild mode is excluded from the diagnostic workflow. Successful extraction does not prove that the code caused an accounting incident. CI verifies the package version and `extract` API.

## BSL Language Server

Source: `https://github.com/1c-syntax/bsl-language-server`

Use: optional fallback static BSL analysis after extraction when the reviewed SonarQube adapter is unavailable or unnecessary. Record the exact release and command used for each case. Diagnostics are hypotheses until connected to the factual document/movement/register chain. MCP mode is not a mandatory dependency.

## SonarQube Community Build and BSL plugin

Official sources:

- SonarQube Community Build: `https://github.com/SonarSource/sonarqube` (GNU LGPL v3); official Web API/scanner documentation under `https://docs.sonarsource.com/sonarqube-community-build/`.
- SonarScanner CLI: `https://github.com/SonarSource/sonar-scanner-cli` (GNU LGPL v3).
- 1C (BSL) Community Plugin: `https://github.com/1c-syntax/sonar-bsl-plugin-community` (GNU LGPL v3), official release `v1.20.0`.

Reviewed local pilot baseline:

- SonarQube Community Build `26.8.0.126808`;
- SonarScanner CLI `8.0.1.6346`;
- plugin key `communitybsl`, language key `bsl`, version `1.20.0`;
- plugin JAR SHA-256 `595F741AFD49BC7F1869B3F82F623821D519CECB399C56F154E55EA83DC7057B`.

Use: optional loopback-only static analysis of sanitized extracted `.bsl`/`.os` sources. The plugin does not bundle or start this toolchain. Gate 0 records actual runtime versions and requires compatibility review when they differ from the baseline. Scanner credentials exist only in the child process environment; API retrieval uses a separate least-privilege token. Because the scanner has no generic auto-create switch, preflight must prove the exact existing project and matching project analysis token or abort before invocation.

Risk and proof boundary: reading an identified report is `R0`; a sanitized loopback scan is `R1`; project/token/profile administration is `R2`; source upload to a remote endpoint is `R3` with separate approval and HTTPS. A rule finding proves only that the analyzer reported it for a source snapshot. ERP causality still requires runtime and document/movement/register evidence plus Gate 7. Fallback: reviewed BSL Language Server or manual code review.

## Unica

Canonical marketplace source: `https://github.com/IngvarConsulting/unica-marketplace.git`

Reviewed release tag: `v0.12.3`.

Immutable marketplace ref: `c02e38d44a7dc238310172b9d790487f81aa4fb4`.

Plugin path: `plugins/unica`.

Manifest version: `0.12.3`.

License: LGPL-3.0-or-later.

Use: optional 1C developer workflows, metadata/BSL investigation and controlled build/test operations. Unica remains an independently installed plugin; this project does not copy or relicense it.

Compatibility review: releases 0.12.1–0.12.3 restore the typed execution surface, correct runtime/Windows behavior and reduce cold-install overhead. The marketplace path and independent-installation boundary remain unchanged. Repository tests validate the new immutable source pin; actual host installation and clean-session capability execution remain external acceptance checks.

## 1C Skills

Canonical source: `https://github.com/Nikolay-Shirokov/cc-1c-skills.git`

License: MIT.

Reviewed immutable generated refs:

- PowerShell plugin `1c-skills`: `8cb7868145281d8e353831512cc1ffa72f1b5c89` (generated from upstream source commit `113dc9e9280b33b7aa3e4691eb8915cdaddea65b`).
- Python plugin `1c-skills-py`: `c1f79f5ac9f31c620b8508f75464f8c42c559ae4` (generated from the same upstream source commit).

Use: optional 1C artifact/configurator/web-client tooling. The PowerShell variant is Windows-first; the Python variant is cross-platform. Both remain independently installed plugins and retain their own permissions and release lifecycle.

## Jev browser use

Canonical source: `https://github.com/wy-coliney/jev-browser-use.git`

Reviewed immutable commit: `cf7e76607d4ec70592b24becadd0296dcda8177a`.

Manifest version: `0.1.0`.

License: MIT.

Use: optional mechanical browser action planning for authorized, repetitive UI navigation. The reviewed skill restricts Jev to navigation, click/toggle/scroll and safe key actions; Codex remains responsible for goal selection, text input, semantic reasoning and visual verification. It requires Node.js 22+, a Codex CUA browser capability and a separately configured external model provider. Page accessibility data, the goal and action history may leave the host for that provider. It is never required for the fixed-origin Infoblog metadata bridge, and its output does not prove success or 1C causality.

The upstream repository has no reviewed release tag. The exact commit pin, explicit installation, origin allowlist, provider consent and post-action verification are mandatory controls. The upstream 20-test suite passed locally without making a paid provider call; live provider/browser compatibility still requires host-side confirmation.

## Infoblog public incident index

Source site: `https://infoblog.mywebguide.ru/`.

Observed fixed index: `https://infoblog.mywebguide.ru/data/search.json`.

Use: metadata-only discovery of practical incident leads. The site frontend loads a compact public JSON index and performs an all-words title search in the browser. The packaged bridge reproduces that search locally, so the query is not sent to the site. It records URL, retrieval time, ETag, Last-Modified and SHA-256; it rejects redirects, oversized/non-JSON/malformed responses and silent stale fallback.

The public index is not treated as a supported API, an official 1C source or a licensed content corpus. Article bodies are not vendored. Titles and links are non-authoritative leads that must be checked against the selected page, official sources and primary case evidence. An explicit offline cache is marked `stale_unverified`.

## Unified marketplace

`.agents/plugins/marketplace.json` exposes `one-c-erp-diagnostics`, Unica, both 1C Skills variants and optional Jev from one source. This is a discovery/installation bundle, not code vendoring and not a permission bypass. All external entries use immutable commit refs. See `docs/ECOSYSTEM_MARKETPLACE.md`.

## 1C ecosystem discovery catalog

Reviewed catalog snapshot: `https://github.com/Untru/1c-mcp` at commit `24a4526d615ca2c531264145553d5e0d28f6e7ce`.

The catalog is used to identify candidates by scenario. It is not bundled wholesale. Current priority queue:

1. **Read-only platform help/context** — evaluate `mcp-bsl-platform-context` or `onec-help-mcp` for current platform API lookup.
2. **Static BSL validation** — maintain the adopted local SonarQube adapter and evaluate BSL Language Server/manual fallbacks with deterministic reports.
3. **Isolated test/build loops** — evaluate `v8-runner` and `mcp-onec-test-runner` only in disposable test contours.
4. **Live information-base access** — prohibited by default for the public plugin; requires a separate threat model, authentication design, minimal tool surface, audit logging and explicit `R3` approval.

## Infostart and StackTechnologies1C discovery map

Reviewed sources:

- Infostart article `https://infostart.ru/1c/articles/2772307/`, `Современный инструментарий 1Сника`, published `2026-08-25`;
- `https://github.com/Oxotka/StackTechnologies1C` at commit `82a7b4c16f0dab0264ddd664b741019ce60aba81`, MIT.

Use: technology discovery and candidate classification only. These sources identify areas such as EDT, Git, BSL analysis, tests, containers, integration, monitoring and prototyping. They are not bundled, do not prove runtime availability and do not authorize tool execution. Every concrete candidate still passes the adoption rule below.

## RampStack skill-governance methodology

Source: `https://github.com/rampstackco/claude-skills` at commit `0479242522549dfdb389bb9b7807ad4d6016ffb7`.

License: MIT.

Use: methodology reference for uniform skill structure, separation of deep references, deterministic lock files and CI linting. The project implements its own 1C-specific governance in `docs/SKILL_AUTHORING_STANDARD.md`, `tools/validate_skills.py` and `tools/update_skill_lock.py`. RampStack's external skills, private lint inputs, marketing/web catalog and plugin manifests are not copied or added to the marketplace.

## msrv-tech Test Bridge protocol

Reviewed 2026-11-14 from the discovery article https://infostart.ru/1c/articles/2705751/ and repository https://github.com/msrv-tech/skills at immutable commit `702dc8dbe0a0d31b1a16af3d871af29b99ef1122`.

Problem addressed: close the gap between static artifact checks and observable test-base evidence. The article describes 82 operation skills; the reviewed current README describes 13 domains. Old operation paths are not assumed current. This source is distinct from the existing Nikolay-Shirokov marketplace companions.

Intake decision: **protocol reference and optional host adapter only; upstream code/CFE redistribution and automatic installation deferred**. No root LICENSE/COPYING/NOTICE file or explicit license grant was found in the reviewed tree. The repository does not vendor, execute, relicense or install upstream implementation. No sixth marketplace entry is added. License clarification and a separate security/compatibility review are prerequisites to any future redistribution or installation workflow.

The independently authored packaged `one-c-erp-test-bridge` skill supports loopback-only Health/Metadata/Describe/Query capture, exact request/response SHA-256 and offline integrity/context verification. Risk: authorized test-contour reads `R0`, local evidence writes `R1`; bridge installation, external-code rendering, BSL, object changes and UI execution are excluded and require separately classified authorization. Loopback is not proof of test status. The expected metadata name is checked but cannot uniquely identify an infobase. No authentication fallback, credentials, remote access, redirects, proxy inheritance or generic command forwarding.

Validation uses synthetic loopback HTTP fixtures for request encoding, response contracts, failure handling, scope, hash tampering and stale-context rejection. It does not prove compatibility with a live 1C base. Query row limits never become population completeness, and Health does not attest an installed commit. Fallback: offline evidence, separately installed Unica/1C Skills in an authorized disposable contour, or manual exports. Rollback: revert the adapter/skill release; there is no base/publication state to undo. See [the packaged workflow](../plugins/one-c-erp-diagnostics/skills/one-c-erp-test-bridge/references/bridge-contract.md).

## Vercel UI SDK

Reviewed 2026-11-14: https://github.com/vercel-labs/ui at immutable commit `724a7d6c2d0ca1251a8eb6172462ae220c484714`, Apache-2.0. UI SDK is beta. The reviewed standalone skill is `packages/core/skills/ui-sdk` with one entrypoint and seven references; it contains no executable scripts.

Use: a user-scoped UI authoring skill and a project-specific methodology mapping through `one-c-erp-ui-design`. The user skill is independently installed; SDK code and upstream skill contents are not bundled in the primary plugin or marketplace. Actual UI projects install and lock core plus their framework adapter separately. The source pin records reviewed instructions, not certification of a future npm version.

Risk: local instruction installation and UI artifact authoring are bounded local changes. A browser component agent bridge is not 1C access, a Codex MCP backend or permission to send case data to a remote provider. WebMCP, deployments, external data transfer and database mutations retain their own scope and authorization. Ordinary diagnostic and strict-JSON paths do not require this skill. Fallback: existing native form tooling or a plain diagnostic report. Verification: source hashes, cross-workspace discovery, package governance and scoped behavior checks; rendered UI/accounting acceptance belongs to the actual UI task. See [installation and scope](UI_SDK_INTEGRATION.md).

## Adoption rule

A new tool or skill enters the ecosystem only after:

1. source, maintainer and license verification;
2. immutable version/tag/commit pin where technically possible;
3. minimal required capability and permission review;
4. sanitized regression testing;
5. `R0–R3` risk classification;
6. fallback and rollback design;
7. documentation of what the tool can and cannot prove;
8. green CI and plugin self-audit.
