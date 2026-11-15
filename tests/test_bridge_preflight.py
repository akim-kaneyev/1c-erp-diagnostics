from __future__ import annotations

import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
from threading import Thread
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plugins/one-c-erp-diagnostics/ui'))
import bridge_doctor


class AuthRequired(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.send_response(self.server.result_status)
        self.end_headers()


class BridgePreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), AuthRequired)
        self.server.result_status = 401
        thread = Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.profile = {'label': 'Synthetic', 'test_contour': True,
                        'expected_metadata_name': 'Synthetic',
                        'base_url': f'http://127.0.0.1:{self.server.server_port}/demo/hs/velis-readonly'}
        self.config = self.root / 'apache.conf'
        self.config.write_text('Listen 127.0.0.1:9091\nLimitRequestBody 65536\n')
        self.vrd = self.root / 'default.vrd'
        self.xml = ('<point xmlns="http://v8.1c.ru/8.2/virtual-resource-system">'
                    '<ws pointEnableCommon="false"/>'
                    '<httpServices publishByDefault="false">'
                    '<service name="VelisReadOnlyBridge" rootUrl="velis-readonly" enable="true"/>'
                    '</httpServices></point>')
        self.vrd.write_text(self.xml)

    def inspect(self):
        return bridge_doctor.inspect(self.profile, apache_config=self.config, vrd=self.vrd)

    def test_literal_loopback_single_service_and_authentication(self):
        self.assertEqual(self.inspect()['status'], 'PASS')
        self.server.result_status = 200
        result = self.inspect()
        self.assertEqual(result['status'], 'FAIL')
        self.assertEqual(result['checks'][-1]['check'], 'http_authentication_required')

    def test_unreviewed_listener_include_or_overridden_limit_fails(self):
        for value in ('Listen 0.0.0.0:9091\nLimitRequestBody 65536\n',
                      'Listen 127.0.0.1:9091\nLimitRequestBody 65536\nInclude extra.conf\n',
                      'Listen 127.0.0.1:9091\nLimitRequestBody 65536\nLimitRequestBody 0\n'):
            with self.subTest(value=value):
                self.config.write_text(value)
                self.assertEqual(self.inspect()['status'], 'FAIL')

    def test_broader_http_or_common_web_publication_fails(self):
        for value in (self.xml.replace('publishByDefault="false"', 'publishByDefault="true"'),
                      self.xml.replace('</httpServices>', '<service name="Other" enable="true"/></httpServices>'),
                      self.xml.replace('pointEnableCommon="false"', 'pointEnableCommon="true"')):
            with self.subTest(value=value):
                self.vrd.write_text(value)
                self.assertEqual(self.inspect()['status'], 'FAIL')

    def test_shipped_native_artifact_matches_recorded_source_and_binary_hashes(self):
        bridge = ROOT / 'plugins/one-c-erp-diagnostics/bridge'
        manifest = json.loads((bridge / 'build.json').read_text())
        artifact = bridge / 'VelisReadOnlyBridge.cfe'
        self.assertEqual(hashlib.sha256(artifact.read_bytes()).hexdigest(), manifest['artifact_sha256'])
        sources = set()
        for path in (bridge / 'src').rglob('*'):
            if path.is_file():
                relative = path.relative_to(bridge / 'src').as_posix()
                sources.add(relative)
                data = path.read_bytes().replace(b'\r\n', b'\n')
                self.assertEqual(hashlib.sha256(data).hexdigest(), manifest['source_sha256'][relative])
        self.assertEqual(sources, set(manifest['source_sha256']))
        self.assertIn('independent_v8unpack_1.2.6_module_equality', manifest['checks'])


if __name__ == '__main__':
    unittest.main()
