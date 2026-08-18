---
name: one-c-erp-diagnostics
description: Run the mandatory evidence-first Gate 1-10 workflow for 1C:ERP incidents involving movements, registers, postings, month close, cost, expenses, settlements, VAT, warehouse/series/assignments, production, or access rights. Use when the user needs a verified cause, comparison, correction plan, or safe next action.
---

# 1C ERP Diagnostics — Codex entrypoint

This is the repository-discoverable entrypoint for `$one-c-erp-diagnostics`.

## Mandatory startup

1. Read repository-root `AGENTS.md`.
2. Read repository-root `SKILL.md`; it is the authoritative Gate 1-10 orchestrator.
3. If the case has `STATE.md`, resume from the earliest gate that is pending, failed, blocked, or stale.
4. Use repository-root `playbooks/router.md` to select the primary playbook.
5. Execute repository-root `skills/diagnose-1c-erp/SKILL.md` plus the selected playbook.
6. Run repository-root `prompts/verify-conclusion.md` as the independent verification gate before any final `УСТАНОВЛЕНО` status.

## Path rule

All supporting files referenced above are relative to the repository root, not to this skill directory.

## User contract

The user should only need to invoke:

`$one-c-erp-diagnostics <task or case path>`

Do not ask the user to manually chain internal skills, prompts, playbooks, tools, or validators.

## Hard stop

If a required evidence source, connector, plugin, sandbox, or independent verification capability is unavailable, mark the affected gate blocked/ТРЕБУЕТ ПРОВЕРКИ. Never simulate a completed verification.
