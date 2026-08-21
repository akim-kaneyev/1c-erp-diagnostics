# Dynamic orchestration architecture

## Design goal

One public diagnostic entrypoint coordinates a changing set of internal skills, verified companion plugins and host tools without treating marketplace presence, runtime availability or tool output as fact.

## Distribution architecture

The repository has two distinct layers:

1. **Ecosystem marketplace** — exposes `one-c-erp-diagnostics`, `unica`, `1c-skills` and `1c-skills-py` from reviewed sources/refs.
2. **Primary orchestrator plugin** — provides the user-facing Gate 0–10 workflow and 32 packaged skills.

The marketplace is an installation/discovery bundle. It does not merge code, grant permissions or create hidden dependencies. Each plugin remains separately installed and governed by its own license, permissions and update channel.

## Runtime layers

1. **Gate controller** — enforces Gate 0–10 and resumable state.
2. **Capability registry** — discovers what the current host actually exposes, including canonical companion names.
3. **Evidence graph** — assigns stable evidence and claim IDs.
4. **Dynamic planner** — builds a bounded dependency graph with exact skills/capabilities and fallbacks.
5. **Domain specialists** — cost, expenses, settlements, VAT, warehouse, production, access, code and release analysis.
6. **Companion coordinator** — delegates bounded tasks to Unica or 1C Skills only when available and justified.
7. **Execution adapters** — Python/PowerShell, OpenSandbox, artifact tools and optional local SonarQube BSL analysis when executable validation adds value.
8. **Synthesis** — preserves supporting and contradicting evidence plus plugin/tool provenance.
9. **Adversarial verifier** — attempts to falsify the preliminary cause using original evidence.
10. **Risk controller** — separates `R0–R3` work and blocks unauthorized high-impact action.
11. **Post-change validator** — checks identical analytics before/after.
12. **Evaluation and release gate** — validates synthetic domain/control coverage, machine-readable Gate results and complete hashed clean-session runtime evidence without exposing expected answers to the runner.

## Canonical companion registry

- `unica` — developer workflows, metadata/BSL investigation and controlled build/test operations.
- `1c-skills` — Windows-first PowerShell 1C tooling.
- `1c-skills-py` — cross-platform Python 1C tooling.

Gate 0 records installation/availability, version/ref when exposed, permission/write surface, purpose and fallback. A companion is never considered available merely because it appears in the marketplace.

## Local static-analysis adapter

`sonarqube-bsl-local` is discovered as a host capability and is not declared in the marketplace. Gate 0 verifies the loopback server, scanner, `communitybsl` plugin/language/profile, pre-created project, version compatibility and scoped authentication. Reading an identified local report is `R0`; a sanitized local scan is `R1`; local project/token/profile administration is `R2`. A remote endpoint is prohibited for this capability; remote source upload/external write would require a separate `R3` workflow.

The adapter captures source identity, tool versions, `report-task.txt`, compute-engine and analysis IDs, quality-gate state, complete paginated issues and artifact hashes. Its findings feed the code specialist as hypotheses and remain subject to factual ERP linkage and Gate 7.

## Bounded planning

A normal case uses:

- one primary domain;
- at most two justified secondary domains;
- no more than four active specialist nodes unless the dependency graph explicitly proves additional value.

Each node defines evidence inputs, exact capability, dependencies, output schema, `R0–R3` risk, falsifier and fallback.

## Parallelism

Parallel specialist work is allowed only for independent read-only questions. Shared-state writes, test mutations and production actions are serialized. The verifier reads original evidence directly rather than trusting the synthesis alone.

## Truth model

Tool output, code findings and official documentation have provenance but different evidentiary roles. Documentation can establish a mechanism; case evidence must establish that the mechanism actually consumed the user's record. External plugin output is never exempt from Gate 7.

## Failure model

- missing optional capability → use documented fallback;
- missing required capability → dependent node/Gate becomes `blocked`;
- contradicting tool results → preserve both, compare inputs/versions/scope, do not vote by majority;
- unapproved `R3` action → stop before execution;
- invalid, incomplete or expectation-contaminated runtime run → release acceptance remains `blocked`;
- new evidence → reopen from the earliest affected gate.
