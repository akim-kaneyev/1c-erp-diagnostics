# v0.4.1 — Unica compatibility and Windows updates

Updates the reviewed Unica companion to 0.13.0 and separates catalog refresh from installed-plugin refresh on Windows. A running bootstrap may lock an unchanged version directory; the documented flow skips identical files and installs changed versions separately. Saved enabled flags and current sessions are preserved. Fresh tasks load the updated MCP schemas.

The viewer app is rebuilt with the matching 0.4.1 version and unchanged behavior/approved Velis assets. The diagnostic plugin is 0.4.1. The 35-skill contract, Gate 0–10, EVAL_RESULT_JSON, immutable evidence and five-plugin marketplace remain in place. No 1C bridge, database mutation or permission widening is added.

## Reviewed external sources

- Unica 0.13.0: `IngvarConsulting/unica-marketplace`, `885ca40dffd127dc29715f637d2ebdd7846b8b6e`, LGPL-3.0-or-later. The official promotion points to Unica source `ee118d78cd4c6fc2df50e68c42a4eddfe4c3401a`. Its migration/fresh-install Windows CI passed. Public tool contracts include schema/dry-run and metadata-edit migrations; discover actual current tools.
- 1C Skills PowerShell: `8cb7868145281d8e353831512cc1ffa72f1b5c89`.
- 1C Skills Python: `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.
- Optional Jev: `cf7e76607d4ec70592b24becadd0296dcda8177a`.

## Acceptance

Required CI/CodeQL, exact installed-package and 26-case clean-session evidence must pass before merge. Fresh Codex skill discovery and public Unica MCP calls use synthetic local files, separately from any live accounting acceptance. Results and immutable identities are recorded on the PR; source review or an HTTP response alone cannot establish business correctness.

Use the [Windows update procedure](PLUGIN_UPDATES.md). Roll back the reviewed marketplace/package version through Codex and start a fresh task. Existing databases and the deferred 1C bridge are outside this release.
