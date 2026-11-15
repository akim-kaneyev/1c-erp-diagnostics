from __future__ import annotations

import base64
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
import socket
import subprocess
from pathlib import Path
import sys
import tempfile
from threading import Thread
import time
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request
import zipfile

CREDENTIAL_FIELD = "password"  # Synthetic negative-test payload field.
ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "plugins/one-c-erp-diagnostics/ui"
sys.path.insert(0, str(UI))
from workbench import Workbench
from workbench_common import BRIDGE, CASE_STATE, WorkbenchError
from workbench_scenarios import execute, examples
from serve_ui import ViewerServer


class TestBridge(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, value, status=200):
        raw = BRIDGE.encode(value)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def authorized(self):
        self.server.calls.append(self.command)
        expected = "Basic " + base64.b64encode("Учебный:synthetic-only".encode()).decode()
        if self.headers.get("Authorization") != expected:
            self.respond({"ok": False}, 401)
            return False
        return True

    def do_GET(self):
        if self.authorized():
            self.respond({"ok": True, "service": "VelisReadOnlyBridge", "metadataName": self.server.metadata_name,
                          "readOnly": True, "contractVersion": 1, "bridgeVersion": "0.1.0"})

    def do_POST(self):
        if not self.authorized():
            return
        value = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.server.payloads.append(value)
        if value["command"] == "Metadata":
            self.respond({"ok": True, "metadataName": "Synthetic", **{key: ([{"name": "SyntheticDoc", "synonym": "Учебный документ"}] if key == "documents" else []) for key in value["sections"]}})
        elif value["command"] == "Describe":
            self.respond({"ok": True, "object": {"name": value["name"]}, "attributes": [], "tableParts": []})
        elif value.get("queryId") == "probe.typed":
            self.respond({"ok": True, "count": 1, "rows": [value["params"]]})
        elif value.get("queryId") == "document.header":
            ref = value["params"]["uuid"]
            self.respond({"ok": True, "count": 1, "rows": [{"ref": ref, "number": "1" if ref.endswith("1") else "2", "posted": True}]})
        else:
            self.respond({"ok": False}, 403)


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.bridge = ThreadingHTTPServer(("127.0.0.1", 0), TestBridge)
        self.bridge.calls, self.bridge.payloads, self.bridge.metadata_name = [], [], "Synthetic"
        self.thread = Thread(target=self.bridge.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.bridge.server_close)
        self.addCleanup(self.bridge.shutdown)
        self.base = f"http://127.0.0.1:{self.bridge.server_port}/demo/hs/velis-readonly"
        self.app = Workbench(Path(self.tmp.name) / "private")
        self.addCleanup(self.app.close)
        self.profile = self.app.store.save_profile({"label": "Учебная база", "base_url": self.base, "expected_metadata_name": "Synthetic", "test_contour": True})
        self.app.store.create_case({"case_id": "CASE-TEST", "title": "Учебный разбор", "goal": "Проверить только учебные данные"})

    def sign_in(self):
        return self.app.connect({"profile_id": self.profile["id"], "username": "Учебный", CREDENTIAL_FIELD: "synthetic-only"})["session_id"]

    def capture(self, session_id, operation, **kwargs):
        return self.app.capture({"session_id": session_id, "case_id": "CASE-TEST", "operation": operation, **kwargs})

    def test_authenticated_capture_keeps_exact_source_and_no_password(self):
        session = self.sign_in()
        receipt = self.capture(session, "probe")
        self.assertTrue(self.bridge.payloads[-1]["queryId"].startswith("probe."))
        case = receipt["case"]
        self.assertEqual(CASE_STATE.validate_state(case["state"])["status"], "PASS")
        self.assertTrue(all(gate["status"] == "pending" for gate in case["state"]["gates"]))
        record = case["state"]["evidence"][0]
        raw = (self.app.store.root / "cases/CASE-TEST" / (record["id"] + ".json")).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), record["artifact_hash"])
        self.assertEqual(json.loads(raw)["rows"], [{"text": "Проверка UTF-8 — 1С", "number": 27.125, "flag": True}])
        self.assertNotIn("synthetic-only", repr(self.app.sessions))
        self.app.close()
        for file in self.app.store.root.rglob("*"):
            if file.is_file():
                self.assertNotIn(b"synthetic-only", file.read_bytes())

    def test_wrong_identity_and_authentication_do_not_create_session(self):
        self.bridge.metadata_name = "Other"
        with self.assertRaisesRegex(BRIDGE.BridgeError, "test_configuration_mismatch"):
            self.sign_in()
        self.assertFalse(self.app.sessions)
        self.assertFalse(self.bridge.payloads)
        self.bridge.metadata_name = "Synthetic"
        with self.assertRaisesRegex(BRIDGE.BridgeError, "http_error_401"):
            self.app.connect({"profile_id": self.profile["id"], "username": "Учебный", CREDENTIAL_FIELD: "wrong-synthetic"})
        self.assertFalse(self.app.sessions)

    def test_session_password_is_discarded_on_timer_without_another_request(self):
        with patch("workbench.SESSION_SECONDS", 0.05):
            session = self.sign_in()
            timer = self.app.sessions[session].timer
            timer.join(timeout=2)
        self.assertNotIn(session, self.app.sessions)

    def test_disconnect_and_server_close_cancel_session_timers(self):
        session = self.sign_in()
        timer = self.app.sessions[session].timer
        self.app.dispatch("/api/disconnect", {"session_id": session})
        timer.join(timeout=2)
        self.assertFalse(timer.is_alive())
        self.assertFalse(self.app.sessions)
        session = self.sign_in()
        timer = self.app.sessions[session].timer
        self.app.close()
        timer.join(timeout=2)
        self.assertFalse(timer.is_alive())
        self.assertFalse(self.app.sessions)

    def test_expiry_profile_change_and_missing_scope_block_network(self):
        session = self.sign_in()
        before = len(self.bridge.calls)
        self.app.sessions[session].created = time.monotonic() - 901
        with self.assertRaisesRegex(WorkbenchError, "sign_in_required"):
            self.capture(session, "health")
        session = self.sign_in()
        self.app.store.save_profile({**self.profile, "label": "Changed"})
        with self.assertRaisesRegex(WorkbenchError, "profile_changed"):
            self.capture(session, "health")
        self.assertEqual(len(self.bridge.calls), before + 1)
        with self.assertRaisesRegex(WorkbenchError, "test_contour_required"):
            self.app.store.save_profile({**self.profile, "test_contour": False})

    def test_query_text_and_unobserved_object_are_refused_before_read(self):
        session = self.sign_in()
        before = len(self.bridge.calls)
        with self.assertRaisesRegex(WorkbenchError, "invalid_fields"):
            self.capture(session, "probe", text="ANY")
        with self.assertRaisesRegex(WorkbenchError, "metadata_must_be_loaded"):
            self.capture(session, "describe", kind="document", name="Invented")
        with self.assertRaisesRegex(WorkbenchError, "operation_not_read_only"):
            self.capture(session, "ExecuteBSL")
        self.assertEqual(len(self.bridge.calls), before)

    def test_metadata_describe_and_explicit_document_comparison(self):
        session = self.sign_in()
        self.capture(session, "metadata")
        description = self.capture(session, "describe", kind="document", name="SyntheticDoc")
        self.assertEqual(description["response"]["object"]["name"], "SyntheticDoc")
        result = self.app.compare_documents({"session_id": session, "case_id": "CASE-TEST", "name": "SyntheticDoc",
            "left_uuid": "00000000-0000-0000-0000-000000000001", "right_uuid": "00000000-0000-0000-0000-000000000002"})
        self.assertEqual(result["result"]["difference_count"], 1)
        derived = result["case"]["state"]["evidence"][-1]
        self.assertEqual(len(derived["derived_from"]), 2)
        self.assertEqual(CASE_STATE.validate_state(result["case"]["state"])["status"], "PASS")
        self.assertEqual(result["result"]["differences"][0]["field"], "number")

    def test_case_contour_cannot_be_silently_replaced(self):
        self.capture(self.sign_in(), "health")
        profile2 = self.app.store.save_profile({**self.profile, "contour_note": "Different test contour"})
        session = self.app.connect({"profile_id": profile2["id"], "username": "Учебный", CREDENTIAL_FIELD: "synthetic-only"})["session_id"]
        before = len(self.bridge.calls)
        with self.assertRaisesRegex(WorkbenchError, "case_contour_mismatch"):
            self.capture(session, "health")
        self.assertEqual(len(self.bridge.calls), before)

    def test_zip_contains_only_verified_case_sources(self):
        receipt = self.capture(self.sign_in(), "health")
        (self.app.store.root / "cases/CASE-TEST/private.env").write_text("do not export", encoding="utf-8")
        self.app.store.notes("CASE-TEST", "Заметка пользователя")
        raw, mime, filename = self.app.export("CASE-TEST", "zip")
        self.assertEqual((mime, filename), ("application/zip", "CASE-TEST.zip"))
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            self.assertIn("case.json", archive.namelist())
            self.assertIn(receipt["evidence_id"] + ".json", archive.namelist())
            self.assertTrue(any(name.endswith("manifest.json") for name in archive.namelist()))
            self.assertNotIn("private.env", archive.namelist())
            self.assertNotIn(b"synthetic-only", b"".join(archive.read(name) for name in archive.namelist()))
        artifact = self.app.store.root / "cases/CASE-TEST" / (receipt["evidence_id"] + ".json")
        artifact.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(WorkbenchError, "artifact_hash_mismatch"):
            self.app.export("CASE-TEST", "zip")

    def test_paths_secrets_and_duplicate_case_are_rejected(self):
        with self.assertRaisesRegex(WorkbenchError, "invalid_id"):
            self.app.store.case("../../outside")
        with self.assertRaisesRegex(WorkbenchError, "invalid_fields"):
            self.app.store.save_profile({**self.profile, CREDENTIAL_FIELD: "synthetic-only"})
        with self.assertRaisesRegex(WorkbenchError, "credentials_in_material"):
            self.app.store.notes("CASE-TEST", f"{CREDENTIAL_FIELD}=synthetic-only")
        with self.assertRaisesRegex(WorkbenchError, "case_exists"):
            self.app.store.create_case({"case_id": "CASE-TEST", "title": "Other", "goal": "Other"})

    def test_human_notes_and_scenario_keep_original_hashes_and_gate_status(self):
        source = self.capture(self.sign_in(), "health")
        original = source["case"]["state"]["evidence"][0]
        output = self.app.scenario({"case_id": "CASE-TEST", "scenario": "allocation", "input": examples()["allocation"], "synthetic": True})
        self.assertEqual(output["result"]["validation_status"], "PASS")
        self.assertEqual(output["case"]["state"]["evidence"][0], original)
        self.assertEqual(CASE_STATE.validate_state(output["case"]["state"])["status"], "PASS")
        self.app.store.notes("CASE-TEST", "Нужно сверить первичные документы")
        report = self.app.store.report("CASE-TEST")
        self.assertIn("учётная причина не установлена", report)
        self.assertIn("Нужно сверить", report)
        self.assertEqual(self.app.store.case("CASE-TEST")["state"]["claims"], [])


