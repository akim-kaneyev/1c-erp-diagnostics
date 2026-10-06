from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


INDEX_URL = "https://infoblog.mywebguide.ru/data/search.json"
ARTICLE_URL_TEMPLATE = "https://infoblog.mywebguide.ru/articles/page_{article_id}.html"
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
CACHE_SCHEMA_VERSION = 1
USER_AGENT = "one-c-erp-diagnostics/0.3.10 (+metadata-only incident search)"
SENSITIVE_TERM = re.compile(
    r"(?i)(?:password|passwd|pwd|token|api[_ -]?key|secret)\s*[:=]\s*\S+"
    + r"|(?:[a-z]:\\"
    + "us"
    + r"ers\\|/ho"
    + r"me/|/us"
    + r"ers/)"
)


class BridgeError(RuntimeError):
    """A fail-closed error safe to show without response content."""


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        raise BridgeError("redirects are not allowed for the fixed Infoblog index")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def payload_sha256(payload_text: str) -> str:
    return hashlib.sha256(payload_text.encode("utf-8")).hexdigest()


def _require_fixed_url(value: str) -> None:
    expected = urlsplit(INDEX_URL)
    actual = urlsplit(value)
    if (
        actual.scheme != "https"
        or actual.netloc != expected.netloc
        or actual.path != expected.path
        or actual.query
        or actual.fragment
    ):
        raise BridgeError("response URL differs from the fixed Infoblog index")


