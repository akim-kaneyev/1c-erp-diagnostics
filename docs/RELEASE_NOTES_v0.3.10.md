# 1C ERP Diagnostics v0.3.10 — Incident Discovery and Companion Provenance

## Summary

Version 0.3.10 adds a bounded incident-discovery path without treating public web material as case evidence. It also updates the reviewed Unica source and exposes Jev as an optional, independently installed browser-action companion.

## Changes

- Added `one-c-erp-incident-search` and a packaged standard-library bridge for the public Infoblog title index.
- Fixed the source to `https://infoblog.mywebguide.ru/data/search.json`; requests are HTTPS GET only, redirects are rejected and user query terms are not transmitted.
- Added media-type, response-size and compact-schema validation plus ETag, Last-Modified, retrieval timestamp and payload SHA-256 provenance.
- Made caching opt-in. Conditional requests revalidate cached data; explicit offline use is marked `stale_unverified`; network failure never silently falls back to stale data.
- Kept article bodies outside the repository. Returned titles and links are non-authoritative leads that require selected-page review, official-source verification and primary case evidence.
- Updated Unica to canonical marketplace release `v0.12.3`, commit `c02e38d44a7dc238310172b9d790487f81aa4fb4`, path `plugins/unica`.
- Added optional Jev browser use `0.1.0` at commit `cf7e76607d4ec70592b24becadd0296dcda8177a`. Jev remains a separate MIT-licensed plugin; it requires Node.js 22+, Codex CUA and an explicitly accepted external model provider/data destination.
- Limited Jev to reviewed mechanical browser actions. It does not type, establish 1C semantics or verify its own result, and it is not used by the deterministic Infoblog bridge.
- Expanded the stable marketplace from four to five entries and the primary plugin from 32 to 33 packaged skills.
- Clarified the rendered `settlements-chronology` contract after clean-session runtime checks exposed an ambiguous current-goal boundary: locating the first visible difference remains intermediate while the consuming mechanism is unproved, so the read-only case stays `R0 + EVIDENCE_REQUIRED`, Gate 7 passes by rejecting causality, Gate 10 remains blocked and claims remain below `УСТАНОВЛЕНО`.
- Clarified the equivalent `warehouse-first-divergence` boundary after the resumed clean-session run reproduced the same ambiguity: the visible series difference is established only as an intermediate localization, while the causal goal and linked incident stay blocked until a consuming mechanism is evidenced.
- Clarified the `post-item-expenses` bounded evidence-assessment boundary after a clean-session response promoted two supplied input facts into established claims: Gate 10 closes only the sufficiency assessment, while the setting-to-result hypothesis and linked incident remain unproved and require non-established claims.
- Reproduced the same contract defect in `production-chain-gap`, where a clean-session response emitted two `УСТАНОВЛЕНО` input-fact claims although the case permits none. The suite now rejects any zero-established case whose rendered prompt does not disclose that boundary.
- Aligned the seven remaining affected prompts (`access-rights-no-broad-grant`, `adversarial-missing-mechanism`, `production-chain-gap`, `scoped-r3-mass-repost`, `sonarqube-static-finding-no-runtime`, `unavailable-required-capability` and `vat-date-separation`) with their existing expectations. This is prompt disclosure only: expected statuses, risks, decisions, evidence and acceptance limits are unchanged.
- Reproduced a separate encoding defect in the externally isolated `six-row-balanced-fallback` case: the arithmetic was correct, but the runner emitted `A=20,B=90,residual=0` and `0` where the validator requires canonical allocation and boolean marker forms. The shared semantic prompt now defines canonical value encodings for all ten marker cases while continuing to hide their expected values.
- Preserved the strict `EVAL_RESULT_JSON` suite, approved Velis assets and existing Gate 0–10 controls.

Unchanged immutable companions:

- 1C Skills PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Release boundary

Repository validation, protected Pull Request CI, CodeQL, merge, tag/release and installed-runtime acceptance are separate claims. This candidate must not be described as runtime-accepted until exact installed v0.3.10 completes the full 26-case clean-session run and `tools/validate_runtime_run.py` validates its hash manifest.

The historical v0.3.8 run and repository-local tests do not accept the changed package. Jev live provider/browser behavior and installed Unica execution also require host-side confirmation.
