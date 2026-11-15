#!/usr/bin/env python3
"""Serve the bundled read-only diagnostic viewer on IPv4 loopback."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import sys
from urllib.parse import unquote, urlsplit
import webbrowser

UI_ROOT = Path(__file__).resolve().parent
DIST_ROOT = UI_ROOT / "dist"


def load_assets(root: Path = DIST_ROOT) -> tuple[dict[str, bytes], dict]:
    manifest = json.loads((root / "build.json").read_text(encoding="utf-8"))
    assets = {}
    for item in manifest["files"]:
        relative = item["path"]
        path = (root / relative).resolve()
        path.relative_to(root.resolve())
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != item["sha256"]:
            raise ValueError(f"Viewer asset hash mismatch: {relative}")
        assets["/" + relative] = content
    if "/index.html" not in assets:
        raise ValueError("Viewer build has no index.html")
    assets["/"] = assets["/index.html"]
    return assets, manifest


class ViewerServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, port: int = 0, root: Path = DIST_ROOT, *, data_dir: Path | None = None):
        self.assets, self.manifest = load_assets(root)
        self.workbench = None
        if data_dir is not None:
            sys.path.insert(0, str(UI_ROOT))
            from workbench import Workbench
            self.workbench = Workbench(data_dir)
        super().__init__(("127.0.0.1", port), ViewerHandler)

    def server_close(self):
        if self.workbench is not None:
            self.workbench.close()
        super().server_close()


class ViewerHandler(BaseHTTPRequestHandler):
    server: ViewerServer
    server_version = "DiagnosticsViewer"
    sys_version = ""

    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def log_message(self, _format: str, *_args) -> None:
        pass

    def _headers(self, status: int, mime: str, length: int) -> None:
        self.send_response(status)
        self._security_headers(mime, length)
        self.end_headers()

    def _security_headers(self, mime: str, length: int) -> None:
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")

    def _allowed(self) -> bool:
        port = self.server.server_address[1]
        hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        origin = self.headers.get("Origin")
        return self.headers.get("Host") in hosts and (origin is None or origin in {"http://" + host for host in hosts})

    def _read(self, head_only: bool = False) -> None:
        if not self._allowed():
            self._headers(403, "text/plain; charset=utf-8", 0)
            return
        try:
            path = unquote(urlsplit(self.path).path, errors="strict")
        except (ValueError, UnicodeError):
            path = ""
        if path == "/api/bootstrap" and self.server.workbench is not None:
            if not self._api_origin(post=False):
                self._headers(403, "application/json", 0)
                return
            try:
                self._json(200, {"ok": True, "data": self.server.workbench.bootstrap()}, head_only)
            except (OSError, ValueError, TypeError, KeyError):
                self._json(400, {"ok": False, "reason": "workspace_unavailable"}, head_only)
            return
        if path == "/health":
            content = json.dumps({"application": "one-c-diagnostics-viewer", "version": self.server.manifest["version"]}).encode()
            mime = "application/json"
        elif path in self.server.assets:
            content = self.server.assets[path]
            mime = "application/octet-stream"
            for suffix, content_type in (
                (".js", "text/javascript"), (".mjs", "text/javascript"),
                (".css", "text/css"), (".json", "application/json"),
                (".png", "image/png"), (".txt", "text/plain; charset=utf-8"),
                (".html", "text/html; charset=utf-8"),
            ):
                if path.endswith(suffix):
                    mime = content_type
                    break
            if path == "/":
                mime = "text/html; charset=utf-8"
        else:
            self._headers(404, "text/plain; charset=utf-8", 0)
            return
        self._headers(200, mime, len(content))
        if not head_only:
            try:
                self.wfile.write(content)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def do_GET(self) -> None:
        self._read()

    def do_HEAD(self) -> None:
        self._read(head_only=True)

    def do_POST(self) -> None:
        if self.server.workbench is None:
            self._headers(405, "text/plain; charset=utf-8", 0)
            return
        from workbench_common import BRIDGE, MAX_BYTES, WorkbenchError, exact
        try:
            if not self._api_origin(post=True):
                self._json(403, {"ok": False, "reason": "local_origin_required"})
                return
            token = self.headers.get("X-Diagnostics-CSRF", "")
            if not secrets.compare_digest(token, self.server.workbench.csrf):
                self._json(403, {"ok": False, "reason": "csrf_required"})
                return
            if self.headers.get("Content-Type", "").lower() != "application/json" or self.headers.get("Transfer-Encoding"):
                raise WorkbenchError("json_content_type_required")
            length = int(self.headers.get("Content-Length", "-1"))
            if not 0 <= length <= MAX_BYTES:
                raise WorkbenchError("request_size_limit")
            body = BRIDGE.decode(self.rfile.read(length))
            path = urlsplit(self.path)
            if path.query or path.fragment or path.path != self.path:
                raise WorkbenchError("unknown_api")
            if path.path == "/api/export":
                exact(body, {"case_id", "format"})
                data, mime, filename = self.server.workbench.export(body["case_id"], body["format"])
                self.send_response(200)
                self.send_header("Content-Disposition", 'attachment; filename="' + filename + '"')
                self._security_headers(mime, len(data))
                self.end_headers()
                self.wfile.write(data)
                return
            result = self.server.workbench.dispatch(path.path, body)
            self._json(200, {"ok": True, "data": result})
        except (BRIDGE.BridgeError, WorkbenchError) as exc:
            reason = str(exc)
            status = 401 if reason in {"http_error_401", "sign_in_required"} else 400
            self._json(status, {"ok": False, "reason": reason})
        except (OSError, ValueError, TypeError, KeyError, RecursionError):
            self._json(400, {"ok": False, "reason": "invalid_request_or_workspace"})

    def _api_origin(self, *, post):
        authority = f"127.0.0.1:{self.server.server_address[1]}"
        origin = self.headers.get("Origin")
        return (self.headers.get("Host") == authority
                and (origin == "http://" + authority if post else origin in {None, "http://" + authority})
                and self.headers.get("Sec-Fetch-Site") in {None, "none", "same-origin"})

    def _json(self, status, payload, head_only=False):
        data = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self._headers(status, "application/json; charset=utf-8", len(data))
        if not head_only:
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--open", action="store_true", help="Open the local URL in the default browser")
    parser.add_argument("--workbench", action="store_true", help="Enable the explicit local connection and case workspace")
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--profile", type=Path, help="Import an explicitly selected test profile without credentials")
    parser.add_argument("--test-contour", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")
    if (args.data_dir or args.profile) and not args.workbench:
        parser.error("--workbench is required for workspace options")
    if args.profile and not args.test_contour:
        parser.error("--test-contour is required to import a selected test profile")
    data_dir = None
    if args.workbench:
        data_dir = args.data_dir or Path(os.environ.get("LOCALAPPDATA", str(Path.home() / ".local/share"))) / "VelisDiagnostics"
    with ViewerServer(args.port, data_dir=data_dir) as server:
        if args.profile:
            sys.path.insert(0, str(UI_ROOT))
            from workbench_common import CASE_STATE, MAX_BYTES, normalized_profile
            if args.profile.stat().st_size > MAX_BYTES:
                parser.error("profile is too large")
            profile = json.loads(args.profile.read_text(encoding="utf-8-sig"))
            if CASE_STATE.contains_credential_like_content(profile):
                parser.error("profile contains credential-like fields")
            if isinstance(profile.get("test_contour"), dict):
                contour = profile["test_contour"]
                profile = {"label": contour.get("label", "Selected test contour"), "base_url": profile["base_url"],
                           "expected_metadata_name": profile["expected_metadata_name"], "test_contour": True,
                           "contour_note": str(contour.get("server", "")) + "/" + str(contour.get("infobase", ""))}
            imported = normalized_profile(profile)
            if not any(p["base_url"] == imported["base_url"] and p["expected_metadata_name"] == imported["expected_metadata_name"] for p in server.workbench.store.profiles()):
                server.workbench.store.save_profile(imported)
        url = f"http://127.0.0.1:{server.server_address[1]}/"
        print(f"1C ERP Diagnostics Viewer {server.manifest['version']}\nLocal: {url}\nStop: Ctrl+C", flush=True)
        if args.open:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
