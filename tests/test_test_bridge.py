from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/one-c-erp-diagnostics/skills/one-c-erp-test-bridge/scripts/test_bridge.py"
spec = importlib.util.spec_from_file_location("test_bridge_adapter", SCRIPT)
BRIDGE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BRIDGE)


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requests = []
        cls.health = {"ok": True, "service": "CodexTestBridge", "metadataName": "Demo"}
        cls.reply = {"ok": True, "rows": [{"Значение": "Тест"}], "count": 1}
        cls.status = 200
        cls.content_type = "application/json"

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                cls.requests.append(("GET", self.path, None))
                self.respond(cls.health)

            def do_POST(self):
                raw = self.rfile.read(int(self.headers["Content-Length"]))
                cls.requests.append(("POST", self.path, json.loads(raw.decode("utf-8"))))
                self.respond(cls.reply)

            def respond(self, value):
                raw = value if isinstance(value, bytes) else BRIDGE.encode(value)
                self.send_response(cls.status)
                self.send_header("Content-Type", cls.content_type)
                self.send_header("Location", "http://192.0.2.1/forbidden")
                self.end_headers()
                try:
                    self.wfile.write(raw)
                except (ConnectionError, OSError):
                    pass

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/demo/hs/codex-test"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.__class__.requests = []
        self.__class__.status = 200
        self.__class__.content_type = "application/json"
        self.__class__.health = {"ok": True, "service": "CodexTestBridge", "metadataName": "Demo"}
        self.__class__.reply = {"ok": True, "rows": [{"Значение": "Тест"}], "count": 1}
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "capture"
        self.context = {"case_id": "CASE-SYNTHETIC", "evidence_ids": ["E-SYNTHETIC"], "analytic_key": "demo/period"}

    def capture(self, operation="query", **overrides):
        options = dict(base_url=self.url, expected_metadata_name="Demo", test_contour=True,
                       operation=operation, payload=overrides.get("payload") if "payload" in overrides else
                       BRIDGE.build_payload(operation, text="ВЫБРАТЬ 1 КАК Значение", limit=1),
                       output=self.output, **self.context)
        options.update(overrides)
        return BRIDGE.capture(**options)

    def test_utf8_request_and_exact_response_hash_with_offline_verification(self):
        result = self.capture()
        self.assertEqual(self.requests[0], ("GET", "/demo/hs/codex-test/health", None))
        self.assertEqual(self.requests[1][1], "/demo/hs/codex-test/command")
        self.assertEqual(self.requests[1][2], {"command": "Query", "text": "ВЫБРАТЬ 1 КАК Значение", "params": {}, "limit": 1})
        self.assertEqual(result["files"]["response.json"]["sha256"], BRIDGE.sha256((self.output / "response.json").read_bytes()))
        self.assertTrue(result["coverage"]["limit_reached"])
        self.assertFalse(result["coverage"]["population_complete"])
        self.assertEqual(BRIDGE.verify(self.output, **self.context)["freshness"], "not_verified")
        self.assertEqual(result["protocol_reference"]["installed_bridge_commit"], "not_attested_by_health")

    def test_sample_below_limit_never_proves_population_coverage(self):
        result = self.capture(payload=BRIDGE.build_payload("query", text="ВЫБРАТЬ 1 КАК X", limit=10))
        self.assertFalse(result["coverage"]["limit_reached"])
        self.assertFalse(result["coverage"]["population_complete"])

    def test_health_only_does_not_send_command(self):
        self.capture("health")
        self.assertEqual(len(self.requests), 1)
        BRIDGE.verify(self.output, **self.context)

    def test_metadata_and_describe_contracts(self):
        self.__class__.reply = {"ok": True, "metadataName": "Demo", **{key: [] for key in BRIDGE.SECTIONS}}
        self.capture("metadata")
        BRIDGE.verify(self.output, **self.context)
        self.__class__.reply = {"ok": True, "object": {}, "attributes": [], "tableParts": []}
        self.capture("describe", output=Path(self.temp.name) / "description",
                     payload=BRIDGE.build_payload("describe", kind="catalog", name="Тест"))

    def test_wrong_configuration_stops_before_query(self):
        self.__class__.health["metadataName"] = "Other"
        with self.assertRaisesRegex(BRIDGE.BridgeError, "test_configuration_mismatch"):
            self.capture()
        self.assertEqual(len(self.requests), 1)
        self.assertFalse((self.output / "manifest.json").exists())

    def test_contour_declaration_and_command_allowlist_prevent_network_calls(self):
        for changes in [dict(test_contour=False), dict(operation="execute-bsl"),
                        dict(payload={"command": "ExecuteBSL", "text": "x", "limit": 1, "params": {}}),
                        dict(case_id=""), dict(timeout=float("nan"))]:
            with self.subTest(changes=changes), self.assertRaises(BRIDGE.BridgeError):
                self.capture(**changes)
        self.assertEqual(self.requests, [])

    def test_endpoint_rejection_before_network(self):
        for url in ["http://localhost/demo/hs/codex-test", "https://127.0.0.1/demo/hs/codex-test",
                    "http://192.0.2.1/demo/hs/codex-test", "http://127.0.0.2/demo/hs/codex-test",
                    "http://user@127.0.0.1/demo/hs/codex-test", self.url + "?x=1", self.url + "#x",
                    self.url.replace("demo", "../demo"), self.url.replace("demo", "%64emo"),
                    self.url.replace("demo", "demo\\evil"), self.url + "/command"]:
            with self.subTest(url=url), self.assertRaises(BRIDGE.BridgeError):
                self.capture(base_url=url)
        self.assertEqual(self.requests, [])
        self.assertEqual(BRIDGE.normalize_url("http://[::1]:8080/demo/hs/codex-test/"), "http://[::1]:8080/demo/hs/codex-test")

    def test_proxy_is_disabled(self):
        with patch.dict("os.environ", {"http_proxy": "http://192.0.2.1:1", "HTTP_PROXY": "http://192.0.2.1:1", "no_proxy": "", "NO_PROXY": ""}):
            self.capture("health")

    def test_redirects_http_errors_and_html_are_failures(self):
        for status, content_type in [(302, "application/json"), (500, "application/json"), (200, "text/html")]:
            self.__class__.status, self.__class__.content_type = status, content_type
            with self.subTest(status=status), self.assertRaises(BRIDGE.BridgeError):
                BRIDGE.request(self.url, None, 2)
        self.assertEqual(len(self.requests), 3)

    def test_malformed_oversized_and_ambiguous_json_rejected(self):
        for raw in [b"[]", b"<html>", b'{"ok":true,"ok":false}', b'{"x":NaN}', b'{"x":1e999}', b'{"x":"\xff"}', b" " * (BRIDGE.MAX_BYTES + 1)]:
            with self.subTest(length=len(raw)), self.assertRaises(BRIDGE.BridgeError):
                BRIDGE.decode(raw)

    def test_application_failure_and_inconsistent_rows_are_failures(self):
        for response in [{"ok": False}, {"ok": 1}, {"ok": True, "rows": [], "count": 1},
                         {"ok": True, "rows": [{}], "count": True}, {"ok": True, "rows": [1], "count": 1},
                         {"ok": True, "rows": [{}, {}], "count": 2}]:
            with self.subTest(response=response), self.assertRaises(BRIDGE.BridgeError):
                BRIDGE.validate_response("query", response, {"limit": 1}, "Demo")

    def test_tampering_and_context_reuse_rejected(self):
        self.capture()
        for context in [dict(self.context, case_id="OTHER"), dict(self.context, evidence_ids=["OTHER"]),
                        dict(self.context, analytic_key="OTHER")]:
            with self.assertRaisesRegex(BRIDGE.BridgeError, "evidence_context_mismatch"):
                BRIDGE.verify(self.output, **context)
        (self.output / "response.json").write_bytes(b'{"ok":true}')
        with self.assertRaisesRegex(BRIDGE.BridgeError, "artifact_hash_mismatch"):
            BRIDGE.verify(self.output, **self.context)

    def test_coverage_cannot_be_promoted_by_editing_manifest(self):
        self.capture()
        manifest_path = self.output / "manifest.json"
        manifest = BRIDGE.decode(manifest_path.read_bytes())
        manifest["coverage"]["population_complete"] = True
        manifest_path.write_bytes(BRIDGE.encode(manifest))
        with self.assertRaisesRegex(BRIDGE.BridgeError, "coverage_mismatch"):
            BRIDGE.verify(self.output, **self.context)

    def test_existing_directory_never_overwritten(self):
        self.output.mkdir()
        sentinel = self.output / "keep.txt"
        sentinel.write_text("keep")
        with self.assertRaisesRegex(BRIDGE.BridgeError, "new_output_directory_required"):
            self.capture()
        self.assertEqual(sentinel.read_text(), "keep")
        self.assertEqual(self.requests, [])

    def test_cli_query_and_verify_end_to_end(self):
        query_path = Path(self.temp.name) / "query.txt"
        query_path.write_text("ВЫБРАТЬ 1 КАК X", encoding="utf-8-sig")
        common = ["--case-id", "CASE-SYNTHETIC", "--evidence-id", "E-SYNTHETIC", "--analytic-key", "demo/period"]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(BRIDGE.main(["capture", "query", "--test-contour", "--base-url", self.url,
                                         "--expected-metadata-name", "Demo", "--query-file", str(query_path),
                                         "--output", str(self.output), *common]), 0)
            self.assertEqual(BRIDGE.main(["verify", "--bundle", str(self.output), *common]), 0)

    def test_cli_does_not_echo_server_error_or_bad_input(self):
        self.__class__.health = {"ok": False, "error": "SYNTHETIC-PRIVATE-TEXT"}
        stream = io.StringIO()
        with contextlib.redirect_stderr(stream):
            code = BRIDGE.main(["capture", "health", "--test-contour", "--base-url", self.url,
                                "--expected-metadata-name", "Demo", "--output", str(self.output),
                                "--case-id", "C", "--evidence-id", "E", "--analytic-key", "K"])
        self.assertEqual(code, 1)
        self.assertNotIn("SYNTHETIC-PRIVATE-TEXT", stream.getvalue())

    def test_installed_script_runs_without_repository_or_upstream_files(self):
        installed = Path(self.temp.name) / "installed"
        installed.mkdir()
        copied = installed / "test_bridge.py"
        shutil.copyfile(SCRIPT, copied)
        result = subprocess.run([sys.executable, str(copied), "capture", "health", "--test-contour",
                                 "--base-url", self.url, "--expected-metadata-name", "Demo",
                                 "--output", str(self.output), "--case-id", "C", "--evidence-id", "E",
                                 "--analytic-key", "K"], cwd=installed, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "captured")
        BRIDGE.verify(self.output, case_id="C", evidence_ids=["E"], analytic_key="K")

    def test_transport_response_limit_applies_before_json_decoding(self):
        self.__class__.health = b" " * (BRIDGE.MAX_BYTES + 1)
        with self.assertRaisesRegex(BRIDGE.BridgeError, "response_too_large"):
            BRIDGE.request(self.url, None, 2)

    def test_unreachable_endpoint_is_explicit_failure(self):
        from unittest.mock import Mock
        from urllib.error import URLError

        opener = Mock()
        opener.open.side_effect = URLError("SYNTHETIC-PRIVATE-TEXT")
        with patch.object(BRIDGE.urllib.request, "build_opener", return_value=opener):
            with self.assertRaisesRegex(BRIDGE.BridgeError, "bridge_unreachable_or_timeout"):
                BRIDGE.request(self.url, None, 2)


if __name__ == "__main__":
    unittest.main()
