<p align="center">
  <img src="plugins/one-c-erp-diagnostics/assets/logo.png" alt="1C ERP Diagnostics" width="150" />
</p>

<h1 align="center">1C ERP Diagnostics</h1>

<p align="center">
  <a href="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml"><img alt="Validation" src="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml/badge.svg" /></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-gold.svg" /></a>
  <img alt="Version 0.2.0" src="https://img.shields.io/badge/version-0.2.0-0D1B2A.svg" />
  <img alt="1C ERP" src="https://img.shields.io/badge/domain-1C%3AERP-F5B800.svg" />
</p>

<p align="center"><strong>Dynamic evidence-first diagnostics for 1C:ERP with Gate 0–10 orchestration, optional companion capabilities and adversarial verification.</strong></p>

> Independent community project. Not affiliated with or endorsed by 1C Company or OpenAI. Product names and trademarks belong to their respective owners.

## Why this project exists

Complex 1C:ERP incidents are often diagnosed from the last visible symptom. This project requires a reproducible causal chain instead:

`document → movement → register/record → consuming mechanism → accounting/stock/access result → symptom`

A plausible explanation is not a final cause. Final `УСТАНОВЛЕНО` requires the dedicated Gate 7 adversarial review.

## Dynamic orchestration

The user selects one plugin or invokes one Codex skill. The orchestrator then:

1. discovers only the capabilities actually available in the current host;
2. resumes prior case state rather than restarting;
3. creates a bounded dependency graph of specialist analyses;
4. runs independent read-only specialists in parallel when safe;
5. records evidence, claims, contradictions and tool provenance;
6. uses executable validation only when it adds measurable value;
7. classifies every proposed action by risk level `R0–R3`;
8. challenges the preliminary conclusion before any final cause;
9. validates the same analytics before and after a change.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Gate 0–10

| Gate | Purpose |
|---|---|
| 0 | Discover capabilities and resume state |
| 1 | Define a verifiable goal contract |
| 2 | Inventory evidence and blind spots |
| 3 | Build the dynamic execution graph |
| 4 | Run specialist analysis |
| 5 | Execute isolated/reproducible validation when justified |
| 6 | Synthesize a claim-to-evidence graph |
| 7 | Adversarially challenge the conclusion |
| 8 | Select the smallest safe action under `R0–R3` controls |
| 9 | Validate identical analytics before/after |
| 10 | Close only when all required gates pass |

## Diagnostic domains

- cost calculation and month close;
- post-item expenses and allocation;
- settlements, advances and offsets;
- VAT records, books and period corrections;
- warehouse, series and assignments;
- production, stages, returns and repair;
- access rights and organization restrictions;
- supplied BSL/query/СКД analysis;
- platform/configuration release differences;
- correct-vs-problematic document comparison.

## Optional companion ecosystem

The orchestrator can coordinate external capabilities when the host actually exposes them:

- **Unica** for 1C developer workflows and code-oriented investigation;
- **1C Skills (Python/PowerShell)** for parsing, indexing, comparison and controlled automation;
- **PDF, Spreadsheets and Documents** for evidence extraction;
- **GitHub and Drive** for user-referenced sources;
- **Computer Use** for observation or explicitly approved interaction;
- **OpenSandbox** for isolated executable validation.

These companions are **not copied into this repository and are not fabricated hard dependencies**. Their private implementation, versions, permissions and installation remain host-managed. Gate 0 records whether each capability is actually available; unavailable required capabilities become `blocked` rather than simulated.

Reviewed open-source integrations and their boundaries are documented in [`docs/OPEN_SOURCE_INTEGRATIONS.md`](docs/OPEN_SOURCE_INTEGRATIONS.md).

## Quick start

### ChatGPT

Add this repository as a marketplace source, enable **1C ERP Diagnostics**, and select:

`@one-c-erp-diagnostics`

### Codex

Repository-local entrypoint:

`.agents/skills/one-c-erp-diagnostics/SKILL.md`

Global invocation after installation:

`$one-c-erp-diagnostics <task or case>`

The full procedure and smoke tests are in [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

## Evidence standard

Priority:

1. exact document movements;
2. exact register records;
3. postings and drill-downs;
4. report exports;
5. supplied metadata/code/queries;
6. screenshots;
7. current official documentation;
8. general theory only as a source of hypotheses.

External plugin output and official documentation have provenance but different roles. Documentation may establish how a mechanism works; case evidence must establish that it consumed the user's exact record.

## Supported artifacts

- XLSX profiling and structural comparison;
- PDF text extraction;
- deterministic case indexing and SHA-256 manifests;
- optional sanitized CF/CFE/EPF extraction through pinned `v8unpack`;
- optional static BSL analysis after extraction.

There is no pretend universal MXL parser. Use a verified export to XLSX/XML/HTML/TXT and PDF for visual control when appropriate.

## Safety

Do not upload production `.dt`, backups, credentials, tokens, unnecessary personal data or broad confidential exports. Production/accounting/access writes are `R3` and require explicit approval, rollback and Gate 9 validation. See `SECURITY.md`, `PRIVACY.md` and `SUPPORT.md`.

## Project structure

- `SKILL.md` — authoritative dynamic Gate 0–10 contract;
- `plugins/one-c-erp-diagnostics/` — packaged ChatGPT/Codex plugin;
- `playbooks/` — domain-specific diagnostic rules;
- `templates/case/STATE.md` — resumable state, capability and claim ledgers;
- `tools/` — deterministic evidence preparation;
- `docs/` — architecture, integrations, audit and release controls.

## Status

Current development candidate: **0.2.0**. It repairs the brand assets and adds dynamic capability discovery, bounded planning, evidence synthesis, optional companion coordination, artifact extraction and `R0–R3` action controls. Public release remains blocked until CI, plugin re-import and clean-session smoke tests pass.

## Contributing

Contributions are welcome when they preserve evidence-first reasoning, explicit uncertainty, reproducibility and data minimization. See `CONTRIBUTING.md`.

## License

MIT. See `LICENSE`.
