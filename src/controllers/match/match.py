'''
добавление очков без логики логика будет в services

сохранение матча без логики опять же

поиск по имени 

'''
from urllib.parse import parse_qs

from views.render import render_template


def match(environ, start_response):
    try:
        request_body_size = int(environ.get(["CONTENT_LENGTH"], 0))
    except ValueError:
        request_body_size = 0

    request_body = environ["wsgi.input"].read(request_body_size)
    request_body = request_body.decode("utf-8")

    post_data = parse_qs(request_body)

    player1 = post_data.get('player1', [''])[0]
    player2 = post_data.get('player2', [''])[0]

    context = {"player1": player1, "player2": player2}
    return render_template("match-score.html", context=context)