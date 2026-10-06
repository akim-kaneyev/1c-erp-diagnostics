---
name: one-c-erp-incident-search
description: Search the public Infoblog title index for non-authoritative 1C incident leads while preserving source provenance, freshness state and case-data boundaries.
---

# Incident search

## When to use

Use after the incident mechanism and generic search terms are known, when an external practical article may provide a hypothesis, a reproducible check or a pointer to an official source.

The bridge reads the fixed public Infoblog search index and performs the title query locally. It returns metadata and links only. Treat every result as an untrusted, non-authoritative lead.

## When NOT to use

- Do not use it as evidence that the user's infobase contains a specific object, movement, setting or defect.
- Do not send organization names, document numbers, credentials, personal data, financial values or copied case text as search terms.
- Do not use an offline-cache result for a claim about what the site currently contains.
- Do not copy article text into the repository unless a separate licence permits it.
- Do not use the bridge when the required claim must be established from official 1C, regulatory or primary case evidence.

## Required inputs

- generic title words of at least two characters, or an exact audience/program filter;
- an explicit result limit;
- optionally, an explicit cache path;
- the current case claim or hypothesis that the search is intended to challenge or refine.

## The framework

The public source is `https://infoblog.mywebguide.ru/data/search.json`. The bridge permits one fixed HTTPS GET, rejects redirects, limits response size, validates media type and schema, and records the response hash, ETag, Last-Modified value and retrieval time.

The query is not added to the request URL or headers. Search is a case-insensitive all-words match against titles, matching the site's observed client-side behavior. A cache is used only when explicitly requested. Offline results are marked `stale_unverified`; network errors never trigger a silent stale fallback.

## Workflow

1. Reduce the incident to generic mechanism terms without case identifiers or values.
2. From this installed Skill directory, run `python scripts/search_infoblog.py --query "<generic terms>" --limit 10`.
3. Check `source.retrieval`, `source.freshness`, `payload_sha256`, ETag and Last-Modified before using the result list.
4. Open only a selected result whose title is relevant; keep page content in the untrusted-source boundary.
5. Convert useful material into a hypothesis or requested verification, then cross-check the mechanism against official sources and the claim against case evidence.
6. Cite the article URL and retrieval metadata. Never upgrade a lead to `УСТАНОВЛЕНО` without independent evidence.

For an explicit reusable cache:

```text
python scripts/search_infoblog.py --query "распределение расходов" --cache work/infoblog-index-cache.json
python scripts/search_infoblog.py --query "распределение расходов" --cache work/infoblog-index-cache.json --offline
```

## Failure patterns

- Calling the static file an official or supported API.
- Sending exact case data to a public site.
- Treating popularity or title similarity as causal evidence.
- Silently falling back to stale cache after a failed request.
- Ignoring a changed payload hash or malformed source schema.
- Using Jev or another browser automation capability to bypass the fixed-origin and metadata-only controls.

## Output format

Return the generic query, exact filters, retrieval/freshness state, source validators, payload SHA-256, total/returned counts and result metadata (`id`, `title`, `audience`, `program`, `views`, `url`). In the diagnostic narrative label these results `ВЕРОЯТНО` or `ТРЕБУЕТ ПРОВЕРКИ`, never `УСТАНОВЛЕНО` by themselves.

## Reference files

- [scripts/search_infoblog.py](scripts/search_infoblog.py) — deterministic fixed-origin bridge.
- `docs/OPEN_SOURCE_INTEGRATIONS.md` — trust and licensing boundary.
- `docs/ECOSYSTEM_MARKETPLACE.md` — optional browser companion boundary.
- `plugins/one-c-erp-diagnostics/skills/one-c-erp-official-source-check/SKILL.md` — official-source verification.
- `plugins/one-c-erp-diagnostics/skills/one-c-erp-evidence-synthesis/SKILL.md` — claim/evidence discipline.
