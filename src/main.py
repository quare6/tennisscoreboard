import sys
from pathlib import Path

from wsgiref.simple_server import make_server

from src.controllers.index import index
from src.controllers.match.new_match import new_match
from src.controllers.match.start_match import match
from src.controllers.match.add_point import add_point
from src.controllers.match.matches import match_search
from src.models.base import Base
from src.database import engine

from whitenoise import WhiteNoise

sys.path.append(str(Path(__file__).parent.parent))

def init_database():
    Base.metadata.create_all(bind=engine)

try:
    print("Initializing database...")
    init_database()
    print("Database initialized successfully!")
except Exception as e:
    print(f"Error initializing database: {e}")
    sys.exit(1)

def application(environ, start_response):
    path = environ['PATH_INFO']

    if path == '/':
        return index(environ, start_response)
    elif path == '/new-match':
        return new_match(environ, start_response)
    elif path == '/start-match':
        return match(environ, start_response)
    elif path == '/add-point':
        return add_point(environ, start_response)
    elif path == '/matches':
        return match_search(environ, start_response)

    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'404 Not Found']

app = WhiteNoise(application)
app.add_files('static', prefix='static/')  # указываем папку со статикой

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print("Serving on http://localhost:8000...")
        httpd.serve_forever()