"""Shared, local-only workbench boundaries."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
VERSION = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
MAX_BYTES = 4 * 1024 * 1024
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")


class WorkbenchError(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise WorkbenchError(code)


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, PLUGIN_ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


BRIDGE = load_module("velis_bridge_client", "skills/one-c-erp-test-bridge/scripts/test_bridge.py")
CASE_STATE = load_module("velis_case_state", "skills/one-c-erp-case-state/scripts/validate_case_state.py")
ACCOUNTING = load_module("velis_accounting", "skills/one-c-erp-diagnose-core/scripts/accounting_invariants.py")


def public_json(value):
    require(not CASE_STATE.contains_credential_like_content(value), "credentials_in_material")
    data = BRIDGE.encode(value)
    require(len(data) <= MAX_BYTES, "material_too_large")
    return data


def text(value, maximum=500, *, empty=False):
    require(isinstance(value, str) and len(value) <= maximum and (empty or bool(value.strip())), "invalid_text")
    return value.strip()


def identifier(value):
    require(isinstance(value, str) and SAFE_ID.fullmatch(value) is not None, "invalid_id")
    return value


def exact(value, keys, optional=()):
    require(isinstance(value, dict) and set(keys) <= set(value) <= set(keys) | set(optional), "invalid_fields")


def normalized_profile(value):
    exact(value, {"label", "base_url", "expected_metadata_name", "test_contour"}, {"id", "contour_note"})
    require(value["test_contour"] is True, "test_contour_required")
    result = {"label": text(value["label"], 100), "base_url": BRIDGE.normalize_url(value["base_url"]),
              "expected_metadata_name": text(value["expected_metadata_name"], 100),
              "test_contour": True, "contour_note": text(value.get("contour_note", ""), 500, empty=True)}
    if "id" in value:
        result["id"] = identifier(value["id"])
    public_json(result)
    return result
