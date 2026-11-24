import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch, MagicMock
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server
from tools.generate_audio import ssml_for
from tools.package import package


class LocalServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.port = cls.httpd.server_address[1]
        cls.url = f'http://127.0.0.1:{cls.port}'
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()

    def request(self, path, method='GET', body=None, headers=None):
        req = urllib.request.Request(self.url + path, data=body, method=method, headers=headers or {})
        try:
            with urllib.request.urlopen(req) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.read()

    def test_index_and_assets_served(self):
        for path in ['/', '/assets/app.js', '/assets/style.css']:
            self.assertEqual(self.request(path)[0], 200)

    def test_private_files_and_directory_traversal_blocked(self):
        for path in ['/.env', '/.git/config', '/.local/evidence/a.json', '/server.py', '/assets/../server.py', '/assets/%2e%2e/server.py', '/assets/']:
            self.assertEqual(self.request(path)[0], 404)

    def test_host_validation(self):
        self.assertEqual(self.request('/', headers={'Host':'attacker.example'})[0], 403)

    def test_health_does_not_expose_key(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY':'private-test-value','OPENAI_MODEL':'test-model'}):
            status, body = self.request('/api/health')
        self.assertEqual(status, 200)
        self.assertNotIn(b'private-test-value', body)
        self.assertTrue(json.loads(body)['openaiConfigured'])

    def test_cross_origin_post_blocked(self):
        self.assertEqual(self.request('/api/chat', 'POST', b'{}', {'Origin':'https://other.example','X-AEL-Request':'1'})[0], 403)

    def test_bad_prompt_rejected_before_service_call(self):
        with patch.object(server, 'call_openai') as call:
            code, _ = self.request('/api/chat', 'POST', b'{"prompt":99,"kind":"coach"}', {'Origin':self.url,'X-AEL-Request':'1'})
            self.assertEqual(code, 400)
            call.assert_not_called()

    def test_valid_request_uses_server_side_call(self):
        with patch.object(server, 'call_openai', return_value={'text':'mock only','request':{}}) as call:
            status, body = self.request('/api/chat','POST',json.dumps({'prompt':'Explain a tense.','kind':'coach','requestId':'test'}).encode(),{'Origin':self.url,'X-AEL-Request':'1'})
            self.assertEqual(status,200)
            call.assert_called_once_with('Explain a tense.','coach','test')
            self.assertEqual(json.loads(body)['text'],'mock only')


class IntegrationContractTests(unittest.TestCase):
    def test_provider_payload_and_unchanged_response_logging(self):
        raw='{"id":"mock","status":"completed","model":"test-model","output":[{"type":"message","content":[{"type":"output_text","text":"Mock explanation"}]}]}'
        response=MagicMock()
        response.__enter__.return_value.read.return_value=raw.encode()
        with patch.dict(os.environ,{'OPENAI_API_KEY':'test-key','OPENAI_MODEL':'test-model'}), patch.object(server.urllib.request,'urlopen',return_value=response) as network, patch.object(server,'record_evidence') as record:
            result=server.call_openai('Exact prompt','coach','test')
            request=network.call_args.args[0]
            body=json.loads(request.data)
            self.assertEqual(body['input'],'Exact prompt')
            self.assertFalse(body['store'])
            self.assertEqual(result['rawResponseText'],raw)
            record.assert_called_once()
            self.assertNotIn('test-key',json.dumps(result))

    def test_azure_xml_escape_and_two_speakers(self):
        text=ssml_for({'script':'Alex: A & B < C.\nMorgan: Yes.'},'AU')
        self.assertIn('A &amp; B &lt; C.',text)
        self.assertIn('en-AU-NatashaNeural',text)
        self.assertIn('en-AU-WilliamNeural',text)
        self.assertNotIn('Alex:',text)

    def test_portable_archive_excludes_secrets(self):
        path=package()
        with ZipFile(path) as archive:
            names=archive.namelist()
            self.assertIn('AEL-Classroom/index.html',names)
            self.assertIn('AEL-Classroom/.env.example',names)
            self.assertFalse(any('/.local/' in n or '/.git/' in n or n.endswith('/.env') for n in names))


if __name__=='__main__':
    unittest.main()
