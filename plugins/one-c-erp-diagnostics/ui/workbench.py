"""Authenticated read capture and private diagnostic workspaces."""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import secrets
from threading import Lock, RLock, Timer
import time
import uuid
import zipfile

from workbench_common import BRIDGE, MAX_BYTES, VERSION, WorkbenchError, exact, identifier, public_json, require, text
from workbench_scenarios import execute, examples
from workbench_storage import Store

SESSION_SECONDS = 900


class Session:
    def __init__(self, profile, credentials, health):
        self.profile, self.credentials, self.health = profile, credentials, health
        self.created = time.monotonic()
        self.lock = Lock()
        self.metadata = {}
        self.timer = None

    def __repr__(self):
        return "<Session: redacted>"


class Workbench:
    def __init__(self, root):
        self.store = Store(root)
        self.csrf = secrets.token_urlsafe(32)
        self.sessions = {}
        self.lock = RLock()

    def cleanup(self):
        with self.lock:
            for key in list(self.sessions):
                if time.monotonic() - self.sessions[key].created >= SESSION_SECONDS:
                    self.disconnect(key)

    def disconnect(self, session_id):
        with self.lock:
            selected = self.sessions.pop(session_id, None)
            if selected is not None and selected.timer is not None:
                selected.timer.cancel()

    def close(self):
        with self.lock:
            for key in list(self.sessions):
                self.disconnect(key)

    def bootstrap(self):
        self.cleanup()
        return {"version": VERSION, "csrf": self.csrf, "profiles": self.store.profiles(),
                "cases": self.store.cases(), "session_minutes": 15,
                "scenarios": [{"id": key, "example": value, "synthetic": True} for key, value in examples().items()]}

    def session(self, session_id):
        self.cleanup()
        require(isinstance(session_id, str), "sign_in_required")
        with self.lock:
            selected = self.sessions.get(session_id)
            require(selected is not None, "sign_in_required")
            current = self.store.profile(selected.profile["id"])
            if current != selected.profile:
                self.disconnect(session_id)
                raise WorkbenchError("profile_changed_sign_in_again")
            return selected

    def connect(self, body):
        exact(body, {"profile_id", "username", "password"})
        self.cleanup()
        with self.lock:
            require(len(self.sessions) < 32, "session_limit")
        profile = self.store.profile(body["profile_id"])
        credentials = BRIDGE.Credentials(profile["base_url"], body["username"], body["password"])
        raw = BRIDGE.request(profile["base_url"], None, 30, credentials=credentials)
        health = BRIDGE.decode(raw)
        BRIDGE.validate_health(health, profile["expected_metadata_name"])
        session_id = secrets.token_urlsafe(32)
        with self.lock:
            require(len(self.sessions) < 32, "session_limit")
            self.sessions[session_id] = Session(profile, credentials, health)
            timer = Timer(SESSION_SECONDS, self.disconnect, args=(session_id,))
            timer.daemon = True
            self.sessions[session_id].timer = timer
            timer.start()
        return {"session_id": session_id, "health": health,
                "server_read_only": health.get("service") == "VelisReadOnlyBridge" and health.get("readOnly") is True}

    def capture(self, body):
        exact(body, {"session_id", "case_id", "operation"}, {"kind", "name", "uuid"})
        session = self.session(body["session_id"])
        case_id, operation = identifier(body["case_id"]), body["operation"]
        require(operation in {"health", "metadata", "probe", "describe", "document.header"}, "operation_not_read_only")
        self.store.case(case_id)
        require(session.lock.acquire(blocking=False), "read_already_running")
        try:
            profile = session.profile
            identity = {key: profile[key] for key in ("base_url", "expected_metadata_name", "contour_note")}
            with self.store.lock:
                context_file = self.store.path("cases", case_id, "contour.json")
                if context_file.exists():
                    require(json.loads(context_file.read_text(encoding="utf-8")) == identity, "case_contour_mismatch")
            strict = session.health.get("service") == "VelisReadOnlyBridge"
            kwargs = {}
            actual_operation = operation
            analytic = "connectivity:" + profile["base_url"]
            if operation == "metadata":
                kwargs["sections"] = ["catalogs", "documents", "enums", "informationRegisters", "accumulationRegisters"]
            elif operation == "probe":
                actual_operation = "query"
                if strict:
                    kwargs = {"queryId": "probe.typed", "params": {"text": "Проверка UTF-8 — 1С", "number": 27.125, "flag": True}, "limit": 2}
                else:
                    kwargs = {"text": "ВЫБРАТЬ 1 КАК X", "params": {}, "limit": 2}
            elif operation in {"describe", "document.header"}:
                kind, name = body.get("kind", "document"), body.get("name")
                collection = {"document": "documents", "catalog": "catalogs", "enum": "enums"}.get(kind)
                require(collection is not None and isinstance(name, str), "metadata_object_required")
                require(name in {item["name"] for item in session.metadata.get(collection, [])}, "metadata_must_be_loaded")
                analytic = kind + ":" + name
                if operation == "describe":
                    kwargs = {"kind": kind, "name": name}
                else:
                    require(strict and kind == "document", "read_only_bridge_required")
                    actual_operation = "query"
                    kwargs = {"queryId": "document.header", "params": {"name": name, "uuid": body.get("uuid")}, "limit": 1}
                    analytic += ":" + str(body.get("uuid"))
            payload = BRIDGE.build_payload(actual_operation, **kwargs)
            evidence_id = "E-" + uuid.uuid4().hex[:16]
            capture_key = "CAP-" + uuid.uuid4().hex
            directory = self.store.path("cases", case_id, "captures")
            directory.mkdir(exist_ok=True)
            output = self.store.path("cases", case_id, "captures", capture_key)
            context = {"case_id": case_id, "evidence_ids": [evidence_id], "analytic_key": analytic}
            manifest = BRIDGE.capture(base_url=profile["base_url"], expected_metadata_name=profile["expected_metadata_name"],
                                      test_contour=True, operation=actual_operation, payload=payload, output=output,
                                      timeout=30, credentials=session.credentials, **context)
            BRIDGE.verify(output, **context)
            raw = (output / "response.json").read_bytes()
            response = BRIDGE.decode(raw)
            if operation == "probe":
                require(response["count"] == 1, "probe_result_mismatch")
                row = response["rows"][0]
                if strict:
                    require(row == {"text": "Проверка UTF-8 — 1С", "number": 27.125, "flag": True}, "probe_result_mismatch")
                else:
                    cell = row.get("X")
                    require(cell == 1 or cell == {"type": "Число", "presentation": "1"}, "probe_result_mismatch")
            if operation == "metadata":
                session.metadata = response
            limitations = ["Это наблюдение из выбранного тестового контура, не подтверждение корректности учёта.",
                           "Имя конфигурации само по себе не является уникальным идентификатором базы."]
            if operation == "document.header":
                limitations.append("Только шапка выбранного документа; движения и табличные части не входят в снимок.")
            with self.store.lock:
                if context_file.exists():
                    require(json.loads(context_file.read_text(encoding="utf-8")) == identity, "case_contour_mismatch")
                else:
                    self.store.write(context_file, identity)
                source_file = self.store.path("cases", case_id, "sources.json")
                sources = json.loads(source_file.read_text(encoding="utf-8")) if source_file.exists() else {}
                sources[evidence_id] = {"capture_key": capture_key, "manifest_sha256": hashlib.sha256((output / "manifest.json").read_bytes()).hexdigest()}
                self.store.write(source_file, sources)
                result = self.store.add_artifact(case_id, {"health": "Проверка подключения", "metadata": "Метаданные 1С",
                    "probe": "Контрольный запрос", "describe": "Описание объекта", "document.header": "Шапка документа"}[operation],
                    response, source="bridge:" + operation, limitations=limitations,
                    capture_id=manifest["run_id"], evidence_id=evidence_id, raw_bytes=raw)
            return {**result, "response": response, "capture_run_id": manifest["run_id"]}
        finally:
            session.lock.release()

    def scenario(self, body):
        exact(body, {"case_id", "scenario", "input"}, {"synthetic"})
        case_id = identifier(body["case_id"])
        self.store.case(case_id)
        result = execute(body["scenario"], body["input"])
        source = self.store.add_artifact(case_id, "Строки для проверки", body["input"], source="user-selected JSON",
            limitations=["Учебные данные." if body.get("synthetic") is True else "Полнота и смысл исходной выгрузки отдельно не подтверждены."])
        derived = self.store.add_artifact(case_id, "Результат: " + body["scenario"], result,
            source="scenario:" + body["scenario"], limitations=result["limitations"], parents=[source["evidence_id"]])
        return {**derived, "result": result}

    def compare_documents(self, body):
        exact(body, {"session_id", "case_id", "name", "left_uuid", "right_uuid"})
        require(body["left_uuid"] != body["right_uuid"], "two_different_documents_required")
        for key in ("left_uuid", "right_uuid"):
            BRIDGE.build_payload("query", queryId="document.header", params={"name": body["name"], "uuid": body[key]}, limit=1)
        common = {"session_id": body["session_id"], "case_id": body["case_id"], "operation": "document.header", "kind": "document", "name": body["name"]}
        left = self.capture({**common, "uuid": body["left_uuid"]})
        right = self.capture({**common, "uuid": body["right_uuid"]})
        require(left["response"]["count"] == right["response"]["count"] == 1, "selected_document_not_found")
        a, b = left["response"]["rows"][0], right["response"]["rows"][0]
        require(set(a) == set(b) and {"ref"} < set(a), "document_header_contract")
        require(a["ref"].lower() == body["left_uuid"].lower() and b["ref"].lower() == body["right_uuid"].lower(), "document_reference_mismatch")
        values = sorted(set(a) - {"ref"})
        payload = {"key_fields": ["selected_document"], "value_fields": values,
                   "left": [{"selected_document": "header", **{k: a[k] for k in values}}],
                   "right": [{"selected_document": "header", **{k: b[k] for k in values}}]}
        result = execute("compare", payload)
        result["limitations"].append("Сравнены только шапки двух явно выбранных документов; движения и табличные части отдельно не проверены.")
        derived = self.store.add_artifact(body["case_id"], "Сравнение шапок документов", result,
            source="scenario:document-headers", limitations=result["limitations"],
            parents=[left["evidence_id"], right["evidence_id"]])
        return {**derived, "result": result}

    def export(self, case_id, format):
        case_id = identifier(case_id)
        case = self.store.case(case_id)
        if format == "json":
            return public_json(case), "application/json", case_id + ".json"
        if format == "markdown":
            return self.store.report(case_id).encode("utf-8"), "text/markdown; charset=utf-8", case_id + ".md"
        require(format == "zip", "unsupported_export")
        with self.store.lock:
            case = self.store.case(case_id)
            files = {"case.json": public_json(case), "notes.json": public_json(self.store.notes(case_id)),
                     "report.md": self.store.report(case_id).encode("utf-8")}
            for item in case["state"]["evidence"]:
                self.store.artifact(case_id, item["id"])
                files[item["id"] + ".json"] = self.store.path("cases", case_id, item["id"] + ".json").read_bytes()
            sources_file = self.store.path("cases", case_id, "sources.json")
            sources = json.loads(sources_file.read_text(encoding="utf-8")) if sources_file.exists() else {}
            required_sources = {item["id"] for item in case["state"]["evidence"]
                                if case["annotations"]["records"][item["id"]]["source"].startswith("bridge:")}
            require(required_sources <= set(sources), "capture_source_missing")
            for evidence_id in sorted(required_sources):
                source = sources[evidence_id]
                key = identifier(source["capture_key"])
                folder = self.store.path("cases", case_id, "captures", key)
                require(hashlib.sha256((folder / "manifest.json").read_bytes()).hexdigest() == source["manifest_sha256"], "capture_manifest_changed")
                manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
                BRIDGE.verify(folder, case_id=case_id, evidence_ids=manifest["evidence_ids"], analytic_key=manifest["analytic_key"])
                for name in ("manifest.json", "request.json", "health.json", "response.json"):
                    files["captures/" + key + "/" + name] = self.store.path("cases", case_id, "captures", key, name).read_bytes()
            require(sum(map(len, files.values())) <= 64 * 1024 * 1024, "export_size_limit")
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, data in files.items():
                    archive.writestr(name, data)
            return output.getvalue(), "application/zip", case_id + ".zip"

    def dispatch(self, path, body):
        if path == "/api/profile":
            return self.store.save_profile(body)
        if path == "/api/connect":
            return self.connect(body)
        if path == "/api/disconnect":
            exact(body, {"session_id"})
            require(isinstance(body["session_id"], str), "sign_in_required")
            self.disconnect(body["session_id"])
            return {"disconnected": True}
        if path == "/api/case/create":
            return self.store.create_case(body)
        if path == "/api/case":
            exact(body, {"case_id"})
            return {"bundle": self.store.case(body["case_id"]), "notes": self.store.notes(body["case_id"])}
        if path == "/api/notes":
            exact(body, {"case_id", "notes"})
            return self.store.notes(body["case_id"], body["notes"])
        if path == "/api/capture":
            return self.capture(body)
        if path == "/api/scenario":
            return self.scenario(body)
        if path == "/api/compare-documents":
            return self.compare_documents(body)
        if path == "/api/artifact":
            exact(body, {"case_id", "evidence_id"})
            return self.store.artifact(body["case_id"], body["evidence_id"])
        raise WorkbenchError("unknown_api")
