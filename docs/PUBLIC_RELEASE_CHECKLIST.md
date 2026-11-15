# Public release checklist — v0.4.1

## Repository and package

- [x] Unica 0.13.0 is pinned to canonical marketplace commit `885ca40dffd127dc29715f637d2ebdd7846b8b6e`.
- [x] Versioned provenance and LGPL-3.0-or-later boundary are documented; external implementation is not copied.
- [x] Windows update procedure separates catalog refresh from replacing a running unchanged cache.
- [x] Five plugin identities, 35 primary skills, Gate 0–10, EVAL_RESULT_JSON and Velis assets are retained.
- [ ] Pass public-package, skill governance, deterministic lock, ecosystem and full-history validators.
- [ ] Pass Python 3.10/3.12 regressions and unchanged frontend typecheck/tests/reproducible build.
- [ ] Confirm required protected PR checks and CodeQL before merge.

## Exact installed acceptance

- [ ] Confirm actual installed primary 0.4.1 and Unica 0.13.0 files match reviewed source hashes.
- [ ] Confirm both saved enabled flags and user-scope skills in separate workspaces.
- [ ] Start a fresh host; enumerate Unica 0.13.0 MCP schemas and exercise offline synthetic operations.
- [ ] Execute all 26 clean diagnostic sessions against exact installed 0.4.1, then strictly validate logs/manifests.
- [ ] Confirm main has the accepted tree and the final GitHub installation has the same package hashes.
- [ ] Keep the existing viewer 0.4.0 asset identity and its UI acceptance separate from primary versioning.

## Public presentation and release

- [ ] Reconfirm Repository visibility is Public and Private vulnerability reporting is enabled.
- [ ] Publish a focused PR and merge only after its required checks and acceptance pass.
- [ ] Record final installation and main CI; preserve accepted-source evidence after squash merge.
- [ ] Create a tag/release or global Plugin Directory publication only through its separate supported flow when in scope.

## Stop condition

Do not merge or claim current acceptance while a critical package check fails, CI/CodeQL is incomplete, a reviewed source mismatch remains or current installed/runtime evidence is absent. Historical runs cannot accept changed bytes. Version 0.4.0 acceptance at `dd351682e6eb14520308824d2b0e7e44323dae88` is preserved as historical evidence only.

No bridge 1С, connection probe, configuration update, document posting or live business-accounting test is included. Offline XML and synthetic fixtures verify the declared integration scope.
