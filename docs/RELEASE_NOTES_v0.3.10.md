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
- Preserved the strict `EVAL_RESULT_JSON` suite, approved Velis assets and existing Gate 0–10 controls.

Unchanged immutable companions:

- 1C Skills PowerShell `8cb7868145281d8e353831512cc1ffa72f1b5c89`;
- 1C Skills Python `c1f79f5ac9f31c620b8508f75464f8c42c559ae4`.

## Release boundary

Repository validation, protected Pull Request CI, CodeQL, merge, tag/release and installed-runtime acceptance are separate claims. This candidate must not be described as runtime-accepted until exact installed v0.3.10 completes the full 26-case clean-session run and `tools/validate_runtime_run.py` validates its hash manifest.

The historical v0.3.8 run and repository-local tests do not accept the changed package. Jev live provider/browser behavior and installed Unica execution also require host-side confirmation.
