from __future__ import annotations

import hashlib
import http.client
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "plugins/one-c-erp-diagnostics/ui"


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


viewer = module_at("diagnostic_viewer", UI / "serve_ui.py")
state_validator = module_at("viewer_state_validator", ROOT / "plugins/one-c-erp-diagnostics/skills/one-c-erp-case-state/scripts/validate_case_state.py")


class DiagnosticViewerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = viewer.ViewerServer()
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join(timeout=3)

    def request(self, path="/", method="GET", headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        try:
            connection.request(method, path, headers=headers or {})
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def test_actual_bundled_index_health_and_all_asset_hashes(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")
        status, headers, body = self.request()
        self.assertEqual(status, 200)
        self.assertIn(b'<html lang="ru">', body)
        self.assertIn("script-src 'self'", headers["Content-Security-Policy"])
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        status, _, health = self.request("/health")
        self.assertEqual(json.loads(health)["version"], "0.4.0")
        for item in self.server.manifest["files"]:
            status, _, content = self.request("/" + item["path"])
            self.assertEqual(status, 200)
            self.assertEqual(hashlib.sha256(content).hexdigest(), item["sha256"])

    def test_does_not_expose_files_uploads_or_foreign_origins(self):
        for path in ("/../serve_ui.py", "/%2e%2e/serve_ui.py", "/STATE.json", "/assets/", "/.git/config"):
            self.assertEqual(self.request(path)[0], 404)
        self.assertEqual(self.request(headers={"Host": "untrusted.example"})[0], 403)
        self.assertEqual(self.request(headers={"Origin": "https://untrusted.example"})[0], 403)
        self.assertEqual(self.request(method="POST")[0], 405)
        self.assertEqual(self.request(method="HEAD")[2], b"")

    def test_asset_tampering_fails_before_startup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("changed", encoding="utf-8")
            (root / "build.json").write_text(json.dumps({"files": [{"path": "index.html", "sha256": "0" * 64}]}))
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                viewer.load_assets(root)

    def test_bundle_contains_synthetic_case_and_runtime_licenses(self):
        example = json.loads((UI / "dist/example.json").read_text(encoding="utf-8"))
        self.assertIs(example["annotations"]["synthetic"], True)
        self.assertEqual(len(example["state"]["evidence"]), 3)
        validation = state_validator.validate_state(example["state"])
        self.assertEqual(validation["status"], "PASS", validation["errors"])
        self.assertIn("@ui-sdk/core", (UI / "dist/THIRD_PARTY_NOTICES.txt").read_text(encoding="utf-8"))
        self.assertIn("Apache", (UI / "dist/THIRD_PARTY_NOTICES.txt").read_text(encoding="utf-8"))

    def test_build_tracks_current_sources_and_package_version(self):
        manifest = json.loads((UI / "dist/build.json").read_text(encoding="utf-8"))
        plugin = json.loads((UI.parent / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], plugin["version"])
        for item in manifest["sources"]:
            source = (ROOT / item["path"]).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
            self.assertEqual(hashlib.sha256(source.encode()).hexdigest(), item["sha256"], item["path"])


if __name__ == "__main__":
    unittest.main()
