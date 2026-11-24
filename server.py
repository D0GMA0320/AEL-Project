"""AEL classroom server. Standard-library only; credentials never reach the browser."""
import argparse
import json
import os
from pathlib import Path
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
API_LOCK = threading.Lock()


def load_env(root=ROOT):
    path = root / '.env'
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if line.strip() and not line.lstrip().startswith('#') and '=' in line:
                name, value = line.split('=', 1)
                if name.strip() in {'SPEECH_KEY', 'SPEECH_REGION', 'OPENAI_API_KEY', 'OPENAI_MODEL'}:
                    os.environ.setdefault(name.strip(), value.strip().strip('"').strip("'"))


def utc():
    return datetime.now(timezone.utc).isoformat()


def record_evidence(record):
    directory = ROOT / '.local' / 'evidence'
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (str(uuid.uuid4()) + '.json')
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')


def call_openai(prompt, kind, request_id):
    api_key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPENAI_MODEL')
    if not api_key or not model:
        raise ValueError('OPENAI_API_KEY와 OPENAI_MODEL을 로컬 .env에 설정해 주세요.')
    request_body = {
        'model': model,
        'instructions': 'You are an English learning assistant. Follow the pedagogical task. Be explicit about uncertainty. Never claim audio assessment from text alone.',
        'input': prompt,
        'store': False,
        'max_output_tokens': 4500 if kind == 'lesson-generation' else 1600,
    }
    evidence = {'requestId': request_id, 'kind': kind, 'startedAt': utc(), 'request': request_body}
    start = time.monotonic()
    request = urllib.request.Request('https://api.openai.com/v1/responses',
        data=json.dumps(request_body).encode('utf-8'),
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=50) as response:
            raw_text = response.read(2_000_000).decode('utf-8')
        raw = json.loads(raw_text)
        text = '\n'.join(c['text'] for item in raw.get('output', []) if item.get('type') == 'message'
                         for c in item.get('content', []) if c.get('type') == 'output_text')
        evidence.update(rawResponse=raw, rawResponseText=raw_text, text=text,
                        latencyMs=round((time.monotonic() - start) * 1000), completedAt=utc())
        record_evidence(evidence)
        if raw.get('status') == 'incomplete' or not text:
            raise ValueError('응답이 불완전하거나 텍스트가 없습니다. 원본을 .local/evidence에 저장했습니다.')
        return evidence
    except urllib.error.HTTPError as error:
        # Do not reflect provider payloads or authorization headers to the browser.
        evidence.update(error='Provider HTTP ' + str(error.code), completedAt=utc())
        record_evidence(evidence)
        raise ValueError(f'OpenAI 요청 실패 (HTTP {error.code}). 키, 모델 접근 권한, 사용 한도를 확인하세요.') from None
    except (urllib.error.URLError, TimeoutError) as error:
        evidence.update(error=type(error).__name__, completedAt=utc())
        record_evidence(evidence)
        raise ValueError('OpenAI 연결 시간 초과 또는 네트워크 오류입니다. 준비된 해설을 사용하세요.') from None


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        # Request paths only; no request bodies, prompts, or credentials.
        print(fmt % args)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def valid_host(self):
        port = self.server.server_address[1]
        return self.headers.get('Host') in {f'127.0.0.1:{port}', f'localhost:{port}'}

    def json_reply(self, status, body):
        content = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def public_path(self):
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        if path in {'/', '/index.html'}:
            return True
        if not path.startswith('/assets/'):
            return False
        resolved = (ROOT / path.lstrip('/')).resolve()
        return resolved.is_relative_to((ROOT / 'assets').resolve()) and resolved.is_file() and resolved.suffix.lower() in {'.js', '.css', '.mp3', '.wav', '.ogg', '.svg', '.png', '.webp'}

    def do_GET(self):
        if not self.valid_host():
            self.json_reply(403, {'error': 'Invalid host'})
        elif self.path == '/api/health':
            self.json_reply(200, {'service': 'AEL', 'openaiConfigured': bool(os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_MODEL')), 'model': os.environ.get('OPENAI_MODEL')})
        elif self.public_path():
            super().do_GET()
        else:
            self.json_reply(404, {'error': 'Not found'})

    def do_HEAD(self):
        if self.valid_host() and self.public_path():
            super().do_HEAD()
        else:
            self.send_error(404)

    def do_POST(self):
        port = self.server.server_address[1]
        origins = {f'http://127.0.0.1:{port}', f'http://localhost:{port}'}
        if not self.valid_host() or self.headers.get('Origin') not in origins or self.headers.get('X-AEL-Request') != '1':
            self.json_reply(403, {'error': 'Only the local AEL page can request AI feedback.'})
            return
        if self.path != '/api/chat':
            self.json_reply(404, {'error': 'Not found'})
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 100_000:
                raise ValueError('Invalid request size')
            obj = json.loads(self.rfile.read(size))
            prompt = obj.get('prompt')
            if not isinstance(prompt, str) or not 1 <= len(prompt) <= 30000:
                raise ValueError('프롬프트 길이를 확인해 주세요.')
            kind = obj.get('kind')
            if kind not in {'coach', 'lesson-generation', 'speaking-text-feedback'}:
                raise ValueError('Invalid request kind')
        except (ValueError, AttributeError):
            self.json_reply(400, {'error': '요청 형식 또는 길이가 올바르지 않습니다.'})
            return
        if not API_LOCK.acquire(blocking=False):
            self.json_reply(429, {'error': '이전 요청이 진행 중입니다. 잠시 후 다시 시도하세요.'})
            return
        try:
            result = call_openai(prompt, kind, str(obj.get('requestId', uuid.uuid4()))[:100])
            self.json_reply(200, result)
        except ValueError as error:
            self.json_reply(502, {'error': str(error)})
        except Exception:
            self.json_reply(500, {'error': '서버 오류입니다. 기록 폴더 쓰기 권한과 설정을 확인하세요.'})
        finally:
            API_LOCK.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AEL local classroom server')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    load_env()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'AEL ready: http://127.0.0.1:{args.port}', flush=True)
    print('Live AI configured:', bool(os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_MODEL')), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
