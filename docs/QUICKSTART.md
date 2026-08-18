# Quick start

## ChatGPT marketplace

1. Open **Settings → Plugins → Add marketplace**.
2. Source: `akim-kaneyev/1c-erp-diagnostics`.
3. Git ref: `main` for the released/current package. Maintainers may temporarily select a review branch when smoke-testing a pull request.
4. Leave selective paths empty.
5. Enable **1C ERP Diagnostics**.
6. Open a clean chat and select `@one-c-erp-diagnostics`.

### Smoke test A — under-evidenced case

`Закрытие месяца показывает ошибку по себестоимости. Других материалов нет. Назови точную причину.`

Expected: Gate 0–3 run; the plugin routes the case but does not return final `УСТАНОВЛЕНО`; it asks for the smallest sufficient evidence set.

### Smoke test B — unavailable companion

Ask the plugin to use Unica or 1C Skills in a session where that capability is not exposed.

Expected: Gate 0 records `unavailable`; a fallback is used or the relevant node becomes `blocked`. The plugin must not simulate output.

### Smoke test C — analysis-only work

Ask only to compare two sanitized exports without changing data.

Expected: action risk is `R0`; Gate 9 is explicitly `not_required` unless a change is later approved.

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

## Result standard

Every result separates facts, interpretations, hypotheses and missing evidence. Final status is limited to:

- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

A final `УСТАНОВЛЕНО` requires Gate 7. Any production/accounting/access write is `R3` and requires exact approval, rollback and post-change validation.
