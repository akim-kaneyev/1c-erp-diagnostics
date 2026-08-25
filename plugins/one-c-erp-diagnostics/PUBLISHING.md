# Publishing and validation

## Required package checks

- manifest version matches `pyproject.toml`;
- author/homepage/repository/license/interface/policy URLs are valid;
- `composerIcon`, `logo` and `logoDark` exist and pass PNG CRC validation;
- at least 32 packaged skills are present, including local static-analysis and dynamic-control skills;
- public-package, publication-history and ecosystem-marketplace validators pass;
- regression tests pass on Python 3.10 and 3.12;
- CodeQL results are present for the release Pull Request;
- no secrets, real case data, production databases or unsupported dependency claims exist;
- `.scannerwork/` and runtime SonarQube evidence are excluded; no token assignment exists anywhere in the candidate.

## Evidence and execution integrity checks

- every material derived artifact used by the harness preserves source Evidence ID(s), transformation, tool/version/ref, run identity when executable, and output hash/identifier where available;
- every material `УСТАНОВЛЕНО` claim has closed source-to-conclusion provenance;
- every relied-upon executable result matches the current case and current material input identities;
- stale/mismatched reports are rerun or explicitly proven equivalent rather than silently reused.

## Strict evaluation-output checks

- literal `EVAL_RESULT_JSON` returns exactly one JSON object without Markdown or prose;
- the supplied skeleton is preserved exactly: no extra/missing/renamed fields or wrong data types;
- Gate statuses use only `pending | passed | blocked | failed | stale | not_required` in lower case;
- Gate-procedure completion is not confused with claim proof status;
- read-only evidence assessment/refusal is `R0`; evidentiary uncertainty cannot by itself become `R3`;
- missing current evidence/rerun/equivalence is `EVIDENCE_REQUIRED`; `NO-GO` is reserved for an unsafe/prohibited/unapproved in-scope action;
- `not_in_scope` requires explicit scope exclusion;
- claim items are exactly `{id, status, text, evidence_ids, falsifier}`;
- causal links are exactly `{stage, evidence_ids}` and `complete=true` requires all six canonical 1C stages in order;
- actions are empty when absent and otherwise use exact structured action objects.

## Required ecosystem checks

- marketplace contains exactly `one-c-erp-diagnostics`, `unica`, `1c-skills`, `1c-skills-py` in documented order;
- Unica is pinned to canonical marketplace release `v0.12.0` and subdirectory `plugins/unica`;
- 1C Skills PowerShell/Python use reviewed immutable generated commit refs;
- every plugin remains `AVAILABLE`, not silently `INSTALLED_BY_DEFAULT`;
- third-party licenses, sources, refs, permissions and update policy are documented;
- no third-party code is copied or relicensed in this repository.

## Clean-session smoke tests

1. marketplace refresh/re-import shows all four plugins;
2. 1C ERP Diagnostics `0.3.3` and the approved Velis icon render in GitHub and the plugin selector, or the runtime explicitly reports `version not exposed` if version metadata is unavailable;
3. Gate 0 reports actual companion availability without treating public-plugin resolver failure as proof that the selected skills-first custom-marketplace plugin is uninstalled;
4. an installed companion call records canonical identity, inputs, operation, run identity, output and limitations;
5. an under-evidenced case cannot end as final `УСТАНОВЛЕНО`;
6. an unavailable companion request becomes fallback/`blocked`, not simulated;
7. Gate 7 challenges original evidence, causal chain and provenance closure;
8. analysis-only work is `R0` and may mark Gate 9 `not_required`;
9. a scoped `R3` safety-only test returns `NO-GO`, `Current goal: closed; linked incident: open` and no decorated Gate statuses;
10. Gate 0 reports `sonarqube-bsl-local` from actual loopback/server/scanner/BSL/auth state rather than marketplace presence;
11. an available sanitized local scan records `R1`, source/tool/analysis/run provenance and complete paginated evidence without retaining a token;
12. a static finding without runtime and ERP-chain evidence remains below `УСТАНОВЛЕНО` after Gate 7;
13. the exact rendered `provenance-closure-broken` result passes `tools/validate_evals.py` and cannot establish source content;
14. the exact rendered `stale-execution-result` result passes `tools/validate_evals.py` with `R0`, `EVIDENCE_REQUIRED`, `linked_incident_status=blocked`, `Gate 5=stale`, `Gate 7=passed`, `Gate 10=blocked`, schema-valid claims, `causal_chain.complete=false` and `actions=[]`;
15. the complete 16-case clean-session run passes `tools/validate_runtime_run.py` for exact installed version `0.3.3`.

## Repository publication

Before a versioned release:

1. use a full Git checkout (`fetch-depth: 0`);
2. run `python tools/validate_publication_history.py` and require PASS;
3. confirm `git archive HEAD` contains exactly the tracked release files;
4. fail if full history contains prohibited case/database/backup/private-key/environment paths, detected plaintext credential assignments or user-machine absolute paths;
5. confirm Python 3.10/3.12 CI, CodeQL and self-audit are green on the release Pull Request;
6. merge only through the protected `main` ruleset;
7. confirm repository description, topics, policies and brand assets are current;
8. verify private vulnerability reporting, dependency monitoring, secret scanning and push protection remain enabled;
9. perform an anonymous review of README, privacy, terms, support and license URLs.

The history validator supplements GitHub secret scanning/push protection and does not replace independent privacy, rights or dependency review.

## ChatGPT/Codex Plugin Directory publication

Public GitHub visibility does not itself create a global listing. After the repository release is available, use the supported ChatGPT/workspace plugin import/publication flow, review listing metadata and permissions, and repeat clean-session smoke tests after installation.

## Release gate

Run `one-c-erp-plugin-audit`. Any critical `FAIL`, failed publication-history check, failed required CI/CodeQL check, or failed exact-version runtime acceptance claim blocks the corresponding release/publication statement.