class ScenarioTests(unittest.TestCase):
    def test_extreme_decimal_exponents_are_refused_before_fraction_conversion(self):
        for number in ('1e-999999999', '1e999999999', '0e999999999', 'NaN', 'Infinity'):
            value = examples()['compare']
            value['left'][0]['quantity'] = number
            with self.subTest(number=number), patch('workbench_scenarios.Fraction') as conversion:
                with self.assertRaisesRegex(WorkbenchError, 'invalid_decimal'):
                    execute('compare', value)
                conversion.assert_not_called()

    def test_allocation_checks_row_and_observed_number_bounds_before_analysis(self):
        for section in ('rows', 'observed'):
            value = examples()['allocation']
            if section == 'rows':
                value['dataset']['rows'][0]['fact'] = '1e-999999999'
            else:
                value['dataset']['observed_allocation']['by_analytic'][0]['amount'] = '1e-999999999'
            with self.subTest(section=section), patch('workbench_scenarios.ACCOUNTING.analyze_dataset') as analysis:
                with self.assertRaisesRegex(WorkbenchError, 'invalid_decimal'):
                    execute('allocation', value)
                analysis.assert_not_called()

    def test_numeric_comparison_preserves_exact_values_and_rejects_ambiguous_keys(self):
        value = examples()["compare"]
        result = execute("compare", value)
        self.assertEqual(result["difference_count"], 1)
        value["right"][0]["quantity"] = "10.000"
        self.assertEqual(execute("compare", value)["difference_count"], 0)
        value["left"].append(dict(value["left"][0]))
        with self.assertRaisesRegex(WorkbenchError, "ambiguous_duplicate_key"):
            execute("compare", value)

    def test_negative_stock_is_bound_to_provided_analytics(self):
        value = examples()["negative-stock"]
        result = execute("negative-stock", value)
        self.assertEqual(result["negative_count"], 1)
        value["rows"][0]["quantity"] = "0"
        self.assertEqual(execute("negative-stock", value)["negative_count"], 0)
        value["rows"][0].pop("series")
        with self.assertRaisesRegex(WorkbenchError, "invalid_row"):
            execute("negative-stock", value)

    def test_allocation_detects_wrong_observed_distribution(self):
        value = examples()["allocation"]
        result = execute("allocation", value)
        self.assertEqual(result["validation_status"], "PASS")
        value["dataset"]["observed_allocation"]["by_analytic"][0]["amount"] = "12"
        self.assertEqual(execute("allocation", value)["validation_status"], "FAIL")


class WorkbenchHTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.server = ViewerServer(data_dir=Path(self.tmp.name))
        Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.origin = "http://127.0.0.1:" + str(self.server.server_port)
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), BRIDGE.NoRedirect())

    def request(self, path, payload=None, **headers):
        data = None if payload is None else BRIDGE.encode(payload)
        req = urllib.request.Request(self.origin + path, data=data,
            headers={"Content-Type": "application/json", **headers})
        try:
            with self.opener.open(req, timeout=5) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read() or b"{}")

    def test_api_requires_exact_host_origin_and_csrf(self):
        status, bootstrap = self.request("/api/bootstrap")
        self.assertEqual(status, 200)
        token = bootstrap["data"]["csrf"]
        body = {"case_id": "CASE-HTTP", "title": "Учебный", "goal": "Проверить"}
        self.assertEqual(self.request("/api/case/create", body)[0], 403)
        self.assertEqual(self.request("/api/case/create", body, Origin="http://outside.invalid", **{"X-Diagnostics-CSRF": token})[0], 403)
        self.assertEqual(self.request("/api/case/create", body, Origin=self.origin, **{"X-Diagnostics-CSRF": "wrong"})[0], 403)
        self.assertEqual(self.request("/api/case/create", body, Origin=self.origin, **{"X-Diagnostics-CSRF": token})[0], 200)
        self.assertEqual(self.request("/api/bootstrap", Host="outside.invalid")[0], 403)

    def test_api_cannot_invoke_arbitrary_tools_or_save_credentials(self):
        token = self.request("/api/bootstrap")[1]["data"]["csrf"]
        headers = {"Origin": self.origin, "X-Diagnostics-CSRF": token}
        self.assertEqual(self.request("/api/ExecuteBSL", {"code": "synthetic"}, **headers)[0], 400)
        self.assertEqual(self.request("/api/profile", {CREDENTIAL_FIELD: "synthetic-only"}, **headers)[0], 400)
        self.assertEqual(list(Path(self.tmp.name).rglob("*.json")), [])


