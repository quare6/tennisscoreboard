
def get_session_id(environ):
    cookies = environ.get('HTTP_COOKIE', '')

    for cookie in cookies.split():
        if 'session_id=' in cookie:
            return cookie.split('session_id=')[1].strip()

    return None