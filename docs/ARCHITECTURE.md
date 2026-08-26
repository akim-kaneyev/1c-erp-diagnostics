# Dynamic orchestration architecture

## Design goal

One public diagnostic entrypoint coordinates a changing set of internal skills, verified companion plugins and host tools without treating marketplace presence, runtime availability or tool output as fact.

The project is intentionally a **harness around a model**, not a model-specific prompt bundle. Correctness must come from explicit instructions, tool/capability boundaries, an inspect → hypothesize → test → compare loop, evidence provenance and deterministic acceptance gates. Model/provider identity is runtime provenance, not evidence of correctness.

## Distribution architecture

The repository has two distinct layers:

1. **Ecosystem marketplace** — exposes `one-c-erp-diagnostics`, `unica`, `1c-skills` and `1c-skills-py` from reviewed sources/refs.
2. **Primary orchestrator plugin** — provides the user-facing Gate 0–10 workflow and 32 packaged skills.

The marketplace is an installation/discovery bundle. It does not merge code, grant permissions or create hidden dependencies. Each plugin remains separately installed and governed by its own license, permissions and update channel.

## Runtime layers

1. **Gate controller** — enforces Gate 0–10 and resumable state.
2. **Capability registry** — discovers host-visible external/plugin/tool surfaces and records canonical companion names plus model/provider provenance where exposed.
3. **Scope controller** — separates the declared current goal from the linked accounting/operational/technical incident and closes them independently.
4. **Evidence graph** — assigns stable evidence and claim IDs.
5. **Evidence coverage controller** — accounts for every supplied source/attachment and prevents silent omission of material inputs.
6. **Derivation/provenance controller** — traces each material derived artifact to source Evidence IDs, transformation, tool/version/ref, execution identity and output hash/identifier.
7. **Dynamic planner** — builds a bounded dependency graph with exact skills/capabilities, validation levels and fallbacks.
8. **Domain specialists** — cost, expenses, settlements, VAT, warehouse, production, access, code and release analysis.
9. **Companion coordinator** — delegates bounded tasks to Unica or 1C Skills only when available and justified.
10. **Execution adapters** — Python/PowerShell, OpenSandbox, artifact tools and optional local SonarQube BSL analysis when executable validation adds value.
11. **Execution identity controller** — binds executable evidence to `run_id`, case identity, material input identities/hashes, tool/runtime version and output identity; mismatched prior runs become stale.
12. **Synthesis** — preserves supporting/contradicting evidence and requires provenance closure for material claims.
13. **Adversarial verifier** — attempts to falsify the preliminary cause using original evidence and verifies provenance closure plus run freshness.
14. **Visual Explanation projector** — optionally renders the Gate 7-reviewed Gate 6 ledger as `diagram` or `sticky` presentation without feeding anything back into evidence, claims or Gate state.
15. **Risk controller** — separates `R0–R3` work and blocks unauthorized high-impact action.
16. **Validation ladder / post-change validator** — requires the highest validation level demanded by the claim: structural → static → metadata/runtime → functional → business/accounting.
17. **Evaluation and release gate** — validates synthetic domain/control coverage, exact machine-readable Gate results and complete hashed clean-session runtime evidence without exposing expected answers to the runner.
18. **Synthetic capability-snapshot controller** — requires eval results to reproduce exactly the capabilities declared by the case; internal reasoning, skills and roles cannot be emitted as runtime capabilities.
19. **Publication integrity gate** — compares the Git archive with tracked HEAD, requires full history in CI and scans history for prohibited case/database/credential artifacts, plaintext credential assignments and user-machine absolute paths.
20. **Regression feedback loop** — escaped defects, contradictions and material omissions are traced to the earliest missed control and converted into an eval/checklist improvement when reproducible.

## Model/provider neutrality

The orchestrator contract is provider-neutral. A different model may expose different context limits, tool-use behavior or reasoning quality, but it enters through the same capability/evidence contract. The harness must not weaken Gate requirements because a model is more confident, newer, or from a preferred provider.

Where host differences require translation, normalize them into capability status, input/output provenance and risk rather than embedding provider-specific correctness assumptions into domain logic.

