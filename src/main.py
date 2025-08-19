
from wsgiref.simple_server import make_server
from controllers.index import index
from controllers.match.new_match import new_match
from controllers.match.match import match
from whitenoise import WhiteNoise


def application(environ, start_response):
    if environ['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [index().encode('utf-8')]

    elif environ['PATH_INFO'] == '/new-match':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [new_match().encode('utf-8')]
    
    elif environ['PATH_INFO'] == '/start-match':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [match(environ)]

    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'404 Not Found']

app = WhiteNoise(application)
app.add_files('static', prefix='static/')  # указываем папку со статикой

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print("Serving on http://localhost:8000...")
        httpd.serve_forever()