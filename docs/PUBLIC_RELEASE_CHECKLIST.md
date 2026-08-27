# Public release checklist — v0.3.9 installed-package resource closure candidate

## Repository and plugin package

- [x] Dynamic Gate 0–10, Gate 7, Gate 9, Gate 10 and `R0–R3` contracts remain present.
- [x] The package contains 32 reviewed skills and the four-plugin marketplace identity is unchanged.
- [x] Accounting, state, artifact-view and credential controls from v0.3.8 remain in the 26-case suite.
- [x] The case-state template is bundled at `plugins/one-c-erp-diagnostics/skills/one-c-erp-case-state/assets/STATE.json`.
- [x] The packaged template is linked from the owning skill and reference, so normal local-link validation covers it.
- [x] A regression requires the packaged template to exist and equal the canonical repository template.
- [x] Public-release validation explicitly requires the packaged template.
- [x] The deterministic skill lock covers the packaged asset.
- [x] The artifact extraction adapter is bundled with its owning Skill and equals the canonical repository tool.
- [x] Packaged runtime paths must be Markdown links, so repository-root dependencies cannot bypass boundary validation.
- [x] The self-audit and authoring standard forbid repository-root resources from satisfying installed-package dependencies.
- [x] Plugin manifest, `pyproject.toml`, active documentation and validator expectations declare `0.3.9`.
- [x] v0.3.9 release notes and self-audit exist without claiming pending external checks as complete.
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

- [x] Historical v0.3.8 public-install run passed all 26 cases with a valid hash manifest for merge commit `826aae46ed278e42c182c1be3e3c93cc2a53766c`.
- [ ] Refresh/re-import the marketplace and confirm exact installed version `0.3.9` when exposed.
- [ ] Confirm the bundled `one-c-erp-case-state/assets/STATE.json` is readable from the installed package.
- [ ] Execute every case from `evals/suite.json` in separate clean sessions against exact installed v0.3.9.
- [ ] Pass `tools/validate_runtime_run.py` for the complete v0.3.9 hash manifest.
- [ ] Re-run the canonical accounting helper baseline/patch comparison and record current helper/input/result hashes.

The v0.3.8 runtime run does not accept v0.3.9 because the installed package contents changed.

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

Do **not** merge, tag, release or claim v0.3.9 runtime acceptance while any critical package/resource check fails, required CI/CodeQL is incomplete, the exact installed version is not confirmed, or the complete v0.3.9 clean-session run is absent. Repository validation and historical v0.3.8 evidence do not substitute for exact-version runtime evidence.
