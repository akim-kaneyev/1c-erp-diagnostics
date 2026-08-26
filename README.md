<p align="center">
  <img src="plugins/one-c-erp-diagnostics/assets/logo.png" alt="1C ERP Diagnostics" width="150" />
</p>

<h1 align="center">1C ERP Diagnostics</h1>

<p align="center">
  <a href="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml"><img alt="Validation" src="https://github.com/akim-kaneyev/1c-erp-diagnostics/actions/workflows/validate.yml/badge.svg" /></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-gold.svg" /></a>
  <img alt="Version 0.3.5" src="https://img.shields.io/badge/version-0.3.5-0D1B2A.svg" />
  <img alt="Public Preview" src="https://img.shields.io/badge/status-public%20preview-2563EB.svg" />
  <img alt="1C ERP" src="https://img.shields.io/badge/domain-1C%3AERP-F5B800.svg" />
</p>

<p align="center"><strong>One evidence-first entrypoint for 1C:ERP diagnostics, backed by a verified companion marketplace and dynamic Gate 0–10 orchestration.</strong></p>

> Independent community project. Not affiliated with or endorsed by 1C Company, OpenAI, Ingvar Consulting or the 1C Skills maintainers. Product names and trademarks belong to their respective owners.

## Why this project exists

Complex 1C:ERP incidents are often diagnosed from the last visible symptom. This project requires a reproducible causal chain instead:

`document → movement → register/record → consuming mechanism → accounting/stock/access result → symptom`

A plausible explanation is not a final cause. Final root-cause `УСТАНОВЛЕНО` requires the dedicated Gate 7 adversarial review and closed provenance for every material causal link.

## Optional companion ecosystem: one marketplace, separate verified plugins

Adding this repository as a marketplace source exposes four independently maintained plugins in one place:

| Plugin | Primary role |
|---|---|
| **1C ERP Diagnostics** | Gate 0–10 orchestration, evidence synthesis and controlled remediation |
| **Unica 0.12.0** | 1C development, metadata/BSL investigation and controlled build/test workflows |
| **1C Skills (PowerShell)** | Windows-first 1C artifact/configurator/web-client tooling |
| **1C Skills (Python)** | Cross-platform 1C artifact parsing and controlled automation |

External plugins are referenced from verified upstream sources and immutable SHAs. They are not copied, silently installed or granted permissions by this repository. Each retains its own license, permissions, updates and confirmation requirements.

See [`docs/ECOSYSTEM_MARKETPLACE.md`](docs/ECOSYSTEM_MARKETPLACE.md) and [`docs/OPEN_SOURCE_INTEGRATIONS.md`](docs/OPEN_SOURCE_INTEGRATIONS.md).

## Dynamic orchestration

The user selects **1C ERP Diagnostics** once. The orchestrator then:

1. discovers only capabilities actually available in the current host;
2. resumes prior case state rather than restarting;
3. inventories every supplied evidence item and preserves artifact hashes/identifiers;
4. traces derived evidence back to its source artifact and transformation;
5. creates a bounded dependency graph of specialist analyses;
6. runs independent read-only specialists in parallel when safe;
7. records evidence, claims, contradictions, tool provenance and execution identity;
8. invokes Unica, 1C Skills or another companion only when installed and justified;
9. classifies every proposed action by risk level `R0–R3`;
10. challenges the preliminary conclusion before any final cause;
11. validates the same analytics before and after a change.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Gate 0–10

| Gate | Purpose |
|---|---|
| 0 | Discover capabilities and resume state |
| 1 | Define a verifiable goal contract |
| 2 | Inventory evidence, derivation lineage and blind spots |
| 3 | Build the dynamic execution graph |
| 4 | Run specialist analysis |
| 5 | Execute isolated/reproducible validation with exact run identity when justified |
| 6 | Synthesize a claim-to-evidence graph and provenance closure |
| 7 | Adversarially challenge the conclusion, lineage and execution freshness |
| 8 | Select the smallest safe action under `R0–R3` controls |
| 9 | Validate identical analytics before/after |
| 10 | Close only the declared goal when all required gates pass |

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

For derived evidence, the project additionally requires artifact lineage: parent Evidence IDs, transformation, tool/version/ref, execution `run_id` when applicable and output identifier/hash. A material root-cause claim is final only when the trace `source artifact → evidence → premise → causal link → conclusion` is closed.

An executable report is not reusable merely because it looks current. Gate 5 records the case, material input identities/hashes, tool/runtime version and output identity; mismatched prior runs are `stale` until rerun or proven equivalent.

## Strict machine-readable evaluation

When a synthetic acceptance prompt contains `EVAL_RESULT_JSON`, the plugin must return exactly one JSON object matching the supplied skeleton.

Version 0.3.3 fixed the first strict-output defect found in the stale-execution smoke test: wrong risk/decision semantics, malformed claim/link/action objects and false six-stage causal-chain completeness.

Version 0.3.4 fixed the provenance-closure boundary:

- synthetic capability snapshots are authoritative;
- internal reasoning steps, packaged skills and reviewer/synthesis roles cannot be invented as runtime capabilities;
- a completed evidence-sufficiency assessment may close its narrow goal while the unresolved incident remains blocked;
- a directly evidenced missing-lineage fact may be established without promoting source content or root cause.

Version 0.3.5 fixes the clean-session capability inventory contract:

