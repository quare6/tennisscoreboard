from uuid import uuid4
from urllib.parse import parse_qs


class SessionMiddleware:
    def __init__(self, app):
        self.app = app
        self.sessions = {}
    
    def __call__(self, environ, start_response):
        session_id = self._get_session_id_from_cookies(environ)

        if not session_id:
            session_id = str(uuid4())
            # self.sessions[session_id] = {'new': True}
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        
        environ['SESSION_ID'] = session_id
        environ['SESSION'] = self.sessions[session_id]

        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly'))
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response)

    def _get_session_id_from_cookies(self, environ):
        cookies_header = environ.get('HTTP_COOKIE')
        if not cookies_header:
            return None
        
        cookies = parse_qs(cookies_header.replace('; ', '&'))
        session_cookies = cookies.get('session_id', [])
        if session_cookies:
            return session_cookies[0]
        return None