# Changelog

## 0.3.3 — strict runtime evaluation output

- added mandatory strict `EVAL_RESULT_JSON` mode to the authoritative, packaged and portable orchestrators;
- require exactly one JSON object matching the supplied skeleton, with no renamed, missing or additional fields;
- clarified that Gate status describes Gate-procedure completion rather than whether a hypothesis was proved;
- prohibit upper-case, combined and custom Gate values and retain only `pending | passed | blocked | failed | stale | not_required`;
- clarified that `R0–R3` classifies the actual/proposed action surface, so read-only rejection of stale evidence is `R0`, not `R3`;
- separated `EVIDENCE_REQUIRED` from `NO-GO`: missing current evidence/rerun/equivalence is an evidence decision, while `NO-GO` blocks an unsafe or unapproved action;
- restricted `not_in_scope` to incidents explicitly excluded by the prompt;
- fixed the strict claim, causal-link and action object contracts and prohibited treating a logical stale-evidence argument as a complete six-stage 1C causal chain;
- added regression assertions covering the runtime mistakes observed after installing v0.3.2;
- retained artifact provenance closure, execution identity, the 16-case suite, 32 packaged skills, stable marketplace identity and immutable companion pins.

## 0.3.2 — provenance closure and publication integrity

- added artifact-anchor/derivation lineage for material derived evidence, including parent Evidence IDs, transformation, tool/version/ref, execution run and output identity where applicable;
- added `closed | open | broken` provenance closure across source artifact → evidence → premise → causal link → conclusion;
- added execution identity and stale-result handling so an old or mismatched tool report cannot prove the current case/input state;
- strengthened Gate 7 to independently verify lineage and execution freshness in addition to evidence coverage and causal links;
- extended resumable case state with derivation and execution ledgers;
- expanded the executable acceptance suite from 14 to 16 cases with required `provenance_closure` and `execution_identity` controls;
- added a full-history publication validator that verifies `git archive HEAD`, rejects shallow-history release claims and scans historical paths/text for prohibited artifacts, credential assignments and user-machine paths;
- changed CI checkout to `fetch-depth: 0` and made publication-history validation mandatory on Python 3.10/3.12;
- retained 32 packaged skills, the stable four-plugin marketplace and all immutable companion pins;
- adopted only general engineering methodology from the reviewed Grok reconstruction repository; no external reconstructed implementation code was copied.

## 0.3.1 — factual SonarQube Gate 0 discovery

- fixed Gate 0 so absence of a dedicated SonarQube MCP/app/tool name is not treated as evidence that the local runtime is unavailable;
- require factual loopback status/version and scanner-version probes whenever the session exposes local execution and loopback HTTP;
- classify a blocked read-only probe as `confirmation_required / host_execution_confirmation_required` rather than invented `unavailable`;
- preserve observed server/scanner facts when protected APIs return `401/403` and keep the capability at `confirmation_required / authentication_required`;
- added regression assertions and clean-session smoke expectations for the reported cross-project failure;
- retained the stable marketplace ID, 32 skills and all immutable companion pins.

## 0.3.0 — optional SonarQube BSL evidence and executable acceptance gates

- added the optional `sonarqube-bsl-local` capability and a packaged SonarQube analysis skill, bringing the primary plugin to 32 packaged skills;
- defined a verified local baseline for SonarQube Community Build `26.8.0.126808`, SonarScanner CLI `8.0.1.6346` and communitybsl `1.20.0`;
- pinned the reviewed communitybsl artifact digest to SHA-256 `595F741AFD49BC7F1869B3F82F623821D519CECB399C56F154E55EA83DC7057B`;
- required SonarQube tokens to be supplied through the environment only and prohibited credentials in repository files, reports, logs and case state;
- classified local analysis as `R1`, SonarQube project/token administration as `R2` and source upload to a remote SonarQube instance as `R3`;
- kept static-analysis findings at hypothesis level until linked to the diagnostic evidence chain and accepted through Gate 7;
- retained the stable marketplace ID `one-c-erp-diagnostics-marketplace`, exactly four marketplace plugins and the existing immutable companion pins;
- added executable evaluation and runtime-acceptance contracts to the public-release gate.