## Capability boundary

A capability is a host-visible external/plugin/tool surface. Packaged skills, specialist roles, synthesis, review and ordinary model reasoning are orchestration internals, not capabilities.

Visual Explanation and its `diagram`/`sticky` modes are presentation concepts inside the orchestrator. They require no image-generation tool and never appear in Gate 0 inventory or a synthetic capability snapshot.

For normal cases Gate 0 discovers the current host state. For synthetic evals the case capability snapshot is authoritative and deterministic:

- every declared capability must be returned with the declared status;
- no undeclared capability may be added;
- an empty snapshot requires `capabilities: []`.

This prevents a model from creating convincing but nonexistent runtime surfaces such as “read-only synthesis capability” or “adversarial review tool”.

## Scope closure

The current goal and linked incident are separate state variables.

- A request to assess evidence sufficiency, compare two exports or evaluate action safety can complete even when the underlying 1C incident remains unresolved.
- `EVIDENCE_REQUIRED` may therefore coexist with `current_goal_status=closed` when the bounded goal was only to determine whether evidence is sufficient.
- The linked incident remains `blocked` or `open` when source content/root cause is still unresolved.
- `not_in_scope` requires an explicit exclusion; missing evidence does not make an incident out of scope.

This avoids both false closure of the whole incident and false blocking of a completed narrow assessment.

## Evidence derivation and provenance closure

Original evidence is an artifact anchor. A parser export, normalized table, filtered dataset, joined report, comparison result or analyzer report is derived evidence rather than a new independent fact source.

A material derivation records parent Evidence IDs, transformation, tool/version/ref, run identity when executable and output hash/identifier where stable. The claim graph must close this path:

`source artifact → inspected/derived evidence → claim premise → causal link → conclusion`.

A set of individually valid references is insufficient when the transition between them is not demonstrated. Material closure is `closed`, `open` or `broken`; `open`/`broken` prevents final root-cause `УСТАНОВЛЕНО` for the dependent claim.

Claim status is assigned per statement. The directly observed absence of lineage metadata may be established while the source value, source-to-derived relationship and root cause remain unproved. An established limitation cannot be promoted into an established cause, and an unproved cause does not erase an observed limitation.

## Execution identity and stale evidence

Executable evidence is accepted only for the case/input generation that produced it. The minimum record is `run_id`, `case_id`, input Evidence IDs plus hashes/stable identifiers, tool/runtime version/ref, operation, timestamps when exposed, output identifier/hash, status and limitations.

If a material input changes after a run, or the report belongs to another case/input identity, the output becomes `stale`. It must be rerun or shown deterministically equivalent before it can support current claims. This prevents a technically valid report from being used against the wrong artifact generation.

## Canonical companion registry

- `unica` — developer workflows, metadata/BSL investigation and controlled build/test operations.
- `1c-skills` — Windows-first PowerShell 1C tooling.
- `1c-skills-py` — cross-platform Python 1C tooling.

Gate 0 records installation/availability, version/ref when exposed, permission/write surface, purpose and fallback. A companion is never considered available merely because it appears in the marketplace.

## Local static-analysis adapter

`sonarqube-bsl-local` is discovered as a host capability and is not declared in the marketplace. Gate 0 verifies the loopback server, scanner, `communitybsl` plugin/language/profile, pre-created project, version compatibility and scoped authentication. Reading an identified local report is `R0`; a sanitized local scan is `R1`; local project/token/profile administration is `R2`. A remote endpoint is prohibited for this capability; remote source upload/external write would require a separate `R3` workflow.

The adapter captures source identity, tool versions, `report-task.txt`, compute-engine and analysis IDs, quality-gate state, complete paginated issues and artifact hashes. Its findings feed the code specialist as hypotheses and remain subject to factual ERP linkage, execution-identity matching and Gate 7.

## Bounded planning

A normal case uses one primary domain, at most two justified secondary domains, and no more than four active specialist nodes unless the dependency graph explicitly proves additional value. Each node defines evidence inputs, exact capability, dependencies, output schema, `R0–R3` risk, required validation level, falsifier and fallback.

