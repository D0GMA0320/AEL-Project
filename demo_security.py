"""Access and request limits for a temporary classroom tunnel, not a production account system."""
from collections import defaultdict
from http.cookies import SimpleCookie
from pathlib import Path
import hmac
import re
import secrets
import threading
import time

def valid_public_origin(value):
    """Accept one explicit HTTPS DNS origin, never a wildcard, path or credentials."""
    label = r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?'
    return isinstance(value, str) and len(value) <= 261 and re.fullmatch(
        rf'https://(?:{label}\.)+[a-z]{{2,63}}', value
    ) is not None

class DemoSecurity:
    def __init__(self, code, origin_file=None, max_calls=100):
        if len(code) < 10:
            raise ValueError('Use a classroom access code of at least 10 characters.')
        self.code = code
        self.origin_file = Path(origin_file) if origin_file else None
        self.sessions = {}
        self.login_attempts = []
        self.requests = defaultdict(list)
        self.calls = 0
        self.max_calls = max_calls
        self.lock = threading.Lock()

    def origin(self):
        if not self.origin_file or not self.origin_file.exists():
            return None
        value = self.origin_file.read_text(encoding='utf-8').strip()
        return value if valid_public_origin(value) else None

    def session(self, cookie):
        try:
            jar = SimpleCookie(cookie or '')
            token = jar['ael_session'].value if 'ael_session' in jar else ''
        except Exception:
            return None
        with self.lock:
            if self.sessions.get(token, 0) > time.monotonic():
                return token
        return None

    def login(self, code):
        with self.lock:
            current = time.monotonic()
            self.login_attempts = [t for t in self.login_attempts if current-t < 60]
            if len(self.login_attempts) >= 60:
                return 429, None
            self.login_attempts.append(current)
            if not isinstance(code, str) or not hmac.compare_digest(code.encode(), self.code.encode()):
                return 401, None
            expired = [token for token, until in self.sessions.items() if until <= current]
            for token in expired:
                self.sessions.pop(token, None)
                self.requests.pop(token, None)
            if len(self.sessions) >= 200:
                return 429, None
            token = secrets.token_urlsafe(32)
            self.sessions[token] = current + 8 * 3600
            return 200, token

    def reserve_call(self, token):
        with self.lock:
            current = time.monotonic()
            recent = [t for t in self.requests[token] if current-t < 60]
            if self.calls >= self.max_calls or len(recent) >= 3:
                return False
            self.requests[token] = recent + [current]
            self.calls += 1
            return True
