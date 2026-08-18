# Installation

## Global Codex skill

Codex can use user-level skills under `$HOME/.agents/skills`.

### Windows PowerShell

From a clone of this repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\install\install-codex-skill.ps1
```

For a private repository, `git clone` must already be authenticated for GitHub.

Expected installed path:

`%USERPROFILE%\.agents\skills\one-c-erp-diagnostics\SKILL.md`

Restart Codex, then test:

`$one-c-erp-diagnostics Проверь тестовый кейс и покажи Gate 1-10`

### Linux/macOS

```bash
bash ./install/install-codex-skill.sh
```

Expected path:

`$HOME/.agents/skills/one-c-erp-diagnostics/SKILL.md`

## ChatGPT

A GitHub repository is not automatically visible to unrelated ChatGPT chats.

If Personal Skills are available for the account:

1. Open `Plugins` in ChatGPT.
2. Open the `Skills` tab.
3. Choose Create/Upload (or Create with editor).
4. Install the portable skill from `skills/one-c-erp-diagnostics/`.
5. Personal Skills must be installed separately on desktop and web/mobile; they do not automatically sync between those surfaces.

In ChatGPT, explicitly invoke an installed plugin/skill with `@`, not `$`.

## Verification

Installation is not complete until a fresh Codex project recognizes `$one-c-erp-diagnostics` and returns Gate 1-10 statuses instead of treating it as plain text.
