#!/usr/bin/env python3
"""Serve the bundled read-only diagnostic viewer on IPv4 loopback."""

from __future__ import annotations

import argparse
import hashlib
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
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

    def __init__(self, port: int = 0, root: Path = DIST_ROOT):
        self.assets, self.manifest = load_assets(root)
        super().__init__(("127.0.0.1", port), ViewerHandler)


class ViewerHandler(BaseHTTPRequestHandler):
    server: ViewerServer
    server_version = "DiagnosticsViewer"
    sys_version = ""

    def log_message(self, _format: str, *_args) -> None:
        pass

    def _headers(self, status: int, mime: str, length: int) -> None:
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        self.end_headers()

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
        self._headers(405, "text/plain; charset=utf-8", 0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--open", action="store_true", help="Open the local URL in the default browser")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")
    with ViewerServer(args.port) as server:
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
