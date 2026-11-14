# v0.3.11 scoped package audit

Date: 2026-11-14. Scope: local test-bridge read adapter, packaged skill, routing, evidence contract and release metadata.

| Control | Result | Evidence / boundary |
|---|---|---|
| Source identity | PASS | msrv-tech/skills immutable `702dc8dbe0a0d31b1a16af3d871af29b99ef1122`; pinned protocol links in packaged reference |
| Upstream license | WARNING | No root license grant verified; redistribution/automatic installation deferred; no upstream implementation bundled |
| Marketplace | PASS | Same five entries and immutable companion pins; bridge is an optional host adapter |
| Execution surface | PASS | Four constructed read commands; no generic forwarding, object writes, BSL, rendering, installation or publication changes |
| Contour identity | WARNING | Explicit test scope and expected metadata checked; Health cannot uniquely identify a base or attest installed CFE |
| Transport and parsing | PASS | Literal loopback only, proxies/redirects rejected, bounded strict UTF-8 JSON, command-level errors and row counts checked |
| Evidence integrity | PASS | Exact byte hashes, case/Evidence/analytic/run identities; offline verification recomputes hashes and coverage |
| Business proof | PASS | Bounded query never claims complete population; metadata/Health never substitute for accounting acceptance or Gate 7 |
| Report/print-form execution | PASS | Separate reviewed execution scope, disposable base, exact inputs and retrieved output assertions required |
| Package boundary | PASS | Script/reference are shipped inside the skill; repository wrapper has no runtime dependency from installed package |
| Privacy | PASS | Explicit local request/result storage; raw evidence remains private; no developer data destination or credential support |
| Version and lock | PASS | Candidate 0.3.11 and deterministic skill lock verified by repository checks |
| Live test contour | WARNING | No identified authorized live base supplied; synthetic HTTP tests are not claimed as live acceptance |
| Exact-version model acceptance | WARNING | Complete installed v0.3.11 clean-session run remains pending, independently of repository CI |
| PR CI / CodeQL | WARNING | Obtain results for the final PR commit; local checks do not attest GitHub execution |

No known critical control failure is asserted for the scoped implementation after repository validation. Warnings are explicit acceptance boundaries, not decorated passes. Do not merge/tag/release or claim live/runtime acceptance until the repository's required external gates pass. A hash bundle is not signed evidence and cannot detect an adversary rewriting both data and manifest; offline verification intentionally reports freshness as unverified.
