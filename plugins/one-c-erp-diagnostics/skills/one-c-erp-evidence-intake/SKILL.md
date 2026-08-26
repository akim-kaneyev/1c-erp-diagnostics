---
name: one-c-erp-evidence-intake
description: Inventory and rank 1C:ERP evidence such as movements, registers, postings, reports, screenshots, XLSX, PDF, MXL exports and code before diagnosis.
---

# Evidence intake

Use for Gate 2.

For every source record: identity, type, period, organization if present, key document/report identifiers, what question it can answer, and its limits.

Evidence priority: movements → exact register records → postings/drill-down → reports → code/queries → screenshots → official docs → theory.

## Evidence coverage contract

Every source or attachment supplied for the current case must receive an Evidence ID and exactly one disposition:

- `examined` — materially inspected with an appropriate method;
- `unreadable` — present but the available capability cannot inspect it reliably;
- `duplicate` — duplicates an identified source and adds no new information;
- `irrelevant_with_reason` — outside the current goal, with the reason recorded;
- `blocked` — relevant inspection depends on an unavailable or unapproved capability.

Gate 2 cannot pass while supplied evidence is unaccounted for. Do not silently omit an attachment because another source looks sufficient.

Once every supplied item is accounted for and its limitations are recorded, Gate 2 passes even when additional expected evidence is missing. Expected-but-missing movements, registrar, register records or mechanism evidence block the affected diagnostic Gate, normally Gate 4, rather than retroactively blocking evidence intake. For `under-evidenced-cost`, accounting for `E-COST-1` therefore means Gate 2 `passed` and Gate 4 `blocked`.

Record the inspection method as part of provenance. For visually rich or structured inputs, use a modality-appropriate method: inspect relevant PDF pages/screenshots, enumerate relevant XLSX sheets/ranges, preserve extracted CF/CFE/EPF structure, and for `.mxl` use only a verified export/inspection path supported by the current host.

Keep two gaps separate:

1. **supplied-but-unexamined evidence** — material already provided but not reliably inspected;
2. **expected-but-missing evidence** — the smallest additional evidence set needed to test a claim.

A final `УСТАНОВЛЕНО` conclusion is forbidden if material supplied evidence remains `unreadable` or `blocked` and could reasonably falsify the conclusion.

## Artifact-anchor and derivation contract

Evidence created by parsing, filtering, normalization, joining, comparison, OCR/export or another transformation is derived evidence. It must keep a traceable lineage to the original artifact:

- parent Evidence ID(s) in `derived_from`;
- transformation name;
- tool and version/ref when applicable;
- `run_id` for executable transformations;
- output hash/identifier when the derived result is persisted or deterministically serializable.

Do not treat a derived table/report as proof of what the original file contained if the parent anchor or transformation is missing. If a material derivation chain is broken, record the evidence as provenance-incomplete and block any final conclusion that depends on that gap.

Do not infer hidden 1C fields or objects from visual similarity. For `.mxl`, do not pretend to have a universal parser; prefer a verified export to XLSX/XML/HTML/TXT plus PDF for visual control when needed.

List the smallest missing evidence set required to advance a blocked conclusion.
