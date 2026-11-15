# Plugin self-audit — 0.4.1

Scope: official Unica 0.13.0 pin, Windows cache-safe update procedure and unchanged local viewer 0.4.0. External implementation remains externally installed and LGPL-3.0-or-later; none is vendored into this MIT plugin.

Reviewed source: `IngvarConsulting/unica-marketplace` at `885ca40dffd127dc29715f637d2ebdd7846b8b6e`; version, license, source commit, runtime manifest and successful official Windows fresh-install/upgrade checks were examined on 2026-11-15. A fresh host must verify the installed public MCP schemas and runtime-file hashes before functional claims.

Runtime behavior: the catalog-only command uses an invocation-scoped `plugins={}` override. It does not persistently disable either plugin or change filesystem ACLs. Targeted installation of a changed version uses the supported Codex CLI. Existing running cache directories remain intact. Both enabled flags must be checked after the operation.

Preserved controls: Gate 0–10, R0–R3, adversarial review, row/value boundaries, credential protection, strict 26-case EVAL_RESULT_JSON, user-owned Velis branding, five-plugin catalog and immutable companion identities. The audit skill now refers to the canonical recorded pin instead of a stale hard-coded release.

No known critical control failure is claimed as a final audit result until required CI/CodeQL, full regression, installed-source identity, fresh MCP and exact-version runtime acceptance pass. Their outcomes belong on the PR, not as invented acceptance in this audit. Unresolved live accounting acceptance and the deferred 1C bridge remain separate.
