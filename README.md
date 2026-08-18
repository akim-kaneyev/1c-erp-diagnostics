<p align="center">
  <img src="plugins/one-c-erp-diagnostics/assets/logo.png" alt="1C ERP Diagnostics" width="150" />
</p>

<h1 align="center">1C ERP Diagnostics</h1>

<p align="center">
  <a href="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml"><img alt="Validation" src="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml/badge.svg" /></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-gold.svg" /></a>
  <img alt="Version 0.2.2" src="https://img.shields.io/badge/version-0.2.2-0D1B2A.svg" />
  <img alt="1C ERP" src="https://img.shields.io/badge/domain-1C%3AERP-F5B800.svg" />
</p>

<p align="center"><strong>One evidence-first entrypoint for 1C:ERP diagnostics, backed by a verified companion marketplace and dynamic Gate 0–10 orchestration.</strong></p>

> Independent community project. Not affiliated with or endorsed by 1C Company, OpenAI, Ingvar Consulting or the 1C Skills maintainers. Product names and trademarks belong to their respective owners.

## Why this project exists

Complex 1C:ERP incidents are often diagnosed from the last visible symptom. This project requires a reproducible causal chain instead:

`document → movement → register/record → consuming mechanism → accounting/stock/access result → symptom`

A plausible explanation is not a final cause. Final `УСТАНОВЛЕНО` requires the dedicated Gate 7 adversarial review.

## Optional companion ecosystem: one marketplace, separate verified plugins

Adding this repository as a marketplace source exposes four independently maintained plugins in one place:

| Plugin | Primary role |
|---|---|
| **1C ERP Diagnostics** | Gate 0–10 orchestration, evidence synthesis and controlled remediation |
| **Unica 0.12.0** | 1C development, metadata/BSL investigation and controlled build/test workflows |
| **1C Skills (PowerShell)** | Windows-first 1C artifact/configurator/web-client tooling |
| **1C Skills (Python)** | Cross-platform 1C artifact parsing and controlled automation |

The external plugins are referenced from verified upstream sources and immutable SHAs. They are not copied, silently installed or granted permissions by this repository. Each retains its own license, permissions, updates and confirmation requirements.

See [`docs/ECOSYSTEM_MARKETPLACE.md`](docs/ECOSYSTEM_MARKETPLACE.md) and [`docs/OPEN_SOURCE_INTEGRATIONS.md`](docs/OPEN_SOURCE_INTEGRATIONS.md).

## Dynamic orchestration

The user selects **1C ERP Diagnostics** once. The orchestrator then:

1. discovers only capabilities actually available in the current host;
2. resumes prior case state rather than restarting;
3. creates a bounded dependency graph of specialist analyses;
4. runs independent read-only specialists in parallel when safe;
5. records evidence, claims, contradictions and tool provenance;
6. invokes Unica, 1C Skills or another companion only when installed and justified;
7. uses executable validation only when it adds measurable value;
8. classifies every proposed action by risk level `R0–R3`;
9. challenges the preliminary conclusion before any final cause;
10. validates the same analytics before and after a change.

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

## Additional capabilities

- PDF, Spreadsheets and Documents for evidence extraction;
- GitHub and Drive for user-referenced sources;
- Computer Use for observation or explicitly approved interaction;
- OpenSandbox for isolated executable validation;
- pinned `v8unpack` for non-executing extraction of sanitized CF/CFE/EPF;
- optional BSL static analysis after extraction.

Gate 0 records whether every capability is `available`, `confirmation_required`, `unavailable` or `prohibited`. Missing capabilities become a documented fallback or `blocked`, never a simulated result.

## Quick start

### ChatGPT / Codex marketplace

Add this repository as a marketplace source:

```text
Source: akim-kaneyev/1c-erp-diagnostics
Git ref: main
Selective paths: empty
```

Install **1C ERP Diagnostics** as the primary entrypoint. Install the companion plugins needed for the current workflow. Invoke:

`@one-c-erp-diagnostics`

The internal marketplace ID remains `one-c-erp-diagnostics-marketplace` for upgrade compatibility; the visible marketplace title is `1C ERP Diagnostics Ecosystem`.

### Codex repository-local skill

`.agents/skills/one-c-erp-diagnostics/SKILL.md`

Global invocation after installation:

`$one-c-erp-diagnostics <task or case>`

The complete procedure and smoke tests are in [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

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

Do not upload production `.dt`, backups, credentials, tokens, unnecessary personal data or broad confidential exports. Production/accounting/access writes are `R3` and require explicit approval, rollback and Gate 9 validation. See `SECURITY.md`, `PRIVACY.md`, `TERMS.md` and `SUPPORT.md`.

## Project structure

- `SKILL.md` — authoritative dynamic Gate 0–10 contract;
- `.agents/plugins/marketplace.json` — unified verified 1C marketplace;
- `plugins/one-c-erp-diagnostics/` — primary ChatGPT/Codex plugin;
- `playbooks/` — domain-specific diagnostic rules;
- `templates/case/STATE.md` — resumable state, capability and claim ledgers;
- `tools/` — deterministic evidence preparation;
- `docs/` — architecture, integrations, audit and release controls.

## Status

Current candidate: **0.2.2**. It preserves the verified Unica/1C Skills ecosystem, fixes in-place marketplace refresh by restoring the stable installation identity, uses verified SHA selectors for external commits, and includes the scoped Gate-closure correction found during the R3 smoke test. Repository publication and global Plugin Directory submission remain separate final steps after refresh verification and public visibility.

## Contributing

Contributions are welcome when they preserve evidence-first reasoning, explicit uncertainty, reproducibility, source provenance and data minimization. See `CONTRIBUTING.md`.

## License

The project code is MIT. Referenced companion plugins retain their own licenses. See `LICENSE` and `docs/ECOSYSTEM_MARKETPLACE.md`.
