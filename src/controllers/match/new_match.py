from src.views.render import render_template

def new_match(environ, start_response):
    html = render_template("new-match.html")
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html.encode('utf-8')]

