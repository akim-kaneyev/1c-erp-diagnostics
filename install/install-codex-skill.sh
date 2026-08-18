#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-https://github.com/akim-kaneyev/1c-erp-diagnostics.git}"
BRANCH="${2:-main}"
SKILL="one-c-erp-diagnostics"
TARGET_ROOT="$HOME/.agents/skills"
TARGET="$TARGET_ROOT/$SKILL"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Installing $SKILL to $TARGET"
git clone --depth 1 --branch "$BRANCH" "$REPO" "$TMP/repo"
mkdir -p "$TARGET_ROOT"
rm -rf "$TARGET"
cp -R "$TMP/repo/skills/$SKILL" "$TARGET"

echo "Installed: $TARGET"
echo "Restart Codex, then invoke: \$one-c-erp-diagnostics <task>"
