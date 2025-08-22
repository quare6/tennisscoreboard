from src.views.render import render_template
from src.controllers.get_session import get_session_id
from src.services.match_service import MatchService

from urllib.parse import parse_qs

def add_point1(environ, start_response):
    # session_id = get_session_id(environ)
    session_id = environ['SESSION_ID']
    if not session_id:
        start_response('302 Found', [('Location', '/new-match')])
        return [b'']
    
    match = MatchService.get_match(session_id)

    if not match:
        start_response('302 Found', [('Location', '/new-match')])
        return [b'']
    
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            content_lenght = int(environ.get('CONTENT_LENGHT', 0))
        except ValueError:
            content_lenght = 0

        # query_string = environ.get('QUERY_STRING', '')[0]
        # query_params = parse_qs(query_string)
        # winner_name = query_params.get('winner', [''])[0]
        request_body = environ['wsgi.input'].read(content_lenght)
        request_body = request_body.decode('utf-8')
        post_data = parse_qs(request_body)
        winner_name = post_data.get('winner', [''])[0].strip()

        print(f"DEBUG: Adding point to: {winner_name}")  # ← Добавьте для дебага
        print(f"DEBUG: Match players: {match.player1.name} vs {match.player2.name}")

        if not winner_name:
            start_response('400 Bad Request', [('Content-Type', 'text/plain')])
            return [b'Winner name is required']

        match.add_points(winner_name)

        if match.is_finished():
            MatchService.end_match(session_id)
            # start_response('302 Found', [('Location', '/match-score')]) # вот тут подумать как сделать чтобы  редирект был на match-score с счетом уже и нельзя управлять тип
        
        score_data = match.get_score_display()
        html = render_template("match-score.html", score_data)

        start_response('200 OK', [('Content-Type', 'text/html')])

        return [html.encode('utf-8')]


def add_point(environ, start_response):
    session_id = environ.get('SESSION_ID')
    match = MatchService.get_match(session_id)
    
    if not match:
        start_response('302 Found', [('Location', '/new-match')])
        return [b'']
    
    if environ['REQUEST_METHOD'] == 'POST':
        # СОХРАНЯЕМ оригинальный wsgi.input до чтения
        original_wsgi_input = environ['wsgi.input']
        original_content_length = environ.get('CONTENT_LENGTH', '0')
        
        try:
            # Читаем тело POST запроса
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            request_body = environ["wsgi.input"].read(content_length)
            
            # Парсим данные
            post_data = parse_qs(request_body.decode("utf-8"))
            winner_name = post_data.get('winner', [''])[0].strip()
            
            print(f"DEBUG: Raw winner value: {post_data.get('winner')}")
            print(f"DEBUG: Adding point to: '{winner_name}'")
            print(f"DEBUG: All POST data: {post_data}")
            
            if not winner_name:
                start_response('400 Bad Request', [('Content-Type', 'text/plain')])
                return [b'Winner name is required']
            
            # Добавляем очко
            match.add_points(winner_name)
            
            # ВОССТАНАВЛИВАЕМ wsgi.input для WhiteNoise!
            # Создаем новый StringIO с теми же данными
            from io import BytesIO
            environ['wsgi.input'] = BytesIO(request_body)
            environ['CONTENT_LENGTH'] = str(len(request_body))
            
            # Получаем обновленный счет
            score_data = match.get_score_display()
            
            if match.is_finished():
                MatchService.end_match(session_id)
            
            # Возвращаем обновленную страницу
            html_content = render_template("match-score.html", score_data)
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [html_content.encode('utf-8')]
            
        except Exception as e:
            print(f"ERROR in add_point: {e}")
            import traceback
            traceback.print_exc()
            
            # Восстанавливаем оригинальные значения
            environ['wsgi.input'] = original_wsgi_input
            environ['CONTENT_LENGTH'] = original_content_length
            
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f"Server Error: {str(e)}".encode('utf-8')]