class WorkspaceOwnershipTests(unittest.TestCase):
    def test_process_exit_releases_lock_without_deleting_the_lock_file(self):
        with tempfile.TemporaryDirectory() as directory:
            script = "import os,sys; sys.path.insert(0,sys.argv[1]); from workbench import Workbench; app=Workbench(sys.argv[2]); os._exit(0)"
            child = subprocess.run([sys.executable, '-c', script, str(UI), directory], capture_output=True, text=True, timeout=15)
            self.assertEqual(child.returncode, 0, child.stderr)
            self.assertTrue((Path(directory) / '.workbench.lock').is_file())
            reopened = Workbench(directory)
            reopened.close()

    def test_another_process_is_refused_and_can_reopen_after_owner_closes(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Workbench(directory)
            script = (
                "import sys; sys.path.insert(0,sys.argv[1]); "
                "from workbench import Workbench; from workbench_common import WorkbenchError; "
                "exec('try:\\n app=Workbench(sys.argv[2])\\n app.close()\\nexcept WorkbenchError as error:\\n print(str(error))\\n sys.exit(17)')"
            )
            try:
                blocked = subprocess.run([sys.executable, '-c', script, str(UI), directory], capture_output=True, text=True, timeout=15)
                self.assertEqual(blocked.returncode, 17, blocked.stderr)
                self.assertEqual(blocked.stdout.strip(), 'workspace_in_use')
                with self.assertRaisesRegex(WorkbenchError, 'workspace_in_use'):
                    Workbench(directory)
            finally:
                app.close()
            reopened = subprocess.run([sys.executable, '-c', script, str(UI), directory], capture_output=True, text=True, timeout=15)
            self.assertEqual(reopened.returncode, 0, reopened.stderr)

    def test_failed_server_bind_releases_workspace_ownership(self):
        with tempfile.TemporaryDirectory() as directory, socket.socket() as occupied:
            occupied.bind(('127.0.0.1', 0))
            occupied.listen()
            with self.assertRaises(OSError):
                ViewerServer(occupied.getsockname()[1], data_dir=Path(directory))
            reopened = Workbench(directory)
            reopened.close()


if __name__ == "__main__":
    unittest.main()
