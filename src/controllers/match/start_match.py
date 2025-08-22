from urllib.parse import parse_qs

from src.views.render import render_template
from src.services.match import Match
from src.services.match_service import MatchService
from src.controllers.get_session import get_session_id


def match(environ, start_response):
    # session_id = get_session_id(environ)
    session_id = environ.get('SESSION_ID')

    if not session_id:
        start_response('302 Found', [
            ('Location', '/new-match'), 
            ('Set-Cookie', 'session_id=temp123')
            ])

    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0

    request_body = environ["wsgi.input"].read(request_body_size).decode("utf-8")

    post_data = parse_qs(request_body)

    player1 = post_data.get('playerOne', [''])[0].strip()
    player2 = post_data.get('playerTwo', [''])[0].strip()

    match = MatchService.create_match(player1_name=player1, player2_name=player2, session_id=session_id)
    context = match.get_score_display()

    html = render_template("match-score.html", context=context)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html.encode('utf-8')]