# Dynamic orchestration architecture

## Design goal

One public entrypoint coordinates a changing set of internal skills, host tools and optional companion plugins without treating availability or output as fact.

## Layers

1. **Gate controller** — enforces Gate 0–10 and resumable state.
2. **Capability registry** — discovers what the current host actually exposes.
3. **Evidence graph** — assigns stable evidence and claim IDs.
4. **Dynamic planner** — builds a bounded dependency graph.
5. **Domain specialists** — cost, expenses, settlements, VAT, warehouse, production, access, code and release analysis.
6. **Execution adapters** — Python/PowerShell, OpenSandbox and artifact tools when justified.
7. **Synthesis** — preserves supporting and contradicting evidence.
8. **Adversarial verifier** — attempts to falsify the preliminary cause.
9. **Risk controller** — separates read-only work from production-impacting actions.
10. **Post-change validator** — checks identical analytics before/after.

## External companions

Unica and 1C Skills can strengthen code/developer and executable workflows when they are installed and exposed. They are not copied into this repository and are not portable hard dependencies. Other host plugins are selected by capability rather than brand name.

## Parallelism

Parallel specialist work is allowed only for independent read-only questions. Shared-state writes, test mutations and production actions are serialized. The verifier reads original evidence directly.

## Truth model

Tool output, code findings and official documentation have provenance but different evidentiary roles. Documentation can establish a mechanism; case evidence must establish that the mechanism actually consumed the user's record.
