from src.views.render import render_template
from src.controllers.get_session import get_session_id
from src.services.match_service import MatchService

from urllib.parse import parse_qs

def add_point(environ, start_response):
    session_id = get_session_id(environ)
    if not session_id:
        start_response('302 Found', [('Location', '/new-match')])
        return [b'']
    
    match = MatchService.get_match(session_id)

    if not match:
        start_response('302 Found', [('Location', '/new-match')])
        return [b'']
    
    if environ['REQUEST_METHOD'] == 'POST':
        query_string = environ.get('QUERY_STRING', [''])[0]
        query_params = parse_qs(query_string)
        winner_name =  query_params.get('winner', [''])[0]

        match.add_point(winner_name)

        if match.is_finished():
            MatchService.end_match(session_id)
            # start_response('302 Found', [('Location', '/match-score')]) # вот тут подумать как сделать чтобы  редирект был на match-score с счетом уже и нельзя управлять тип
        
        score_data = match.get_score_display()
        html = render_template("match-score.html", score_data)

        start_response('200 OK', [('Content-Type', 'text/html')])

        return [html.encode('utf-8')]