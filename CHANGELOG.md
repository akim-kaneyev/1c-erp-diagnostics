# Changelog

## 0.2.2 — marketplace refresh hotfix candidate

- restored the stable internal marketplace ID `one-c-erp-diagnostics-marketplace` so existing installations can update in place;
- retained `1C ERP Diagnostics Ecosystem` as display text rather than installation identity;
- switched external companion commit pins from `ref` to the verified `sha` selector supported by the OpenAI marketplace loader;
- bumped the plugin/package version so the installed plugin cache receives the scoped Gate-closure correction;
- added regression checks preventing marketplace-ID drift, commit-selector misuse and version-stable behavior changes;
- documented the exact refresh failure cause and recovery path.

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
