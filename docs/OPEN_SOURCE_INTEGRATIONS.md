# Reviewed open-source integrations

Review date: 2026-08-26.

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

Reviewed release tag: `v0.12.0`.

Immutable marketplace ref: `aefc880f9bab606a5c55ed11af563b740054a549`.

Plugin path: `plugins/unica`.

Manifest version: `0.12.0`.

License: LGPL-3.0-or-later.

Use: optional 1C developer workflows, metadata/BSL investigation and controlled build/test operations. Unica remains an independently installed plugin; this project does not copy or relicense it.

## 1C Skills

Canonical source: `https://github.com/Nikolay-Shirokov/cc-1c-skills.git`

License: MIT.

Reviewed immutable generated refs:

- PowerShell plugin `1c-skills`: `8cb7868145281d8e353831512cc1ffa72f1b5c89` (generated from upstream source commit `113dc9e9280b33b7aa3e4691eb8915cdaddea65b`).
- Python plugin `1c-skills-py`: `c1f79f5ac9f31c620b8508f75464f8c42c559ae4` (generated from the same upstream source commit).

Use: optional 1C artifact/configurator/web-client tooling. The PowerShell variant is Windows-first; the Python variant is cross-platform. Both remain independently installed plugins and retain their own permissions and release lifecycle.

## Unified marketplace

`.agents/plugins/marketplace.json` exposes `one-c-erp-diagnostics`, Unica and both 1C Skills variants from one source. This is a discovery/installation bundle, not code vendoring and not a permission bypass. All external entries use immutable commit refs. See `docs/ECOSYSTEM_MARKETPLACE.md`.

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