## 0.2.3 — Velis branding and repository hardening

- replaced the previous plugin artwork with the approved white-dog Velis mascot identity;
- retained one Velis medallion on the collar and removed the redundant second medallion from the draft;
- added separate optimized composer, card and dark-surface assets;
- documented the approved asset mapping and brand/trademark boundary;
- preserved the independent-project disclaimer and did not introduce the corporate 1C logo;
- aligned the plugin manifest, project metadata, README, policies, release notes, audit, validators and tests to version `0.2.3`;
- recorded the active `main` ruleset with required Pull Request, squash merge, Python 3.10/3.12 checks, CodeQL results, resolved conversations, linear history, no force-push and no deletion;
- recorded successful CodeQL default setup for GitHub Actions and Python with zero open alerts;
- recorded private vulnerability reporting, dependency graph, Dependabot alerts/security updates, secret scanning and push protection as enabled.

## 0.2.2 — public preview

- opened the clean release repository to the public under `akim-kaneyev/1c-erp-diagnostics`;
- restored the stable internal marketplace ID `one-c-erp-diagnostics-marketplace` so existing installations can update in place;
- retained `1C ERP Diagnostics Ecosystem` as display text rather than installation identity;
- switched external companion commit pins from `ref` to the verified `sha` selector supported by the marketplace loader;
- bumped the plugin/package version so the installed plugin cache receives the scoped Gate-closure correction;
- added regression checks preventing marketplace-ID drift, commit-selector misuse and version-stable behavior changes;
- validated the four-plugin marketplace, Gate 0 capability inventory, under-evidenced-case behavior and `R3 / NO-GO` safety control;
- updated README, privacy, release notes, public launch checklist and v0.2.2 self-audit for public distribution.

## 0.2.1 — verified ecosystem marketplace candidate

- expanded the repository marketplace from one local plugin to a verified four-plugin 1C ecosystem;
- added canonical Unica `0.12.0` source `IngvarConsulting/unica-marketplace@v0.12.0`;
- added immutable generated refs for 1C Skills PowerShell and Python from `Nikolay-Shirokov/cc-1c-skills`;
- documented third-party licenses, provenance, permissions and update boundaries;
- updated Gate 0 companion coordination to use canonical plugin identities and conflict handling;
- added ecosystem installation, capability, under-evidenced, unavailable-companion and `R3` smoke tests;
- added public terms and publication preparation guidance;
- strengthened validation to verify the exact external marketplace contract.

## 0.2.0 — dynamic orchestrator candidate

- repaired the corrupted PNG brand asset and added separate `composerIcon`, `logo` and `logoDark` files;
- expanded the manifest with author, homepage, license, public URLs and validated interface metadata;
- introduced Gate 0 capability discovery and a bounded dynamic execution graph;
- added evidence synthesis, contradiction handling and capability provenance;
- added optional companion coordination for Unica, 1C Skills, document tools, GitHub/Drive, Computer Use and OpenSandbox;
- made companion plugins runtime-discovered rather than fabricated hard dependencies;
- added `R0–R3` action-risk controls;
- added sanitized CF/CFE/EPF extraction through optional pinned `v8unpack`;
- added release-difference and open-source intake skills;
- strengthened the plugin validator with PNG CRC checks, manifest checks and dynamic-contract tests.

## 0.1.2 — public-ready candidate

- polished international README and project positioning;
- added MIT license, privacy, contribution, conduct and trademark notices;
- added public-release checklist, GitHub profile copy and smoke-test plan;
- added issue and pull-request templates;
- public developer identity migrated to `akim-kaneyev`;
- retained Gate 1–10 evidence-first orchestration and adversarial verification.

## 0.1.1

- added Variant A brand identity and plugin icon;
- added `composerIcon`, `logo` and `brandColor` metadata;
- improved public repository presentation.

## 0.1.0

- initial skills-only plugin package;
- Gate 1–10 master orchestrator;
- domain skills for cost/month close, post-item expenses, settlements, VAT, warehouse/series/assignments, production, access rights and code analysis;
- independent verification, case-state, safety and official-source skills;
- local marketplace and global Codex skill installation.
