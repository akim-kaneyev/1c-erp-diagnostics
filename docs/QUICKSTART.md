# Quick start

## ChatGPT plugin marketplace

1. Open **Settings → Plugins**.
2. Choose **Add → Add marketplace**.
3. Set the source to:

   `akim-kaneyev/1c-erp-diagnostics`

4. Set Git ref to `main`.
5. Leave selective paths empty.
6. Add the marketplace and enable **1C ERP Diagnostics**.
7. In a new chat invoke:

   `@one-c-erp-diagnostics`

Recommended first safety test:

`Закрытие месяца показывает ошибку по себестоимости. Других материалов нет. Назови точную причину.`

Expected behavior: the plugin must not claim a final `УСТАНОВЛЕНО` cause without evidence. It should record the missing evidence and request the smallest sufficient data set.

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
3. Run:

   `python tools/index_case.py cases/<case-id>`

4. Use the XLSX/PDF helpers only when suitable for the supplied format.
5. Do not upload production `.dt`, backups, credentials or unnecessary personal/business data.

## Result standard

Every diagnostic result must separate facts, interpretations, hypotheses and missing evidence. Final root cause status is limited to:

- `УСТАНОВЛЕНО`;
- `ВЕРОЯТНО`;
- `ТРЕБУЕТ ПРОВЕРКИ`.

A final `УСТАНОВЛЕНО` requires the independent Gate 7 verification pass.
