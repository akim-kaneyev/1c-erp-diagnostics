from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "plugins"
    / "one-c-erp-diagnostics"
    / "skills"
    / "one-c-erp-incident-search"
    / "scripts"
    / "search_infoblog.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("incident_search", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SEARCH = load_module()


def sample_data() -> dict:
    return {
        "a": ["Бухгалтер", "Разработчик"],
        "p": ["1С:ERP", "Платформа 1С"],
        "r": [
            [42, "Распределение расходов в 1С:ERP", 0, 0, 100],
            [7, "Проверка сервисов платформы", 1, 1, 50],
            [99, "Расходы будущих периодов", 0, 0, 25],
        ],
    }


def sample_payload() -> str:
    return json.dumps(sample_data(), ensure_ascii=False, separators=(",", ":"))


class FakeResponse:
    status = 200

    def __init__(self, payload: str):
        self.payload = payload.encode("utf-8")
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "ETag": '"synthetic"',
            "Last-Modified": "Thu, 01 Oct 2026 00:00:00 GMT",
        }

    def geturl(self) -> str:
        return SEARCH.INDEX_URL

    def read(self, _limit: int) -> bytes:
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


class FakeOpener:
    def __init__(self, payload: str):
        self.payload = payload
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        return FakeResponse(self.payload)


class NotModifiedOpener:
    def __init__(self):
        self.request = None

    def open(self, request, timeout):
        self.request = request
        raise urllib.error.HTTPError(request.full_url, 304, "Not Modified", {}, None)


class IncidentSearchTests(unittest.TestCase):
    def test_all_words_search_and_exact_filters_preserve_source_order(self) -> None:
        data = SEARCH.parse_index(sample_payload())
        total, results = SEARCH.search_index(
            data,
            query="расходов распределение",
            audience="бухгалтер",
            program="1с:erp",
            limit=10,
        )
        self.assertEqual(total, 1)
        self.assertEqual(results[0]["id"], 42)
        self.assertEqual(
            results[0]["url"],
            "https://infoblog.mywebguide.ru/articles/page_000042.html",
        )

    def test_malformed_index_fails_closed(self) -> None:
        malformed = json.dumps({"a": ["A"], "p": ["P"], "r": [[1, "T", 2, 0, 1]]})
        with self.assertRaisesRegex(SEARCH.BridgeError, "out of bounds"):
            SEARCH.parse_index(malformed)

    def test_query_is_never_sent_to_remote_source(self) -> None:
        opener = FakeOpener(sample_payload())
        data, source = SEARCH.load_index(
            cache_path=None,
            offline=False,
            timeout=5,
            opener=opener,
            checked_at="2026-10-05T00:00:00+00:00",
        )
        SEARCH.search_index(
            data,
            query="распределение расходов",
            audience=None,
            program=None,
            limit=5,
        )
        request, timeout = opener.requests[0]
        self.assertEqual(request.full_url, SEARCH.INDEX_URL)
        self.assertNotIn("распределение", request.full_url)
        self.assertNotIn("распределение", str(request.header_items()).casefold())
        self.assertEqual(timeout, 5)
        self.assertEqual(source["retrieval"], "network")
        self.assertEqual(source["freshness"], "current_at_retrieval")

    def test_sensitive_terms_are_rejected_before_network(self) -> None:
        with self.assertRaisesRegex(SEARCH.BridgeError, "credential-like"):
            SEARCH.validate_search_terms("token=synthetic-secret", None, None)
        with self.assertRaisesRegex(SEARCH.BridgeError, "machine-path"):
            machine_path = "C:\\" + "Us" + "ers\\synthetic\\case"
            SEARCH.validate_search_terms(machine_path, None, None)
        with self.assertRaisesRegex(SEARCH.BridgeError, "at least two"):
            SEARCH.validate_search_terms("x", None, None)

    def test_response_url_must_match_exact_fixed_origin(self) -> None:
        with self.assertRaisesRegex(SEARCH.BridgeError, "differs"):
            SEARCH._require_fixed_url(
                "https://user@infoblog.mywebguide.ru/data/search.json"
            )

    def test_tampered_cache_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cache.json"
            envelope = {
                "schema_version": SEARCH.CACHE_SCHEMA_VERSION,
                "index_url": SEARCH.INDEX_URL,
                "fetched_at": "2026-10-01T00:00:00+00:00",
                "validated_at": "2026-10-01T00:00:00+00:00",
                "etag": '"synthetic"',
                "last_modified": None,
                "payload_sha256": "0" * 64,
                "payload_text": sample_payload(),
            }
            path.write_text(json.dumps(envelope), encoding="utf-8")
            with self.assertRaisesRegex(SEARCH.BridgeError, "hash does not match"):
                SEARCH.read_cache(path)

    def test_offline_cache_is_explicitly_marked_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cache.json"
            payload = sample_payload()
            envelope = {
                "schema_version": SEARCH.CACHE_SCHEMA_VERSION,
                "index_url": SEARCH.INDEX_URL,
                "fetched_at": "2026-10-01T00:00:00+00:00",
                "validated_at": "2026-10-01T00:00:00+00:00",
                "etag": '"synthetic"',
                "last_modified": None,
                "payload_sha256": SEARCH.payload_sha256(payload),
                "payload_text": payload,
            }
            SEARCH.write_cache(path, envelope)
            _, source = SEARCH.load_index(
                cache_path=path,
                offline=True,
                timeout=5,
                checked_at="2026-10-05T00:00:00+00:00",
            )
            self.assertEqual(source["retrieval"], "offline_cache")
            self.assertEqual(source["freshness"], "stale_unverified")
            self.assertEqual(source["fetched_at"], "2026-10-01T00:00:00+00:00")

    def test_conditional_304_revalidates_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cache.json"
            payload = sample_payload()
            envelope = {
                "schema_version": SEARCH.CACHE_SCHEMA_VERSION,
                "index_url": SEARCH.INDEX_URL,
                "fetched_at": "2026-10-01T00:00:00+00:00",
                "validated_at": "2026-10-01T00:00:00+00:00",
                "etag": '"synthetic"',
                "last_modified": "Thu, 01 Oct 2026 00:00:00 GMT",
                "payload_sha256": SEARCH.payload_sha256(payload),
                "payload_text": payload,
            }
            SEARCH.write_cache(path, envelope)
            opener = NotModifiedOpener()
            _, source = SEARCH.load_index(
                cache_path=path,
                offline=False,
                timeout=5,
                opener=opener,
                checked_at="2026-10-05T00:00:00+00:00",
            )
            headers = dict(opener.request.header_items())
            self.assertEqual(headers["If-none-match"], '"synthetic"')
            self.assertIn("If-modified-since", headers)
            self.assertEqual(source["retrieval"], "not_modified_cache")
            self.assertEqual(source["freshness"], "current_at_retrieval")
            updated = SEARCH.read_cache(path)
            self.assertEqual(updated["validated_at"], "2026-10-05T00:00:00+00:00")

    def test_repository_entry_point_targets_packaged_script(self) -> None:
        wrapper = (ROOT / "tools" / "search_infoblog.py").read_text(encoding="utf-8")
        self.assertIn('"one-c-erp-incident-search"', wrapper)
        self.assertTrue(SCRIPT.is_file())


if __name__ == "__main__":
    unittest.main()
