# 1C ERP Diagnostics v0.3.9 — Installed-package Resource Closure

## Summary

Version 0.3.9 fixes a distribution defect discovered after v0.3.8: `one-c-erp-case-state` referred to the repository-root `templates/case/STATE.json`, but that file was outside the installable plugin directory. Repository tests passed because they read the checkout root; an installed plugin could not access the template it documented.

Final pre-PR review found the same escaped dependency shape in `one-c-erp-artifact-extraction`: an inline path referred to the repository-root extraction adapter. The candidate now packages that adapter with the owning Skill, rejects unlinked descriptive resource paths and validates fenced-command paths against the owning Skill and plugin boundary.

## Changes

- bundled the empty machine-state template at `plugins/one-c-erp-diagnostics/skills/one-c-erp-case-state/assets/STATE.json`;
- linked the bundled asset from the owning `SKILL.md` and state-integrity reference;
- required the packaged template in public-release validation;
- added a regression that compares the packaged asset with the canonical repository template;
- bundled the artifact extraction adapter with its owning Skill and linked that packaged copy;
- added regressions that reject unlinked descriptive paths, reject invalid packaged command paths and compare the packaged adapter with its canonical repository tool;
- added package-resource closure to the skill-authoring, publishing and self-audit contracts;
- retained the v0.3.8 accounting/state behavior, strict `EVAL_RESULT_JSON` contract, 26-case suite, four-plugin marketplace and approved Velis assets.

The companion identities are unchanged: Unica `aefc880f9bab606a5c55ed11af563b740054a549`, 1C Skills PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`, and 1C Skills Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Release boundary

The verified v0.3.8 clean-session run is historical evidence only. Because v0.3.9 changes installed contents, exact-version runtime acceptance remains blocked until the installed public v0.3.9 package passes the complete 26-case hash-manifest run.

Repository validation, Python 3.10/3.12 checks, protected Pull Request CI and CodeQL must pass independently before merge. Merge, tag, release and Plugin Directory publication are not claimed by these notes.
