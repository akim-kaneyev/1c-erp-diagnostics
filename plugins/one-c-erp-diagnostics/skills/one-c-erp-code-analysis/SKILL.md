---
name: one-c-erp-code-analysis
description: Analyze supplied 1C code, queries, SKD definitions or extensions and connect code behavior to observed ERP movements/results without inventing metadata.
---

# 1C code analysis

Use only code actually provided or fetched from the relevant repository. Identify inputs, branches, queries, writes, calls and conditions. Map code paths to observed evidence only when identifiers match or the linkage is otherwise proven.

For a causal conclusion show: input/context → executed branch/query → produced/changed record/result → observed symptom. Distinguish unreachable code, possible code path and demonstrated code path. If runtime behavior is required to prove execution and no trace/test is available, do not mark it established.

When static analysis adds value, route discovery and execution through `one-c-erp-local-static-analysis`. Preserve the analyzer, server/plugin/scanner versions, project/source identity, analysis ID, rule, file/line and report hash. A SonarQube or BSL Language Server finding proves only that the analyzer reported a rule violation for that source snapshot. It does not prove that the branch executed or caused the ERP incident; require matching runtime and document/movement/register evidence and Gate 7 review.
