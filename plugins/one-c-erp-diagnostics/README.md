# 1C ERP Diagnostics plugin — v0.3.2

A single dynamic entrypoint for ChatGPT and Codex:

- ChatGPT: `@one-c-erp-diagnostics`
- Codex: `$one-c-erp-diagnostics <task or case>`

## What is bundled in the primary plugin

- Gate 0–10 master orchestration;
- 32 packaged 1C:ERP and control skills;
- capability discovery and bounded dynamic planning;
- evidence coverage, artifact derivation lineage and provenance closure;
- execution identity/stale-result controls for tool and sandbox evidence;
- evidence synthesis, contradiction handling and adversarial verification;
- `R0–R3` risk controls and same-analytics validation;
- artifact/open-source intake rules;
- deterministic Python helpers and publication-integrity validation;
- optional `sonarqube-bsl-local` discovery, safe scan and evidence-provenance contract;
- approved Velis mascot assets for the composer, plugin card and dark surfaces.

The artwork is an original white-dog mascot identity with one Velis collar medallion and does not reproduce the corporate 1C graphic logo. Product references are descriptive; the project is independent from 1C Company and OpenAI.

## What is exposed by the ecosystem marketplace

The repository marketplace also references three independently maintained companions:

- `unica` — Unica `0.12.0` from `IngvarConsulting/unica-marketplace@v0.12.0`;
- `1c-skills` — PowerShell runtime pinned to immutable ref `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- `1c-skills-py` — Python runtime pinned to immutable ref `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

They remain separate plugins. They are not silently installed, copied, relicensed or granted permissions by `one-c-erp-diagnostics`.

## Runtime coordination

Gate 0 records whether Unica, 1C Skills, document tools, GitHub/Drive, Computer Use, OpenSandbox and local SonarQube are actually available and permitted. Missing capabilities become fallback or `blocked`, never simulated.

When a companion/tool result is used as executable evidence, Gate 5 records its run/case/input/tool/output identity. A result tied to a previous or different material input is stale until rerun or proven equivalent.

Derived evidence must preserve its source anchor and transformation. Gate 6/7 require closed provenance across every material causal transition before `УСТАНОВЛЕНО` can become final.

## Safety

Do not include production `.dt`, plaintext credentials, full confidential database backups or unnecessary personal data. External tool output is evidence to verify, not truth by itself. Production/accounting/access actions remain `R3` and require exact approval, rollback and Gate 9 validation.

The release process separately checks the current public tree, full Git history and archive identity; removing a sensitive file from HEAD alone is not treated as sufficient cleanup.
