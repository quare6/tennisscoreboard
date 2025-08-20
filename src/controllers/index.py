from src.views.render import render_template

def index(environ, start_response):
    html = render_template("index.html")
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html.encode('utf-8')]
