# Plugin self-audit — v0.3.10

## Scope

The audit covers the Infoblog incident-search bridge, Unica `v0.12.3`, optional Jev at immutable commit `cf7e76607d4ec70592b24becadd0296dcda8177a`, versioned package/documentation surfaces and preservation of the existing Gate 0–10, provenance, stale-result and publication controls.

## Controls

| # | Status | Evidence | Remaining action |
|---:|:---:|---|---|
| 1 | PASS | Manifest and `pyproject.toml` declare `0.3.10`; the validator expects the same version. | None. |
| 2 | PASS | The marketplace identity is unchanged and its five-entry order is deterministic. | None. |
| 3 | PASS | Unica `v0.12.3` is sourced from `IngvarConsulting/unica-marketplace`, path `plugins/unica`, immutable commit `c02e38d44a7dc238310172b9d790487f81aa4fb4`. | Confirm installed-host execution separately. |
| 4 | PASS | Jev is referenced, not copied, under MIT at exact commit `cf7e76607d4ec70592b24becadd0296dcda8177a`. | Confirm provider/CUA behavior only with explicit consent. |
| 5 | PASS | Jev is independently installable and is not declared available merely because it appears in the marketplace. | None. |
| 6 | PASS | Jev's goal/page-snapshot/action-history data destination and independent verification requirement are documented. | None. |
| 7 | PASS | Infoblog requests use one fixed HTTPS JSON URL, GET only, no query transmission and no redirect. | None. |
| 8 | PASS | Response size, media type, UTF-8 and compact index schema are validated fail-closed. | None. |
| 9 | PASS | Source URL, retrieval mode/freshness, timestamps, ETag, Last-Modified and payload SHA-256 are returned. | None. |
| 10 | PASS | Cache is opt-in, hash-checked and atomically written; offline cache is `stale_unverified`; no silent stale fallback exists. | None. |
| 11 | PASS | Search output contains metadata/links only and is explicitly non-authoritative. | None. |
| 12 | PASS | The packaged skill forbids confidential case terms, article copying and causal promotion. | None. |
| 13 | PASS | The plugin contains 33 skills; the new runtime script is inside the installed package boundary. | None. |
| 14 | PASS | Existing Gate 0–10, R0–R3, synthetic snapshot and stale-execution contracts remain present. | None. |
| 15 | PASS | The 26-case specification remains unchanged. | Exact installed-v0.3.10 run is still required. |
| 16 | WARNING | Protected PR CI and CodeQL are external repository settings/checks and cannot be established by local files. | Confirm them on the focused Pull Request. |
| 17 | WARNING | Exact installed-v0.3.10 clean-session acceptance does not yet exist. | Run all 26 cases and validate the complete hash manifest. |
| 18 | WARNING | Live Jev provider/browser and installed Unica compatibility were not exercised in this repository-only audit. | Perform consented host smoke tests before claiming availability. |
| 19 | WARNING | Core dependencies remain broad (`openpyxl>=3.1`, `pypdf>=5`) and CI resolves their newest compatible versions; optional `v8unpack==1.2.6` and `opensandbox==0.1.14` are exact reviewed pins but are behind current upstream releases. | Keep exact adapter pins until their changed APIs are separately reviewed; add a reproducible dependency lock/minimum-and-latest matrix in a focused dependency change. |
| 20 | PASS | GitHub Actions uses least-privilege `contents: read`, full history, concurrency cancellation and SHA-pinned checkout/setup-python actions on Python 3.10/3.12. | Do not treat green historical main CI as evidence for this candidate. |
| 21 | PASS | Public GitHub API exposes an active dynamic CodeQL workflow; the latest observed run for current main commit `8ff373d` completed successfully on 2026-09-29. | Confirm CodeQL and required checks again on the candidate Pull Request; default-setup configuration details require authenticated access. |
| 22 | PASS | The local unmerged `9f01787` strict-runtime fix was reviewed. Its general nested-object contract and bounded-comparison correction were ported; case-by-case answer encoding was not imported wholesale. | Re-run exact installed evals because repository tests cannot prove model compliance. |

## Local verification

- Project suite: 158 tests passed after the final bridge hardening.
- Project validators: public release, skill governance, deterministic lock, ecosystem marketplace and 26-case eval specification passed; governance retains 256 pre-existing advisory `missing_heading` warnings.
- Committed publication history/archive validator after fetching public tags/remote refs: PASS; 206 tracked files, 208 historical paths, 95 root trees, 707 blobs, 103 commits, 2 annotated tag objects and no symlink entries.
- System validators: `quick_validate.py` passed the new incident-search Skill and `validate_plugin.py` passed the v0.3.10 plugin.
- Live Infoblog check: fixed URL returned 30 title matches for the generic term `распределение`; ETag `"499cf1-65ced0da22a80"`, Last-Modified `Sat, 03 Oct 2026 10:24:26 GMT`, payload SHA-256 `7c0c182e0a27e7193d47ab20e5bd107167fb3a4211a2bb6bae63d9a1d7910ceb`.
- Upstream compatibility checks: Unica marketplace commit tests passed 43/43; Jev repository tests passed 20/20 without a paid provider call.

## Decision

No known critical control is failed in the reviewed local candidate. Repository validation can pass without claiming publication or runtime acceptance. Merge/release remains blocked by the external warnings applicable to those claims.
