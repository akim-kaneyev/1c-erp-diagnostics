# 1C ERP Diagnostics Ecosystem marketplace

## Purpose

The repository marketplace provides one installation source for a controlled 1C:Enterprise analysis ecosystem. It does **not** merge third-party code into one binary package and does not bypass each plugin's permissions.

The marketplace contains:

| Plugin | Role | Source/SHA | License |
|---|---|---|---|
| `one-c-erp-diagnostics` | Evidence-first Gate 0–10 orchestration for 1C:ERP incidents | this repository, local package | MIT |
| `unica` | 1C developer workflows, BSL/metadata investigation and controlled build/test capabilities | `IngvarConsulting/unica-marketplace`, SHA `aefc880f9bab606a5c55ed11af563b740054a549` (release tag `v0.12.0`), path `plugins/unica` | LGPL-3.0-or-later |
| `1c-skills` | Windows-first PowerShell tooling for 1C artifacts, configurator and web-client workflows | `Nikolay-Shirokov/cc-1c-skills`, SHA `8cb7868145281d8e353831512cc1ffa72f1b5c89` | MIT |
| `1c-skills-py` | Cross-platform Python tooling for 1C artifacts and automation | `Nikolay-Shirokov/cc-1c-skills`, SHA `c1f79f5ac9f31c620b8508f75464f8c42c559ae4` | MIT |

## Stable marketplace identity

The internal marketplace ID is:

```text
one-c-erp-diagnostics-marketplace
```

It is an installation identity, not display text. It must remain stable after users add the marketplace. The visible title may evolve through `interface.displayName`, currently `1C ERP Diagnostics Ecosystem`.

OpenAI's marketplace updater validates that the ID in an upgraded checkout matches the ID stored in the user's marketplace configuration. Renaming the internal ID breaks in-place refresh even when the Git repository and display title are unchanged. Any future branding change must therefore modify only the display name, never the internal marketplace ID.

## Why this architecture

OpenAI plugins are packages of skills and optional apps. The current public manifest contract does not define a generic field that embeds arbitrary third-party plugins as hidden dependencies. Therefore the safe and portable design is:

1. one marketplace exposes the verified plugins;
2. the user/workspace chooses which companions to install;
3. Gate 0 discovers what is actually available and permitted in the current session;
4. `one-c-erp-diagnostics` coordinates only those capabilities;
5. unavailable capabilities become fallback or `blocked`, never simulated.

This preserves:

- third-party licenses and update channels;
- explicit installation and permissions;
- action confirmation for write-capable tools;
- reproducible source/SHA provenance;
- a single user-facing diagnostic entrypoint.

## Installation

Add the repository as a marketplace source:

```text
Source: akim-kaneyev/1c-erp-diagnostics
Git ref: main
Selective paths: empty
```

The marketplace should show four independently installable plugins. Install `1C ERP Diagnostics` as the primary entrypoint. Install Unica and one or both 1C Skills runtimes only when their capabilities are required and their permissions are acceptable.

## Host-adapter boundary

`sonarqube-bsl-local` is intentionally absent from the marketplace table. SonarQube, SonarScanner and the BSL analyzer are separately installed host software rather than ChatGPT/Codex plugins. Gate 0 may discover and use that optional loopback capability under the reviewed `R0–R3` contract, but marketplace installation neither supplies it nor proves it available.

## Runtime contract

A diagnostic starts with `@one-c-erp-diagnostics`.

Gate 0 records, for every companion:

- canonical name and version/SHA where exposed;
- installation and availability status;
- required confirmation or permissions;
- read/write surface and `R0–R3` risk;
- assigned task and evidence IDs;
- fallback if unavailable.

The orchestrator may delegate a bounded task, but the final causal conclusion remains governed by the project evidence standard and Gate 7 adversarial verification.

## Provenance rationale

The marketplace uses the official `sha` selector for every external plugin commit. The installer checks out the requested SHA and verifies that `HEAD` matches it. The human-readable Unica release tag `v0.12.0` was resolved to SHA `aefc880f9bab606a5c55ed11af563b740054a549` before inclusion. The 1C Skills SHAs are generated Codex plugin commits produced from upstream source commit `113dc9e9280b33b7aa3e4691eb8915cdaddea65b`.

Immutable SHAs prevent a reviewed marketplace package from changing silently when an upstream branch or tag target changes. They do not replace installation-time review, license review or runtime permission controls.

## Update policy

External SHAs are reviewed before change. A SHA update requires:

1. upstream source and license verification;
2. manifest and release review;
3. sanitized regression tests;
4. comparison of capabilities and permission surface;
5. fallback/rollback documentation;
6. green repository CI and plugin self-audit.

Mutable branch names are not used for external plugin entries in the public candidate.

The primary plugin's semantic version must change whenever packaged skills, manifest metadata or runtime behavior changes. This prevents an updated marketplace checkout from retaining an older installed plugin cache under the same version.

## Non-goals

The marketplace does not:

- copy or relicense Unica or 1C Skills;
- bundle, install or configure SonarQube, SonarScanner or the BSL analyzer;
- silently install or enable companions;
- guarantee that every ChatGPT surface exposes cross-plugin invocation;
- grant access to production 1C data;
- make external plugin output proof of an accounting cause;
- authorize writes, closed-period changes, mass reposting or access-right changes.
