# Reviewed protocol and local workflow

Reviewed 2026-11-14:

- Discovery article: https://infostart.ru/1c/articles/2705751/ (2026-08-27).
- Source: https://github.com/msrv-tech/skills at `702dc8dbe0a0d31b1a16af3d871af29b99ef1122`.
- [Pinned API specification](https://github.com/msrv-tech/skills/blob/702dc8dbe0a0d31b1a16af3d871af29b99ef1122/codex-test-bridge/BRIDGE.md).
- [Pinned implementation inspected for response shapes](https://github.com/msrv-tech/skills/blob/702dc8dbe0a0d31b1a16af3d871af29b99ef1122/codex-test-bridge/src/HTTPServices/CodexTestBridge/Ext/Module.bsl).

The article's 82 operation skills have since become 13 domain skills in the reviewed README. Use current pinned paths rather than the article's old operation folders. `msrv-tech/skills` is a different source from the existing `Nikolay-Shirokov/cc-1c-skills` marketplace entries. No license file or license grant was found at the reviewed repository root; copying/redistribution is deferred pending clarification. This package contains an independently written HTTP client, not upstream code or binaries. The protocol review is not certification of an installed bridge or its security.

## Wire contract

`GET <base>/health` must return JSON with literal `ok: true`, `service: CodexTestBridge`, and the expected `metadataName`. The bridge does not provide a unique infobase ID or installed commit through Health. Explicitly identify the disposable test base independently; bases using the same configuration name cannot be distinguished by Health.

`POST <base>/command` takes one constructed command:

| Command | Request fields | Response checked |
|---|---|---|
| Metadata | sections from the five documented collections | matching metadataName, section arrays |
| Describe | kind catalog/document/enum, existing metadata name | object, attributes, tableParts |
| Query | text, params, limit 1–1000 | rows as objects, integer count equal to returned rows |

The upstream Query response has no total-row count or trustworthy completeness flag. `count == limit` may be truncated. `count < limit` still cannot prove that the query covers all required analytics or that the source is unchanged. Reconcile against independent counts/totals at the same cutoff. Nonexistent or different protocol fields fail closed.

Only literal `127.0.0.1` and `[::1]` over HTTP and a publication path ending in `/hs/codex-test` are accepted. DNS names are excluded to avoid resolution changes. HTTP on loopback matches the reviewed local publication; remote and authenticated connections require a separately reviewed design. System proxies, redirects and compressed responses are disabled; JSON bodies are limited to 4 MiB. Errors expose only stable reason codes. There is no automatic retry and no query cancellation guarantee.

## Commands

Run from this skill directory. Replace the sample configuration name and case context with observed identities; no example is an instruction to connect to an unknown base. The output must be a new directory in a private case workspace outside the repository.

```text
python scripts/test_bridge.py capture health --base-url http://127.0.0.1:9091/demo/hs/codex-test --expected-metadata-name Demo --test-contour --case-id CASE-DEMO --evidence-id E-DEMO --analytic-key demo-period --output <private-case-dir>/health-run

python scripts/test_bridge.py capture metadata --base-url http://127.0.0.1:9091/demo/hs/codex-test --expected-metadata-name Demo --test-contour --case-id CASE-DEMO --evidence-id E-DEMO --analytic-key demo-period --sections documents accumulationRegisters --output <private-case-dir>/metadata-run

python scripts/test_bridge.py capture query --base-url http://127.0.0.1:9091/demo/hs/codex-test --expected-metadata-name Demo --test-contour --case-id CASE-DEMO --evidence-id E-DEMO --analytic-key demo-period --query-file <private-case-dir>/query.txt --params-file <private-case-dir>/params.json --limit 100 --output <private-case-dir>/query-run

python scripts/test_bridge.py verify --bundle <private-case-dir>/query-run --case-id CASE-DEMO --evidence-id E-DEMO --analytic-key demo-period
```

The repository checkout also provides a wrapper with the same filename in its tools directory; the installed skill uses the packaged command above. Query text is UTF-8 (BOM accepted); optional params are a JSON object with upstream-supported typed values. Inspect queries for bounded period/analytics and workload before sending. The adapter is not a query optimizer or a parser proving semantic safety. No arbitrary BSL, common-module calls, object writes, posting, deletion, UI jobs or rendering commands are accepted.

Each capture stores exact `health.json`, `response.json`, constructed `request.json`, and a final `manifest.json` containing run/case/Evidence identities, analytic key, timestamps, adapter hash, reviewed protocol revision, file hashes/sizes and coverage limitations. Data may include confidential query results. Keep all artifacts local with appropriate filesystem access; never publish them to Git. The verifier checks integrity and supplied context offline; `freshness: not_verified` is intentional.

## Functional validation of reports and print forms

Use separately authorized upstream tooling only when installed revision/permission and test-contour isolation are verified. The read adapter does not perform these steps.

1. Hash and inspect sanitized EPF/ERF sources; build into a new temporary file. Record source, platform/configuration and built-artifact hashes. Building is structural evidence only.
2. Select the exact test document UUID(s), period, analytic filters, expected rows/totals and falsifiers before execution. Avoid the upstream fallback that silently selects the first document for an acceptance test.
3. Render through the reviewed `RenderExternalPrintForm` or `RenderExternalReport` contract. The documented test exports are `СформироватьПечатнуюФормуДляТеста(МассивОбъектов)` and `СформироватьОтчетДляТеста(Параметры)`. Do not insert these methods into supplied code without an authorized development scope.
4. Treat EPF/ERF loading and rendering as external-code execution with possible writes. Use a disposable base, least privilege, known input data and a snapshot/rollback. No production contour; no blind retry after timeout.
5. A returned server path is not a local artifact. Retrieve output through an authorized local/server file channel, validate path containment, hash actual MXL/HTML/TXT bytes, link parent Evidence IDs and run ID, and retain execution errors.
6. Independently compare headers, row identities/counts, duplicates, empty sections, totals, tax/rounding and expected analytic coverage. Inspect visual layout when it matters. A text export cannot prove layout; an MXL property tree cannot prove tabular values.
7. Compare before/after on identical analytics, record expected versus observed values and failed assertions. Require Gate 7 independent challenge and Gate 9 evidence before closing the scoped goal. A demo-only success does not prove a production incident resolved.

Fallback: existing Unica/1C Skills capabilities in an authorized disposable contour, offline XML/static review, or manually produced same-analytics exports. Report the missing runtime acceptance explicitly; do not simulate it. Rollback for this adapter is removal of the feature/plugin version; it never changes the base or publication.
