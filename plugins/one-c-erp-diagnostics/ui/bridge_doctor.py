"""Read-only connection preflight. No installation, database writes or saved secrets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from workbench_common import BRIDGE, normalized_profile


def inspect(profile, *, apache_config=None, vrd=None, web_module=None):
    profile = normalized_profile(profile)
    checks = [{"check": "explicit_test_profile", "status": "PASS"}]
    if web_module is not None:
        checks.append({"check": "1c_web_module", "status": "PASS" if Path(web_module).is_file() else "FAIL"})
    if apache_config is not None:
        raw = Path(apache_config).read_text(encoding="utf-8-sig")
        lines = [line.strip() for line in raw.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        listeners = [line.split(None, 1)[1] for line in lines if re.match(r"(?i)^Listen\s", line)]
        safe = bool(listeners) and all(re.fullmatch(r"127\.0\.0\.1:\d+|\[::1\]:\d+", item) for item in listeners)
        # Included config could add listeners; an unreviewed include is not considered verified.
        safe = safe and not any(re.match(r"(?i)^Include(?:Optional)?\s", line) for line in lines)
        checks.append({"check": "apache_literal_loopback_only", "status": "PASS" if safe else "FAIL"})
        limits = [line.split(None, 1)[1] for line in lines if re.match(r"(?i)^LimitRequestBody\s", line)]
        checks.append({"check": "apache_request_body_limit", "status": "PASS" if limits == ["65536"] else "FAIL"})
    if vrd is not None:
        root = ET.fromstring(Path(vrd).read_bytes())
        ns = {"v": "http://v8.1c.ru/8.2/virtual-resource-system"}
        services = root.find("v:httpServices", ns)
        allowed = services is not None and services.get("publishByDefault") == "false"
        if allowed:
            enabled = [node for node in services if node.get("enable") == "true"]
            allowed = len(enabled) == 1 and enabled[0].get("name") == "VelisReadOnlyBridge" and enabled[0].get("rootUrl") == "velis-readonly"
        checks.append({"check": "publication_single_readonly_service", "status": "PASS" if allowed else "FAIL"})
        ws = root.find("v:ws", ns)
        ws_disabled = ws is not None and ws.get("pointEnableCommon") == "false" and not list(ws)
        checks.append({"check": "publication_other_web_services_disabled", "status": "PASS" if ws_disabled else "FAIL"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), BRIDGE.NoRedirect())
    try:
        with opener.open(profile["base_url"] + "/health", timeout=5) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code
        error.close()
    except (OSError, urllib.error.URLError):
        status = None
    checks.append({"check": "http_authentication_required", "status": "PASS" if status == 401 else "FAIL", "http_status": status})
    return {"schema_version": 1, "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
            "checks": checks, "limitations": ["Configuration files are checked only when explicitly supplied.",
            "This preflight does not authenticate, attest the running binary or prove business correctness."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--apache-config", type=Path)
    parser.add_argument("--vrd", type=Path)
    parser.add_argument("--web-module", type=Path)
    args = parser.parse_args()
    try:
        result = inspect(json.loads(args.profile.read_text(encoding="utf-8-sig")), apache_config=args.apache_config, vrd=args.vrd, web_module=args.web_module)
        print(json.dumps(result, ensure_ascii=True))
        raise SystemExit(0 if result["status"] == "PASS" else 1)
    except (ValueError, OSError, ET.ParseError):
        print('{"status":"FAIL","reason":"invalid_profile_or_local_config"}')
        raise SystemExit(1)