A fixed seven-role pipeline is deliberately not required. Role separation is used where it increases independence, but the dynamic planner should avoid ceremony, information loss and duplicated review work when fewer bounded nodes can prove the same result.

## Parallelism

Parallel specialist work is allowed only for independent read-only questions. Shared-state writes, test mutations and production actions are serialized. The verifier reads original evidence directly rather than trusting synthesis alone.

## Truth model

Tool output, code findings and official documentation have provenance but different evidentiary roles. Documentation can establish a mechanism; case evidence must establish that the mechanism actually consumed the user's record. External plugin output is never exempt from Gate 7.

A reviewer label such as `critical` or a clean static-analysis/build result is also not case truth. Review findings must be reproduced or linked to evidence; lower validation levels cannot replace runtime or business/accounting validation when those levels are required. A derived artifact without a closed source lineage, or a result from a stale execution identity, is likewise insufficient.

Gate status and claim status are independent. Gate 6/7 may pass by correctly establishing insufficiency or rejecting a hypothesis. A claim can be established only to the exact extent directly supported by its Evidence IDs.

## Visual Explanation seam

Visual Explanation has one narrow interface: requested `mode` plus the passed Gate 6 claim/evidence ledger and the passed Gate 7 review result. It returns an inline Markdown presentation only. There is no external renderer, new Gate, write surface or feedback path into diagnosis.

The interface supports exactly two modes:

- `diagram` projects reviewed claim/evidence relationships or the canonical causal stages. Every node carries its existing Claim ID/Evidence ID and final status. An open, broken or unproved transition is shown as a gap, never promoted into an edge.
- `sticky` projects compact cards for the reviewed result, decisive evidence and remaining uncertainty/falsifier. Every factual card retains existing Claim IDs, Evidence IDs and final status.

The projector cannot create or strengthen a claim, Evidence item, causal link, proof or provenance closure. Its output receives no Evidence ID and cannot support another claim. A changed source ledger invalidates the presentation; regenerate it only after the affected Gate 6/7 work is repeated.

The sidecar runs only for an explicitly requested normal narrative response after Gate 6 and Gate 7 pass. If either prerequisite is absent, the presentation is omitted without blocking or reopening a Gate. Literal `EVAL_RESULT_JSON` disables it unconditionally because the supplied strict skeleton is the entire allowed output.

## Publication integrity

Current-tree cleanliness is necessary but not sufficient for a public diagnostics repository. Deleting a confidential artifact from the current tree does not remove it from Git history. CI therefore uses a full checkout and a separate publication validator that:

- proves the `git archive HEAD` file set matches the tracked release tree;
- scans historical paths for prohibited database/backups, private keys, environment files and case data;
- scans manageable historical text blobs for plaintext credential assignments and user-machine absolute paths;
- fails rather than claiming a history-safe release when the checkout is shallow.

This complements GitHub secret scanning/push protection; it does not replace provider-side security controls or independent rights/privacy review.

## Failure model

- missing optional capability → documented fallback;
- missing required capability → dependent node/Gate `blocked`;
- internal reasoning/skill/role emitted as a synthetic capability → strict eval failure;
- declared synthetic capability omitted or status changed → strict eval failure;
- supplied material evidence not reliably inspected → Gate 2 blocked for affected conclusions;
- material derived evidence has no parent/transformation anchor → provenance `broken`, dependent source/cause conclusion blocked;
- executable result no longer matches current case/input identity → evidence/Gate `stale` until rerun/equivalence proof;
- narrow evidence-sufficiency goal completed but linked incident unresolved → current goal closed, linked incident blocked/open;
- contradicting tool results → preserve both, compare inputs/versions/run identity/scope, never vote by majority;
- unapproved `R3` action → stop before execution;
- required higher-level validation unavailable → block rather than promote a lower-level check;
- invalid/incomplete/expectation-contaminated runtime run → release acceptance blocked;
- shallow Git history or unsafe historical residue → publication integrity blocked;
- escaped defect/material omission → strengthen earliest applicable gate/eval;
- new evidence → reopen from earliest affected gate.
