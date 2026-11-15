# Updating the two installed plugins on Windows

The primary plugin and Unica remain independently installed under the stable `one-c-erp-diagnostics-marketplace` identity. Version 0.4.1 pins Unica 0.13.0 to the official marketplace commit `885ca40dffd127dc29715f637d2ebdd7846b8b6e`.

## Why access can fail

Windows may refuse a backup/rename of an installed version directory while that version's MCP bootstrap is running. A user who already has full control of the directory does not need an ACL change. A catalog refresh that automatically reinstalls every configured plugin can therefore fail on an unchanged running Unica version.

## Update without replacing unchanged running files

Run from a normal project or user directory outside the plugin cache:

```powershell
codex.exe -c plugins={} plugin marketplace upgrade one-c-erp-diagnostics-marketplace --json
codex.exe plugin list --marketplace one-c-erp-diagnostics-marketplace --available --json
```

The first command uses a supported configuration override for that invocation only: its empty plugin map lets the Git catalog refresh without automatically refreshing configured installed plugins. It does not disable plugins in the saved configuration. Verify both saved enabled flags afterwards. Inspect the offered and installed versions in the second command before installing anything.

For each changed version, install that exact plugin through the supported CLI:

```powershell
codex.exe plugin add one-c-erp-diagnostics@one-c-erp-diagnostics-marketplace --json
codex.exe plugin add unica@one-c-erp-diagnostics-marketplace --json
```

Run only the relevant install command when that plugin changed. If the same version is already installed and its files match the reviewed source, leave its running cache in place. New versions use separate version directories. A forced repair of an identical version requires first closing the affected host MCP sessions through their normal lifecycle; do not kill 1C, delete a live cache, broaden ACLs or edit the installed vendor package.

Open a new Codex task after an update so its MCP server and tool schemas come from the new version. Preserve the existing task history. Verify installed manifest versions, file hashes, both enabled flags, user-scope skill discovery and fresh-host MCP startup with offline synthetic inputs. A successful install does not attest a live 1C database or a business-accounting result.

## Acceptance scope and rollback

The primary app and diagnostic plugin both report 0.4.1. The viewer is rebuilt with the matching version and retains its behavior. UI acceptance and 1C runtime acceptance remain separate. The 1C HTTP test bridge is not installed or started by this update.

Rollback restores the prior reviewed marketplace pin and primary package through the same supported install flow and starts a fresh task. Do not modify the user's database, credentials, licenses or companion configuration to make an update pass.
