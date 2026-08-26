# 1C toolchain discovery and candidate intake

## Purpose

This document turns external technology maps into a controlled candidate queue. A catalog entry is discovery evidence only. It is not proof of security, compatibility, installation, runtime availability or suitability for a specific 1C:ERP incident.

## Reviewed discovery sources

### Infostart technology map

- article: `https://infostart.ru/1c/articles/2772307/`;
- title: `Современный инструментарий 1Сника`;
- publication date: `2026-08-25`;
- role: broad map of 1C development, testing, integration, delivery, monitoring and prototyping technologies;
- adoption status: methodology/discovery only; article text and images are not copied into this repository.

The map is useful for identifying candidate classes such as EDT, Git, BSL static analysis, YAxUnit, Vanessa Automation, Docker, message brokers, monitoring/logging and interface prototyping. Each concrete product still requires independent review.

### StackTechnologies1C

- source: `https://github.com/Oxotka/StackTechnologies1C`;
- reviewed commit: `82a7b4c16f0dab0264ddd664b741019ce60aba81`;
- license: MIT;
- role: maintained 1C technology catalog and learning map;
- adoption status: discovery reference only; not a runtime dependency or marketplace plugin.

### RampStack skill governance

- source: `https://github.com/rampstackco/claude-skills`;
- reviewed commit: `0479242522549dfdb389bb9b7807ad4d6016ffb7`;
- license: MIT;
- role: methodology reference for uniform skill structure, reference separation, deterministic lock files and CI linting;
- adoption status: project-specific implementation in `tools/validate_skills.py`, `tools/update_skill_lock.py` and `docs/SKILL_AUTHORING_STANDARD.md`; the external catalog and its 103 skills are not bundled.

## Candidate record

Every candidate must record:

| Field | Required meaning |
|---|---|
| Candidate ID | Stable local identifier |
| Source/revision | Repository or official source plus immutable tag/commit when possible |
| License | Exact license and redistribution obligations |
| Problem solved | Specific 1C scenario, not a generic capability claim |
| Inputs/outputs | File formats, APIs, reports and retained state |
| Execution surface | Read-only, local derived output, test write or production/external write |
| Risk | `R0`, `R1`, `R2` or `R3` |
| Proof boundary | What the result proves and cannot prove |
| Data destination | Local, loopback, sandbox or external service |
| Authentication | Required credentials and least-privilege boundary |
| Validation | Sanitized test and independent acceptance evidence |
| Fallback/rollback | Safe alternative and removal path |
| Status | `candidate`, `reviewed_methodology`, `runtime_adapter`, `marketplace_companion`, `rejected` or `prohibited` |

## Admission gates

A candidate becomes a runtime adapter or marketplace companion only after:

1. source and maintainer verification;
2. license review;
3. immutable revision selection;
4. minimal permission and data-flow analysis;
5. sanitized deterministic tests;
6. `R0–R3` classification;
7. explicit proof limitations;
8. fallback and rollback;
9. green repository CI and adversarial review;
10. clean-session/runtime verification when the installed plugin behavior changes.

## Current integration decision

The reviewed sources add governance and discovery, not new runtime breadth:

- marketplace composition remains exactly `one-c-erp-diagnostics`, `unica`, `1c-skills`, `1c-skills-py`;
- no RampStack marketing/web skill is packaged;
- no StackTechnologies1C content or image is vendored;
- no new MCP server, backend, credential or production write is introduced;
- existing Gate 0, evidence, provenance, execution-identity and `R0–R3` controls remain authoritative.

This boundary prevents routing ambiguity while allowing the project to learn from broader engineering practice.
