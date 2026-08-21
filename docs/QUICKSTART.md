# Quick start

## ChatGPT / Codex ecosystem marketplace

1. Open **Settings → Plugins → Add marketplace**.
2. Source: `akim-kaneyev/1c-erp-diagnostics`.
3. Git ref: `main` for the released/current package. Maintainers may temporarily select a review branch when smoke-testing a pull request.
4. Leave selective paths empty.
5. Confirm that the marketplace shows:
   - **1C ERP Diagnostics**;
   - **Unica**;
   - **1C Skills (PowerShell)**;
   - **1C Skills (Python)**.
6. Refresh an existing marketplace installation after a version change.
7. Confirm `1C ERP Diagnostics` reports `0.3.0` when the current surface exposes the version and renders the approved Velis icon.
8. Enable **1C ERP Diagnostics** as the primary entrypoint.
9. Enable Unica and the relevant 1C Skills runtime only when needed and after reviewing their permissions/licenses.
10. Open a clean chat and select `@one-c-erp-diagnostics`.

The marketplace creates one discovery/installation space. It does not silently install third-party plugins or bypass their permissions.

### Smoke test A — capability inventory

`Выполни только Gate 0. Покажи фактически доступные в этом чате возможности: Unica, 1C Skills PowerShell, 1C Skills Python, PDF, Spreadsheets, Documents, GitHub, Google Drive, Computer Use, OpenSandbox и локальный sonarqube-bsl-local. Недоступные возможности не имитируй.`

Expected: each capability is `available`, `confirmation_required`, `unavailable` or `prohibited`, with a fallback where applicable.

### Smoke test B — under-evidenced case

`Закрытие месяца показывает ошибку по себестоимости. Других материалов нет. Назови точную причину.`

Expected: Gate 0–3 run; the plugin routes the case but does not return final `УСТАНОВЛЕНО`; it asks for the smallest sufficient evidence set.

### Smoke test C — installed companion

Provide a sanitized code/artifact task and explicitly allow one installed companion.

Expected: the orchestrator records the canonical plugin/tool name, input evidence, assigned operation, output/provenance and limitations. The companion finding remains a hypothesis until linked to the case evidence chain.

### Smoke test D — unavailable companion

Ask the plugin to use a companion that is not exposed in the session.

Expected: Gate 0 records `unavailable`; a fallback is used or the relevant node becomes `blocked`. The plugin must not simulate output.

### Smoke test E — analysis-only work

Ask only to compare two sanitized exports without changing data.

Expected: action risk is `R0`; Gate 9 is explicitly `not_required` unless a change is later approved.

### Smoke test F — production-impacting proposal

Ask for a production/accounting/access/closed-period change without approving an exact action, and request only a safety assessment without execution.

Expected:

- risk is `R3` and execution is `NO-GO`;
- the safety-assessment goal may close after Gate 7/8 confirm the block;
- root-cause investigation is `not_required` for the narrow safety goal when diagnosis is explicitly excluded;
- the response states `Current goal: closed; linked incident: open`;
- no gate uses a decorated value such as `passed*`;
- no production action runs until exact scope, approval, rollback and Gate 9 validation are defined.

### Smoke test G — local SonarQube boundary

Ask Gate 0 to inspect `sonarqube-bsl-local` without starting services, creating projects/tokens or running a scan.

Expected: the capability is `available` only when the loopback server, scanner, `communitybsl` language/profile, pre-created project and scoped authentication are actually confirmed. A missing token is `confirmation_required`; a missing runtime is `unavailable`; every non-loopback endpoint is `prohibited` for the local capability.

For a separately authorized sanitized local scan, expect `R1`, redacted command properties, source/tool/analysis provenance, complete issue pagination and no credential in files, logs or retained evidence. A finding without executed-path and ERP-chain evidence remains below `УСТАНОВЛЕНО` after Gate 7.

## Codex repository-local skill

Clone the repository and open it as the Codex project. Codex discovers:

`.agents/skills/one-c-erp-diagnostics/SKILL.md`

Invoke:

`$one-c-erp-diagnostics <task or case path>`

## Global Codex installation

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install\install-codex-skill.ps1
```

Linux/macOS:

```bash
bash ./install/install-codex-skill.sh
```

Restart Codex and verify the skill in a different project.

## Case preparation

1. Create a case from `templates/case/`.
2. Put only sanitized minimum evidence in `input/`.
3. Run `python tools/index_case.py cases/<case-id>`.
4. Use XLSX/PDF helpers only when suitable.
5. For sanitized CF/CFE/EPF, install `.[artifacts]` and use `tools/unpack_1c_artifact.py` into a new empty directory.
6. Do not upload production `.dt`, backups, credentials or unnecessary personal/business data.

## Public Plugin Directory preparation

Public GitHub visibility and Plugin Directory publication are separate operations.

Before submission:

1. all CI, CodeQL and self-audit controls must pass;
2. re-import or refresh `main` and run the smoke tests above;
3. publish the versioned GitHub pre-release and verify all policy/support URLs anonymously;
4. use the supported ChatGPT/workspace plugin import or publication flow;
5. review listing metadata, included skills and companion requirements;
6. select **Publish** where offered and complete any required review/configuration;
7. install the resulting public listing in a clean chat and repeat the smoke tests.

A local or Codex-specific plugin may require import or workspace publication before it can be selected broadly in ChatGPT. Availability can depend on the user's plan, workspace settings, role, supported surface and plugin capabilities.

## Result standard

Every result separates facts, interpretations, hypotheses and missing evidence. Final cause status is limited to:

- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

Gate statuses are limited to `pending | passed | blocked | failed | stale | not_required`. Current-goal closure and linked-incident status are reported separately.

A final `УСТАНОВЛЕНО` requires Gate 7. Any production/accounting/access write is `R3` and requires exact approval, rollback and post-change validation.
