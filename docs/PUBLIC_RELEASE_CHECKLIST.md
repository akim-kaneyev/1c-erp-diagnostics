# Public release checklist — v0.4.0 local viewer candidate

## Repository and plugin package

- [x] Dynamic Gate 0–10, Gate 7, Gate 9, Gate 10 and `R0–R3` contracts remain present.
- [x] The package contains 35 reviewed skills and the stable marketplace identity exposes five independently installable plugins.
- [x] Accounting, state, artifact-view and credential controls from v0.3.8 remain in the 26-case suite.
- [x] The case-state template is bundled at `plugins/one-c-erp-diagnostics/skills/one-c-erp-case-state/assets/STATE.json`.
- [x] The packaged template is linked from the owning skill and reference, so normal local-link validation covers it.
- [x] A regression requires the packaged template to exist and equal the canonical repository template.
- [x] Public-release validation explicitly requires the packaged template.
- [x] The deterministic skill lock covers the packaged asset.
- [x] The artifact extraction adapter is bundled with its owning Skill and equals the canonical repository tool.
- [x] Descriptive packaged runtime paths must be Markdown links; fenced-command paths must resolve from the owning Skill inside the plugin boundary.
- [x] The self-audit and authoring standard forbid repository-root resources from satisfying installed-package dependencies.
- [x] The Infoblog bridge is fixed-origin, metadata-only, locally searched, bounded and fail-closed; cache freshness and payload provenance are explicit.
- [x] Unica is pinned to the canonical marketplace commit for `v0.12.3`.
- [x] Jev is optional, immutable-pinned, not vendored and documented with its CUA/provider/data-transfer boundary.
- [x] Plugin manifest, `pyproject.toml`, active documentation and validator expectations declare `0.4.0`.
- [x] v0.4.0 release notes and self-audit exist without claiming pending external checks as complete.
- [x] Confirm the final branch diff contains no unrelated files or local runtime evidence.

## Repository validation

- [x] Pass public-package validation.
- [x] Pass skill governance and deterministic lock validation.
- [x] Pass full-history publication validation.
- [x] Pass ecosystem marketplace validation.
- [x] Pass the 26-case eval specification validator.
- [ ] Pass all unit/regression tests on Python 3.10 and 3.12.
- [x] Run the system skill `quick_validate.py` in an environment with PyYAML available.
- [ ] Confirm required protected Pull Request checks and CodeQL are green.

## Runtime acceptance

- [x] Historical v0.3.11 accepted source `13e5d9b09b09028985bfd439eca045de7f6a567d` passed all 26 cases; merged main `d69db19504e7525ea1c1e95146c3b2070ab8b5f0` has the identical tree (PR #41).

- [x] Historical v0.3.8 public-install run passed all 26 cases with a valid hash manifest for merge commit `826aae46ed278e42c182c1be3e3c93cc2a53766c`.
- [ ] Refresh/re-import the marketplace and confirm exact installed version `0.4.0` when exposed.
- [ ] Confirm the bundled `one-c-erp-case-state/assets/STATE.json` is readable from the installed package.
- [ ] Execute every case from `evals/suite.json` in separate clean sessions against exact installed v0.4.0.
- [ ] Pass schema-2 `tools/validate_runtime_run.py` for the complete v0.4.0 external run with exact plugin mention, no model tools, current source/plugin-tree identity and per-case result/log hashes.
- [ ] Re-run the canonical accounting helper baseline/patch comparison and record current helper/input/result hashes.

The v0.3.8 runtime run does not accept v0.4.0 because the installed package contents changed.

## GitHub identity, security and presentation

- [x] Repository visibility is Public.
- [x] README, license, policies, support files and approved Velis assets are present.
- [x] Private vulnerability reporting is enabled.
- [x] Dependency graph, secret scanning and push protection were confirmed for the prior release.
- [ ] Reconfirm protected-branch rules, security settings and public URLs before publication.

## Publication

- [ ] Open a focused protected Pull Request from the approved branch.
- [ ] Merge only after every required repository and CodeQL check passes.
- [ ] Create tag/release only after merged `main` is revalidated.
- [ ] Publish or update the Plugin Directory only through the supported product flow.
- [ ] Repeat exact-version clean-session acceptance after installation from the public distribution surface.

## Stop condition

Do **not** merge, tag, release or claim v0.4.0 runtime acceptance while any critical package/resource check fails, required CI/CodeQL is incomplete, the exact installed version is not confirmed, or the complete v0.4.0 clean-session run is absent. Repository validation and historical v0.3.8 evidence do not substitute for exact-version runtime evidence.

## Local test-bridge acceptance

- [ ] Confirm the exact disposable test contour and installed CFE revision separately from Health.
- [ ] Run health/metadata/query capture and offline verification with current case context.
- [ ] Reconcile independent row counts/totals on identical analytics; retain bounded-query limitations.
- [ ] Where in scope, execute report/print-form validation and inspect actual output artifacts.

Synthetic HTTP fixtures do not satisfy these live-contour checks.

## UI SDK workflow

- [x] Verify upstream source/license and installed skill hashes.
- [x] Verify global user-scope discovery in separate working directories.
- [x] Verify packaged UI skill references resolve within the plugin.
- [ ] Record the exact-version diagnostic regression and UI workflow checks separately.

Version 0.4.0 ships an actual local application. Record the frontend tests, production build, real-browser checks, installed-cache launch and exact diagnostic runtime bundle on the PR before merge. The earlier 0.3.12 run is historical evidence only. The live 1C bridge remains deferred and is outside this release's UI acceptance scope.

## Ready viewer

- [ ] Pass frontend typecheck and human/agent interaction tests.
- [ ] Pass production asset, loopback, Host/Origin and native example tests.
- [ ] Verify the committed bundle rebuilds identically in CI.
- [ ] Check desktop/mobile layout, keyboard, popup focus and actual color contrast in a browser.
- [ ] Install the candidate in Codex and launch the viewer from that installed cache.
- [ ] Confirm the final main installation matches the accepted package and build hashes.
