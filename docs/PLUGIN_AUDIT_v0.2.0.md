# Plugin self-audit — v0.2.0

Audit target: `plugins/one-c-erp-diagnostics/` and the repository-level Gate 0–10 contract.

Audit result: **PASS with three non-critical runtime warnings**. No critical control is `FAIL`.

## Controls

| # | Control | Status | Evidence |
|---|---|---|---|
| 1 | Manifest identity and version are consistent | PASS | Manifest and `pyproject.toml` both declare `0.2.0`; CI validates strict semver, repository/homepage/license, interface fields and prompt limits. |
| 2 | Brand assets are structurally valid | PASS | `composerIcon`, `logo` and `logoDark` exist; CI validates PNG signature, IHDR/IDAT/IEND structure, dimensions and CRCs. |
| 3 | Single entrypoint owns the workflow | PASS | Repository and packaged master skills require one user invocation and ordered Gate 0–10 execution. |
| 4 | Capability availability is not invented | PASS | Gate 0 records `available`, `confirmation_required`, `unavailable` or `prohibited`; Unica, 1C Skills, OpenSandbox and other companions are never assumed. |
| 5 | Dynamic plan is bounded | PASS | One primary domain, at most two secondary domains and no more than four active specialist nodes without explicit justification. |
| 6 | Evidence provenance and contradictions are preserved | PASS | Gate 6 uses a claim ledger with supporting/contradicting evidence, falsifiers and specialist/capability provenance. |
| 7 | Gate 7 protects final causality | PASS | Final `УСТАНОВЛЕНО` is forbidden when adversarial verification is unavailable or fails. |
| 8 | Gate 9 validates identical analytics | PASS | Post-change validation compares the same analytic key and checks movements, records, amounts, balances, postings and side effects. |
| 9 | Production-impacting actions are controlled | PASS | `R0–R3` model requires explicit approval, scope, rollback and validation for production/accounting/access/closed-period actions. |
| 10 | External companions are integrated honestly | PASS | Unica and 1C Skills are optional host-managed capabilities; private implementation is not copied and no fabricated `.app.json`/MCP dependency is declared. |
| 11 | Open-source intake is controlled | PASS | Every addition requires source/license verification, version pin where applicable, sanitized tests, risk classification and fallback/rollback. |
| 12 | Optional Python adapters are pinned and importable | PASS | CI installs and imports `v8unpack==1.2.6` and `opensandbox==0.1.14` on Python 3.10 and 3.12 and verifies the expected extraction/Sandbox APIs. |
| 13 | Artifact extraction is non-executing and bounded | PASS | Adapter accepts only sanitized CF/CFE/EPF, refuses implicit overwrite, records SHA-256/provenance and excludes rebuild/BSL execution. |
| 14 | Public package contains no case data or forbidden artifacts | PASS | Validator rejects tracked case input/work files, `.dt`, `.1CD`, backups, keys and obvious plaintext credential assignments. |
| 15 | Regression suite covers the dynamic contract | PASS | CI reports 31 packaged skills and passes manifest, risk/orchestration, optional-adapter, XLSX, PDF and case-indexing tests on both supported Python versions. |

## Runtime warnings

### WARNING 1 — host-managed companion availability

Repository CI cannot prove that a particular ChatGPT session exposes Unica, 1C Skills, Computer Use or another installed plugin. Gate 0 therefore must be verified in a clean ChatGPT session after marketplace re-import.

### WARNING 2 — UI rendering cache

PNG integrity is proven, but GitHub/ChatGPT visual rendering and cache refresh are product-surface behaviors. The selected Variant A icon must be visually confirmed after the `0.2.0` marketplace package is re-imported.

### WARNING 3 — BSL Language Server is documented, not bundled

BSL Language Server remains an optional external analyzer. Each use must record its exact release, command and report. Its diagnostics are not a case-specific accounting cause without evidence-chain linkage.

## Conclusion

The `0.2.0` candidate is internally consistent, substantially safer than a hard-wired multi-plugin bundle, and has no critical self-audit failure. Merge is technically permitted after CI remains green. Public release remains blocked until the clean-session capability, under-evidenced, unavailable-companion and UI-icon smoke tests pass.
