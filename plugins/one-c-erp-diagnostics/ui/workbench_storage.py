"""Private profiles and immutable evidence; no credentials on disk."""
from __future__ import annotations

from datetime import datetime, timezone
import errno
import hashlib
import json
import os
from pathlib import Path
from threading import RLock
import uuid

from workbench_common import BRIDGE, CASE_STATE, MAX_BYTES, VERSION, WorkbenchError, exact, identifier, normalized_profile, public_json, require, text


def now():
    return datetime.now(timezone.utc).isoformat()


def initial_state(case_id):
    return {"schema_version": 1, "case_id": case_id, "evidence": [], "runs": [], "claims": [], "documents": [],
            "gates": [{"id": str(i), "status": "pending", "claim_ids": []} for i in range(11)],
            "active_index": {"run_id": None, "claim_ids": [], "document_ids": []}}


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = RLock()
        self._workspace_guard = None
        guard = self.root / ".workbench.lock"
        require(not guard.is_symlink() and guard.resolve().is_relative_to(self.root), "unsafe_storage_path")
        handle = guard.open("a+b")
        try:
            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            handle.close()
            code = "workspace_in_use" if error.errno in {errno.EACCES, errno.EAGAIN} else "workspace_lock_failed"
            raise WorkbenchError(code) from None
        self._workspace_guard = handle
        try:
            for folder in ("profiles", "cases"):
                self.path(folder).mkdir(exist_ok=True)
        except BaseException:
            self.close()
            raise

    def close(self):
        with self.lock:
            if self._workspace_guard is not None:
                # Closing releases the OS lock, including after process termination.
                # Keep the file: deleting it could let another process lock a new inode.
                self._workspace_guard.close()
                self._workspace_guard = None

    def path(self, *parts):
        require(self._workspace_guard is not None, "workspace_closed")
        candidate = self.root.joinpath(*parts)
        require(candidate.resolve().is_relative_to(self.root), "unsafe_storage_path")
        require(not candidate.is_symlink(), "unsafe_storage_path")
        return candidate

    def write(self, path, payload):
        data = public_json(payload)
        require(path.resolve().is_relative_to(self.root), "unsafe_storage_path")
        temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
        try:
            with temporary.open("xb") as stream:
                stream.write(data)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)

    def profiles(self):
        with self.lock:
            paths = sorted(self.path("profiles").glob("*.json"))
            require(len(paths) <= 100, "profile_limit")
            return [normalized_profile(json.loads(self.path("profiles", p.name).read_text(encoding="utf-8"))) for p in paths]

    def profile(self, profile_id):
        name = identifier(profile_id)
        path = self.path("profiles", name + ".json")
        require(path.is_file(), "profile_not_found")
        require(path.stat().st_size <= MAX_BYTES, "material_too_large")
        result = normalized_profile(json.loads(path.read_text(encoding="utf-8")))
        require(result.get("id") == profile_id, "profile_identity_mismatch")
        return result

    def save_profile(self, payload):
        result = normalized_profile(payload)
        result.setdefault("id", "P-" + uuid.uuid4().hex)
        with self.lock:
            require(len(self.profiles()) < 100 or self.path("profiles", result["id"] + ".json").is_file(), "profile_limit")
            self.write(self.path("profiles", result["id"] + ".json"), result)
        return result

    def case(self, case_id):
        path = self.path("cases", identifier(case_id), "case.json")
        require(path.is_file(), "case_not_found")
        require(path.stat().st_size <= MAX_BYTES, "material_too_large")
        result = json.loads(path.read_text(encoding="utf-8"))
        require(result["state"]["case_id"] == case_id, "case_identity_mismatch")
        require(CASE_STATE.validate_state(result["state"])["status"] == "PASS", "case_state_invalid")
        public_json(result)
        return result

    def cases(self):
        with self.lock:
            paths = sorted(self.path("cases").iterdir())
            require(len(paths) <= 500, "case_limit")
            result = []
            for path in paths:
                if path.is_dir() and valid_case_id(path.name):
                    case = self.case(path.name)
                    result.append({"id": path.name, "title": case["annotations"]["title"],
                                   "evidence_count": len(case["state"]["evidence"])})
            return result

    def create_case(self, payload):
        exact(payload, {"case_id", "title", "goal"})
        case_id = identifier(payload["case_id"])
        result = {"viewer_schema_version": 1, "state": initial_state(case_id),
                  "annotations": {"title": text(payload["title"], 200), "goal": text(payload["goal"], 1000), "records": {},
                                  "coverage": {"total": None, "limitation": "Собраны отдельные источники; полнота учётных данных не установлена."}}}
        public_json(result)
        with self.lock:
            folder = self.path("cases", case_id)
            require(not folder.exists(), "case_exists")
            require(len(self.cases()) < 500, "case_limit")
            folder.mkdir()
            self.write(folder / "case.json", result)
            self.write(folder / "notes.json", {"notes": "", "updated_at": now()})
        return result

    def notes(self, case_id, value=None):
        with self.lock:
            self.case(case_id)
            path = self.path("cases", identifier(case_id), "notes.json")
            if value is not None:
                self.write(path, {"notes": text(value, 10000, empty=True), "updated_at": now()})
            return json.loads(path.read_text(encoding="utf-8"))

    def add_artifact(self, case_id, title, content, *, source, limitations, parents=(), capture_id=None,
                     evidence_id=None, raw_bytes=None):
        with self.lock:
            case = self.case(case_id)
            require(len(case["state"]["evidence"]) < 5000, "evidence_limit")
            known = {item["id"] for item in case["state"]["evidence"]}
            require(set(parents) <= known, "evidence_reference_missing")
            evidence_id = identifier(evidence_id) if evidence_id is not None else "E-" + uuid.uuid4().hex[:16]
            require(evidence_id not in known, "evidence_exists")
            canonical = public_json(content)
            raw = canonical if raw_bytes is None else raw_bytes
            require(len(raw) <= MAX_BYTES and BRIDGE.encode(json.loads(raw)) == canonical, "artifact_content_mismatch")
            record = {"id": evidence_id, "status": "active", "artifact_hash": hashlib.sha256(raw).hexdigest(),
                      "derived_from": list(parents), "run_id": None,
                      "transformation": source if parents else None, "tool": "VelisWorkbench" if parents else None,
                      "tool_version": VERSION if parents else None, "limitations": list(limitations),
                      "superseded_by": None, "invalidates_ids": []}
            case["state"]["evidence"].append(record)
            case["annotations"]["records"][evidence_id] = {"title": title, "description": "Наблюдение; учётный вывод не принят." + (" Capture: " + capture_id if capture_id else ""), "source": source, "date": now()[:10]}
            require(CASE_STATE.validate_state(case["state"])["status"] == "PASS", "case_state_invalid")
            artifact = self.path("cases", case_id, evidence_id + ".json")
            require(not artifact.exists(), "artifact_exists")
            with artifact.open("xb") as stream:
                stream.write(raw)
            self.write(self.path("cases", case_id, "case.json"), case)
            return {"evidence_id": evidence_id, "sha256": record["artifact_hash"], "case": case}

    def artifact(self, case_id, evidence_id):
        with self.lock:
            case = self.case(case_id)
            selected = [item for item in case["state"]["evidence"] if item["id"] == evidence_id]
            require(len(selected) == 1, "evidence_not_found")
            path = self.path("cases", identifier(case_id), identifier(evidence_id) + ".json")
            data = path.read_bytes()
            require(hashlib.sha256(data).hexdigest() == selected[0]["artifact_hash"], "artifact_hash_mismatch")
            return json.loads(data)

    def report(self, case_id):
        with self.lock:
            case, notes = self.case(case_id), self.notes(case_id)
            lines = ["# " + case["annotations"]["title"], "", "Цель: " + case["annotations"]["goal"],
                     "", "Статус: материалы собраны; учётная причина не установлена.", "", "## Источники", ""]
            for item in case["state"]["evidence"]:
                self.artifact(case_id, item["id"])
                label = case["annotations"]["records"][item["id"]]["title"]
                lines += ["- " + item["id"] + ": " + label, "  SHA-256: " + item["artifact_hash"]]
                lines.extend("  Ограничение: " + x for x in item["limitations"])
            lines += ["", "## Заметки", "", notes["notes"] or "Не добавлены.", "", "## Следующий шаг", "", "Независимо сверить полноту данных, аналитику и причинную цепочку. Gate 0–10 автоматически не закрывались."]
            return "\n".join(lines) + "\n"


def valid_case_id(value):
    try:
        identifier(value)
        return True
    except ValueError:
        return False