def parse_index(payload_text: str) -> dict[str, Any]:
    try:
        data = json.loads(payload_text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise BridgeError("Infoblog index is not valid JSON") from exc

    if not isinstance(data, dict):
        raise BridgeError("Infoblog index root must be an object")
    audiences = data.get("a")
    programs = data.get("p")
    rows = data.get("r")
    if not isinstance(audiences, list) or not all(
        isinstance(item, str) for item in audiences
    ):
        raise BridgeError("Infoblog audience dictionary has an unexpected schema")
    if not isinstance(programs, list) or not all(
        isinstance(item, str) for item in programs
    ):
        raise BridgeError("Infoblog program dictionary has an unexpected schema")
    if not isinstance(rows, list):
        raise BridgeError("Infoblog result rows have an unexpected schema")

    for row in rows:
        if not isinstance(row, list) or len(row) != 5:
            raise BridgeError("Infoblog result row has an unexpected schema")
        article_id, title, audience_index, program_index, views = row
        if isinstance(article_id, bool) or not isinstance(article_id, int) or article_id < 0:
            raise BridgeError("Infoblog article id has an unexpected schema")
        if not isinstance(title, str) or not title.strip():
            raise BridgeError("Infoblog article title has an unexpected schema")
        for label, index, dictionary in (
            ("audience", audience_index, audiences),
            ("program", program_index, programs),
        ):
            if isinstance(index, bool) or not isinstance(index, int):
                raise BridgeError(f"Infoblog {label} index has an unexpected schema")
            if index < 0 or index >= len(dictionary):
                raise BridgeError(f"Infoblog {label} index is out of bounds")
        if isinstance(views, bool) or not isinstance(views, int) or views < 0:
            raise BridgeError("Infoblog view count has an unexpected schema")
    return data


def read_cache(path: Path) -> dict[str, Any]:
    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BridgeError("cache cannot be read or is not valid JSON") from exc
    if not isinstance(envelope, dict) or envelope.get("schema_version") != CACHE_SCHEMA_VERSION:
        raise BridgeError("cache schema is unsupported")
    if envelope.get("index_url") != INDEX_URL:
        raise BridgeError("cache belongs to a different source")
    payload_text = envelope.get("payload_text")
    digest = envelope.get("payload_sha256")
    if not isinstance(payload_text, str) or not isinstance(digest, str):
        raise BridgeError("cache payload metadata is incomplete")
    if payload_sha256(payload_text) != digest:
        raise BridgeError("cache payload hash does not match")
    parse_index(payload_text)
    return envelope


def write_cache(path: Path, envelope: dict[str, Any]) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            json.dump(envelope, stream, ensure_ascii=False, separators=(",", ":"))
            stream.write("\n")
            temporary_name = stream.name
        os.replace(temporary_name, path)
    except OSError as exc:
        if temporary_name:
            try:
                Path(temporary_name).unlink(missing_ok=True)
            except OSError:
                pass
        raise BridgeError("cache could not be written") from exc


def _content_type(headers: Any) -> str:
    if hasattr(headers, "get_content_type"):
        return str(headers.get_content_type()).lower()
    value = headers.get("Content-Type", "") if headers is not None else ""
    return str(value).split(";", 1)[0].strip().lower()


def _source_metadata(
    envelope: dict[str, Any], *, retrieval: str, checked_at: str
) -> dict[str, Any]:
    return {
        "index_url": INDEX_URL,
        "retrieval": retrieval,
        "freshness": (
            "stale_unverified" if retrieval == "offline_cache" else "current_at_retrieval"
        ),
        "checked_at": checked_at,
        "fetched_at": envelope["fetched_at"],
        "etag": envelope.get("etag"),
        "last_modified": envelope.get("last_modified"),
        "payload_sha256": envelope["payload_sha256"],
    }


def load_index(
    *,
    cache_path: Path | None,
    offline: bool,
    timeout: float,
    opener: Any | None = None,
    checked_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    checked_at = checked_at or utc_now()
    cached = read_cache(cache_path) if cache_path is not None and cache_path.exists() else None

    if offline:
        if cached is None:
            raise BridgeError("offline mode requires an existing valid cache")
        return parse_index(cached["payload_text"]), _source_metadata(
            cached, retrieval="offline_cache", checked_at=checked_at
        )

    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if cached is not None:
        if isinstance(cached.get("etag"), str) and cached["etag"]:
            headers["If-None-Match"] = cached["etag"]
        if isinstance(cached.get("last_modified"), str) and cached["last_modified"]:
            headers["If-Modified-Since"] = cached["last_modified"]

    request = urllib.request.Request(INDEX_URL, headers=headers, method="GET")
    opener = opener or urllib.request.build_opener(NoRedirectHandler())
    try:
        response = opener.open(request, timeout=timeout)
    except urllib.error.HTTPError as exc:
        if exc.code == 304 and cached is not None:
            cached["validated_at"] = checked_at
            if cache_path is not None:
                write_cache(cache_path, cached)
            return parse_index(cached["payload_text"]), _source_metadata(
                cached, retrieval="not_modified_cache", checked_at=checked_at
            )
        raise BridgeError(f"Infoblog index request failed with HTTP {exc.code}") from exc
    except BridgeError:
        raise
    except (OSError, urllib.error.URLError) as exc:
        raise BridgeError("Infoblog index request failed") from exc

    with response:
        response_url = response.geturl()
        _require_fixed_url(response_url)
        if getattr(response, "status", 200) != 200:
            raise BridgeError("Infoblog index returned an unexpected status")
        if _content_type(response.headers) != "application/json":
            raise BridgeError("Infoblog index returned an unexpected content type")
        payload = response.read(MAX_RESPONSE_BYTES + 1)
        if len(payload) > MAX_RESPONSE_BYTES:
            raise BridgeError("Infoblog index exceeds the response size limit")
        try:
            payload_text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BridgeError("Infoblog index is not UTF-8") from exc
        data = parse_index(payload_text)
        envelope = {
            "schema_version": CACHE_SCHEMA_VERSION,
            "index_url": INDEX_URL,
            "fetched_at": checked_at,
            "validated_at": checked_at,
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "payload_sha256": payload_sha256(payload_text),
            "payload_text": payload_text,
        }
    if cache_path is not None:
        write_cache(cache_path, envelope)
    return data, _source_metadata(envelope, retrieval="network", checked_at=checked_at)


def _exact_dictionary_value(value: str | None, dictionary: list[str], label: str) -> str | None:
    if value is None:
        return None
    matches = [item for item in dictionary if item.casefold() == value.casefold()]
    if len(matches) != 1:
        raise BridgeError(f"unknown or ambiguous {label} filter")
    return matches[0]


def validate_search_terms(
    query: str | None, audience: str | None, program: str | None
) -> str:
    normalized_query = (query or "").strip()
    if normalized_query and len(normalized_query) < 2:
        raise BridgeError("query must contain at least two characters")
    if not normalized_query and audience is None and program is None:
        raise BridgeError("provide a query or at least one exact filter")
    for value in (normalized_query, audience or "", program or ""):
        if SENSITIVE_TERM.search(value):
            raise BridgeError("search terms contain credential-like or machine-path data")
    return normalized_query


def search_index(
    data: dict[str, Any],
    *,
    query: str | None,
    audience: str | None,
    program: str | None,
    limit: int,
) -> tuple[int, list[dict[str, Any]]]:
    normalized_query = validate_search_terms(query, audience, program)

    audiences: list[str] = data["a"]
    programs: list[str] = data["p"]
    audience_value = _exact_dictionary_value(audience, audiences, "audience")
    program_value = _exact_dictionary_value(program, programs, "program")
    words = [word.casefold() for word in normalized_query.split() if word]
    results: list[dict[str, Any]] = []
    total = 0
    for article_id, title, audience_index, program_index, views in data["r"]:
        title_folded = title.casefold()
        if words and not all(word in title_folded for word in words):
            continue
        row_audience = audiences[audience_index]
        row_program = programs[program_index]
        if audience_value is not None and row_audience != audience_value:
            continue
        if program_value is not None and row_program != program_value:
            continue
        total += 1
        if len(results) < limit:
            results.append(
                {
                    "id": article_id,
                    "title": title,
                    "audience": row_audience,
                    "program": row_program,
                    "views": views,
                    "url": ARTICLE_URL_TEMPLATE.format(article_id=f"{article_id:06d}"),
                }
            )
    return total, results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search the public Infoblog title index without sending the query to the site."
    )
    parser.add_argument("--query", help="Generic title words; keep case data out of the query")
    parser.add_argument("--audience", help="Exact audience value from the public index")
    parser.add_argument("--program", help="Exact program value from the public index")
    parser.add_argument("--limit", type=int, default=10, choices=range(1, 101), metavar="1..100")
    parser.add_argument("--cache", type=Path, help="Optional explicit cache file")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use an explicit cache without freshness validation; output is marked stale_unverified",
    )
    parser.add_argument("--timeout", type=float, default=20.0, help="Network timeout in seconds (1..60)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not 1 <= args.timeout <= 60:
        parser.error("--timeout must be between 1 and 60 seconds")
    if args.offline and args.cache is None:
        parser.error("--offline requires --cache")
    try:
        validate_search_terms(args.query, args.audience, args.program)
        data, source = load_index(
            cache_path=args.cache,
            offline=args.offline,
            timeout=args.timeout,
        )
        total, results = search_index(
            data,
            query=args.query,
            audience=args.audience,
            program=args.program,
            limit=args.limit,
        )
    except BridgeError as exc:
        print(f"incident search failed: {exc}", file=sys.stderr)
        return 2

    output = {
        "status": "OK",
        "query": args.query or "",
        "filters": {"audience": args.audience, "program": args.program},
        "source": source,
        "scope": "metadata_only_non_authoritative_leads",
        "total_matches": total,
        "returned": len(results),
        "results": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
