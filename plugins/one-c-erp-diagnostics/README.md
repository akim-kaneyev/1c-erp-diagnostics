# 1C ERP Diagnostics plugin — v0.3.7

A single dynamic entrypoint for ChatGPT and Codex:

- ChatGPT: `@one-c-erp-diagnostics`
- Codex: `$one-c-erp-diagnostics <task or case>`

## What is bundled in the primary plugin

- Gate 0–10 master orchestration;
- 32 packaged 1C:ERP and control skills;
- capability discovery and bounded dynamic planning;
- evidence coverage, artifact derivation lineage and provenance closure;
- execution identity/stale-result controls for tool and sandbox evidence;
- deterministic raw-row accounting invariants, observed allocation reconciliation and before/after effect classification;
- machine-readable case-state uniqueness, reference and invalidation-closure validation;
- evidence synthesis, contradiction handling and adversarial verification;
- strict `EVAL_RESULT_JSON` output with exact schema/risk/decision/Gate semantics;
- deterministic synthetic capability snapshots and scoped current-goal/linked-incident closure;
- inventory-only output semantics with exact `{name,status,simulated}` capability rows;
- `R0–R3` action-risk controls and same-analytics validation;
- artifact/open-source intake rules;
- property-tree versus row-data controls and credential-incident tree/history/archive scanning;
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

Gate 0 records whether Unica, 1C Skills, document tools, GitHub/Drive, Computer Use, OpenSandbox and local SonarQube are actually available and permitted. Missing capabilities become fallback or `blocked`, never simulated. A public global-plugin/dependency resolver miss is not by itself proof that the currently selected skills-first custom-marketplace plugin is absent.

In synthetic `EVAL_RESULT_JSON` cases, the case capability snapshot is authoritative. Internal reasoning steps, packaged skills and reviewer/synthesis roles are not host capabilities. If the synthetic case declares none, the result must contain `capabilities: []`.

Every strict capability row is exactly `{name,status,simulated}` with `simulated=false`. Evidence IDs remain in top-level `evidence_ids_used`; capability rows do not contain `evidence_id` and are not promoted into claims.

When a companion/tool result is used as executable evidence, Gate 5 records its run/case/input/tool/output identity. A result tied to a previous or different material input is stale until rerun or proven equivalent.

Derived evidence must preserve its source anchor and transformation. Gate 6/7 require closed provenance across every material causal transition before a root-cause `УСТАНОВЛЕНО` can become final. A directly evidenced limitation such as missing lineage may itself be established without proving source content or cause.

## Strict evaluation output

When a prompt contains `EVAL_RESULT_JSON`, the plugin returns one JSON object only and must match the supplied skeleton exactly. Gate status records whether the Gate procedure completed, not whether the cause was proved. Read-only rejection of stale evidence is `R0 + EVIDENCE_REQUIRED`; `R3 + NO-GO` is reserved for an actual unsafe or unapproved write action.

For `capability-inventory`, use `ТРЕБУЕТ ПРОВЕРКИ`, `R0`, `NO_ACTION`, current goal closed, linked incident not in scope, Gate 0/10 passed, Gates 1–9 not required, exact capability rows, `claims=[]`, false causal-chain completeness and no actions.

The declared current goal and linked incident close independently. A bounded evidence-sufficiency assessment may close after correctly requiring more evidence, while the linked source/root-cause incident remains `blocked` or `open`. `not_in_scope` requires an explicit exclusion.

Claim, causal-link and action arrays use their exact structured item contracts. `causal_chain.complete=true` is reserved for the six canonical 1C stages in order. `УСТАНОВЛЕНО` requires Gate 7, Gate 10, a closed goal and complete causality.

## Safety

Do not include production `.dt`, plaintext credentials, full confidential database backups or unnecessary personal data. External tool output is evidence to verify, not truth by itself. Production/accounting/access actions remain `R3` and require exact approval, rollback and Gate 9 validation.

The release process separately checks the current public tree, full Git history and archive identity; removing a sensitive file from HEAD alone is not treated as sufficient cleanup.

Runtime acceptance for the v0.3.7 baseline remains blocked until the exact installed capability-inventory result and the complete hashed 16-case clean-session run pass their validators. The accounting/state changes in this branch are an unversioned candidate and remain blocked from publication until an explicitly approved synchronized version passes the complete hashed 26-case clean-session run.