- successful inventory completion is not a proved 1C/root-cause conclusion, so `final_status=ТРЕБУЕТ ПРОВЕРКИ`;
- a closed Gate-0-only goal requires Gate 10 `passed`, while Gates 1–9 are `not_required`;
- every strict capability item is exactly `{name,status,simulated}` with `simulated=false`;
- `evidence_id` is forbidden inside capability rows; snapshot evidence stays in `evidence_ids_used`;
- capability statuses are inventory rows, not claims, so the canonical result uses `claims=[]`;
- `УСТАНОВЛЕНО` is rejected unless Gate 7 and Gate 10 pass and the six-stage causal chain is complete.

The strict mode separates three concepts that must not be collapsed: capability inventory, bounded procedure closure and diagnostic proof status.

## Additional capabilities

- PDF, Spreadsheets and Documents for evidence extraction;
- GitHub and Drive for user-referenced sources;
- Computer Use for observation or explicitly approved interaction;
- OpenSandbox for isolated executable validation;
- pinned `v8unpack` for non-executing extraction of sanitized CF/CFE/EPF;
- optional `sonarqube-bsl-local` analysis after extraction, with BSL Language Server/manual review as fallback.

Gate 0 records whether every capability is `available`, `confirmation_required`, `unavailable` or `prohibited`. Missing capabilities become a documented fallback or `blocked`, never a simulated result.

## Quick start

### ChatGPT / Codex marketplace

Add this repository as a marketplace source:

```text
Source: akim-kaneyev/1c-erp-diagnostics
Git ref: main
Selective paths: empty
```

Install **1C ERP Diagnostics** as the primary entrypoint. Install companion plugins needed for the current workflow. Invoke:

`@one-c-erp-diagnostics`

The internal marketplace ID remains `one-c-erp-diagnostics-marketplace` for upgrade compatibility; the visible marketplace title is `1C ERP Diagnostics Ecosystem`.

### Codex repository-local skill

`.agents/skills/one-c-erp-diagnostics/SKILL.md`

Global invocation after installation:

`$one-c-erp-diagnostics <task or case>`

The complete procedure and smoke tests are in [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

## Supported artifacts

- XLSX profiling and structural comparison;
- PDF text extraction;
- deterministic case indexing and SHA-256 manifests;
- optional sanitized CF/CFE/EPF extraction through pinned `v8unpack`;
- optional local SonarQube/BSL static analysis after extraction, with versioned provenance and sanitized report hashes.

There is no pretend universal MXL parser. Use a verified export to XLSX/XML/HTML/TXT and PDF for visual control when appropriate.

## Safety and publication integrity

Do not upload production `.dt`, backups, credentials, tokens, unnecessary personal data or broad confidential exports. Production/accounting/access writes are `R3` and require explicit approval, rollback and Gate 9 validation.

Current-tree cleanliness is not sufficient for a public release. CI also validates the full Git history and the actual `git archive HEAD` tree so deleted confidential artifacts, environment files, key material, case data or obvious credential residue cannot be ignored merely because they are absent from the latest checkout.

See `SECURITY.md`, `PRIVACY.md`, `TERMS.md`, `SUPPORT.md` and [`plugins/one-c-erp-diagnostics/PUBLISHING.md`](plugins/one-c-erp-diagnostics/PUBLISHING.md).

## Project structure

- `SKILL.md` — authoritative dynamic Gate 0–10 and strict evaluation contract;
- `.agents/plugins/marketplace.json` — unified verified 1C marketplace;
- `plugins/one-c-erp-diagnostics/` — primary ChatGPT/Codex plugin;
- `playbooks/` — domain-specific diagnostic rules;
- `templates/case/STATE.md` — resumable state, evidence lineage, execution and claim ledgers;
- `evals/` — synthetic executable acceptance cases and machine-readable result contracts;
- `tools/` — deterministic evidence and release validation;
- `docs/` — architecture, integrations, audit and release controls.

The eval suite is validated in CI. A plugin version is runtime-accepted only after a complete hashed clean-session run passes [`tools/validate_runtime_run.py`](tools/validate_runtime_run.py); see [`docs/RUNTIME_ACCEPTANCE.md`](docs/RUNTIME_ACCEPTANCE.md).

## Status

**v0.3.5 Public Preview release candidate.** This hotfix corrects the exact clean-session capability-inventory deviations observed in installed v0.3.4. It preserves earlier stale-execution and provenance-closure controls, artifact provenance, execution identity, deterministic skill locking, full-history publication validation, the verified four-plugin marketplace, 32 packaged skills and approved Velis assets.

Protected Pull Request CI, CodeQL, merge and exact-version clean-session acceptance for `0.3.5` remain separate evidence until completed. Runtime acceptance is **BLOCKED** until the refreshed installed version passes the canonical `capability-inventory` case, the two earlier priority cases and then the full 16-case run.

Public preview means the workflow is usable and safety-tested, but host capabilities, companion availability and cross-plugin delegation may vary by ChatGPT/Codex plan, workspace, session and permissions. Gate 0 must always report actual runtime state outside deterministic synthetic eval snapshots.

The repository marketplace and the global ChatGPT Plugin Directory remain separate distribution channels. Refresh an existing marketplace installation after each version change; global listing publication requires the supported OpenAI-side publish flow.

## Contributing

Contributions are welcome when they preserve evidence-first reasoning, explicit uncertainty, reproducibility, source provenance and data minimization. See `CONTRIBUTING.md`.

## License

The project code is MIT. Referenced companion plugins retain their own licenses. Reviewed external methodology is not copied as external implementation code. See `LICENSE` and `docs/ECOSYSTEM_MARKETPLACE.md`.
