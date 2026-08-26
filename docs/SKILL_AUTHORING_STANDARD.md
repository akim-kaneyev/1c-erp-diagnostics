# Skill authoring and governance standard

## Purpose

This standard keeps all `1C ERP Diagnostics` skills consistent without turning the plugin into a generic catalog. It governs structure, routing, references, synchronization and self-checking. It does not import third-party skills or change the four-plugin marketplace.

## Authority and runtime surfaces

The runtime contract has one authority and three synchronized delivery surfaces:

1. repository-root `SKILL.md` — authoritative Gate 0–10 and strict evaluation contract;
2. `plugins/one-c-erp-diagnostics/skills/one-c-erp-diagnostics/SKILL.md` — packaged plugin orchestrator;
3. `skills/one-c-erp-diagnostics/SKILL.md` — portable global skill;
4. `.agents/skills/one-c-erp-diagnostics/SKILL.md` — repository-local routing shim.

The delivery surfaces may differ in length, but they must preserve the same non-negotiable invariants: Gate 0–10, Gate 7, canonical Gate statuses, `EVAL_RESULT_JSON`, `R0–R3`, evidence/provenance rules and no simulated unavailable capability.

## Packaged skill boundary

Every packaged skill lives under:

```text
plugins/one-c-erp-diagnostics/skills/<skill-name>/SKILL.md
```

Requirements:

- folder and frontmatter `name` are identical;
- name is unique and starts with `one-c-erp-`;
- `description` states the concrete task and trigger context;
- local Markdown links resolve inside the repository;
- the skill does not declare an unavailable app, plugin, MCP server or write permission as present;
- external discovery catalogs never become marketplace entries without the separate intake process;
- final 1C causality remains governed by the evidence chain and Gate 7.

## Recommended skill structure

New or materially revised skills should use this order when applicable:

1. `## When to use`;
2. `## When NOT to use`;
3. `## Required inputs`;
4. `## The framework`;
5. `## Workflow`;
6. `## Failure patterns`;
7. `## Output format`;
8. `## Reference files`.

Existing skills are migrated gradually. Missing recommended sections are advisory warnings until a dedicated runtime-behavior release explicitly makes them mandatory. Structural errors, duplicate names, broken local links, namespace violations and lock drift fail CI immediately.

## Reference files

Use references for material that would otherwise make `SKILL.md` difficult to audit:

- templates — fillable output structure;
- checklists — executable verification sequence;
- examples — synthetic worked result;
- domain guides — deeper stable methodology.

A reference must be linked from its owning `SKILL.md`, remain inside the repository and state what it proves or controls. Real customer/company evidence is prohibited.

## Deterministic lock

`SKILLS.lock.json` records SHA-256, size and path for runtime instruction surfaces, packaged skill contents, playbooks, checklists and the case-state template.

Commands:

```text
python tools/update_skill_lock.py --write
python tools/update_skill_lock.py --check
python tools/validate_skills.py
```

Any intentional runtime-surface change must update the lock in the same Pull Request. An unexplained lock change is not approval; reviewers still inspect the source diff and runtime/eval consequences.

## Self-check sequence

Every skill or governance change follows one chain:

`inspect current contract → identify exact scope → edit → structural lint → link validation → lock check → unit/eval checks → adversarial diff review → protected Pull Request → CI/CodeQL → clean-session acceptance when runtime behavior changed`

Rules:

- do not edit protected `main` directly;
- do not combine unrelated runtime, marketplace and branding changes;
- do not bump the plugin version for repository-only governance unless packaged runtime behavior or distribution metadata changes;
- do bump the version when installed skill content, manifest metadata or runtime behavior changes;
- do not claim clean-session acceptance from repository CI alone;
- reopen the earliest affected control when a defect escapes.

## Source adaptation rule

External repositories may provide methodology, examples or candidate tools. Adoption requires source, license, immutable revision, scope, risks, tests and fallback. General principles are rewritten for this project. Third-party catalogs and skills are not copied wholesale, silently installed or added to the marketplace merely because they are useful elsewhere.
