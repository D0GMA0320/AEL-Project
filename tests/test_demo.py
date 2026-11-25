import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from demo_security import DemoSecurity, valid_public_origin
import server
class DemoTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.origin=Path(self.temp.name)/'origin.txt'
        self.origin.write_text('https://class-test.trycloudflare.com')
        self.sec=DemoSecurity('test-classroom-code',self.origin,max_calls=2)
        self.httpd=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);self.httpd.demo_security=self.sec
        self.port=self.httpd.server_address[1];self.thread=threading.Thread(target=self.httpd.serve_forever,daemon=True);self.thread.start()
    def tearDown(self):
        self.httpd.shutdown();self.httpd.server_close();self.thread.join();self.temp.cleanup()
    def request(self,path,body=None,cookie=None,origin='https://class-test.trycloudflare.com',host='class-test.trycloudflare.com'):
        headers={'Host':host,'Origin':origin,'X-AEL-Request':'1','Content-Type':'application/json'}
        if cookie:headers['Cookie']=cookie
        req=urllib.request.Request(f'http://127.0.0.1:{self.port}'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        try:
            with urllib.request.urlopen(req) as r:return r.status,r.read(),r.headers
        except urllib.error.HTTPError as e:return e.code,e.read(),e.headers
    def login(self):
        status,body,headers=self.request('/api/session',{'code':'test-classroom-code'})
        self.assertEqual(status,200);self.assertIn('HttpOnly',headers['Set-Cookie']);self.assertIn('Secure',headers['Set-Cookie'])
        return headers['Set-Cookie'].split(';')[0]
    def test_anonymous_health_and_audio_blocked(self):
        self.assertEqual(self.request('/api/health')[0],401);self.assertEqual(self.request('/assets/audio/meeting-US.mp3')[0],401);self.assertEqual(self.request('/')[0],200)
    def test_login_host_and_origin(self):
        self.assertEqual(self.request('/api/session',{'code':'wrong'})[0],401)
        for kwargs in [{'origin':'https://attacker.example'},{'host':'attacker.example'}]:self.assertEqual(self.request('/api/session',{'code':'test-classroom-code'},**kwargs)[0],403)
        self.assertEqual(self.request('/api/health',cookie=self.login())[0],200)
    def test_private_and_admin_routes_blocked(self):
        cookie=self.login()
        for path in ['/.env','/.local/demo/share.txt','/demo_security.py','/studio.html','/assets/../server.py']:self.assertEqual(self.request(path,cookie=cookie)[0],404,path)
        self.assertEqual(self.request('/api/chat',{'prompt':'arbitrary generation'},cookie)[0],404)
    def test_coach_context_and_session_budget(self):
        cookie=self.login();body={'pack':'toeic3','questionId':'t3-1','learnerQuestion':'Why ten fifty?','reason':'I heard eleven.'}
        with patch('server.call_openai',return_value={'text':'Test explanation'}) as provider:
            for _ in range(2):self.assertEqual(self.request('/api/coach',body,cookie)[0],200)
            self.assertEqual(self.request('/api/coach',body,cookie)[0],429);self.assertEqual(provider.call_count,2)
            self.assertIn('ten minutes early',provider.call_args[0][0])
            self.assertEqual(self.request('/api/coach',{**body,'questionId':'unknown'},cookie)[0],400)
    def test_expiry_and_origin_fail_closed(self):
        cookie=self.login();self.sec.sessions[cookie.split('=')[1]]=0
        self.assertEqual(self.request('/api/health',cookie=cookie)[0],401)
        self.origin.write_text('https://example.com/path');self.assertIsNone(self.sec.origin())
    def test_named_domain_login_and_exact_host_origin(self):
        self.origin.write_text('https://ael.52sierra.net')
        named={'host':'ael.52sierra.net','origin':'https://ael.52sierra.net'}
        status,_,headers=self.request('/api/session',{'code':'test-classroom-code'},**named)
        self.assertEqual(status,200)
        self.assertIn('Secure',headers['Set-Cookie'])
        cookie=headers['Set-Cookie'].split(';')[0]
        self.assertEqual(self.request('/api/health',cookie=cookie,**named)[0],200)
        self.assertEqual(self.request('/api/session',{'code':'test-classroom-code'})[0],403)
        for changed in [{'host':'ael.52sierra.net.attacker.example'}, {'origin':'https://attacker.example'}]:
            self.assertEqual(self.request('/api/session',{'code':'test-classroom-code'},**{**named,**changed})[0],403)
        self.assertEqual(self.request('/.env',cookie=cookie,**named)[0],404)
    def test_public_origin_rejects_non_origins(self):
        for value in ['http://ael.52sierra.net','https://ael.52sierra.net/','https://user@ael.52sierra.net',
                      'https://*.52sierra.net','https://ael.52sierra.net:443','https://ael.52sierra.net?x=1',
                      'https://ael.52sierra.net#x','https://localhost','https://127.0.0.1','https://-bad.example','']:
            self.assertFalse(valid_public_origin(value),value)
        self.assertTrue(valid_public_origin('https://ael.52sierra.net'))
        self.assertTrue(valid_public_origin('https://class-test.trycloudflare.com'))
    def test_short_code_and_login_limit(self):
        with self.assertRaises(ValueError):DemoSecurity('short')
        for _ in range(60):self.sec.login('incorrect')
        self.assertEqual(self.sec.login('test-classroom-code')[0],429)
if __name__=='__main__':unittest.main()
