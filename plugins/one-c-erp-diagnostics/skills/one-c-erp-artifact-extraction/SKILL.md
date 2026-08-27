---
name: one-c-erp-artifact-extraction
description: Safely extract and inventory sanitized 1C CF/CFE/EPF artifacts without running untrusted BSL or loading them into an information base.
---

# 1C artifact extraction

Use for sanitized `.cf`, `.cfe` and `.epf` evidence.

1. Record filename, size and SHA-256.
2. Confirm the artifact is sanitized and contains no credentials/customer data.
3. Use the pinned optional `v8unpack` adapter through the [bundled extraction adapter](scripts/unpack_1c_artifact.py).
4. Extract into a new empty directory; never build/repack in the diagnostic workflow.
5. Preserve `_extraction_manifest.json`.
6. Inventory confirmed metadata, BSL and JSON files.
7. If static BSL analysis is useful, route the extracted `.bsl`/`.os` tree through `one-c-erp-local-static-analysis` when a safe local SonarQube capability is confirmed; otherwise use a reviewed BSL Language Server/manual fallback. Record the exact analyzer versions, command/properties with credentials redacted, source manifest and report hash.
8. Link any code finding to the factual document/movement chain before treating it as causal.

Do not rename unsupported formats to bypass validation. Do not execute extracted BSL. `.mxl` remains subject to the conservative export policy rather than this extractor.

For an `.mxl`-derived tabular export, capture `rows_present`, row/column counts, redacted header/value previews and SHA-256 before accepting it as row evidence. Cell count alone cannot distinguish a property tree from business rows: confirm `--view-kind rows --view-sheet-index N` with the new visual-gate Evidence ID for that exact sheet. One visual-gate Evidence ID never confirms other workbook sheets. Schema/property metadata is `wrong_view/incomplete`; change the export instruction and repeat the visual gate rather than claiming row content. Credential-like or user-machine values are redacted and block acceptance.
