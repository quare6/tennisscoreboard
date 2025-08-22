from urllib.parse import parse_qs

from src.views.render import render_template
from src.services.search_match import SearchMatch

def match_search(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        query_string = environ.get('QUERY_STRING', '')
        query_params = parse_qs(query_string)

        # print(query_params.get('page', [1]))
        page = int(query_params.get('page', [1])[0])
        player_name = query_params.get('player_name', [''])[0].strip()
        matches_per_page = 3

        if player_name:
            matches = SearchMatch.by_name(player_name)
            
        else:
            matches = SearchMatch.all()
        
        total_matches = len(matches)
        total_pages = max(1, (total_matches + matches_per_page - 1) // matches_per_page)

        start_idx = (page - 1) * matches_per_page
        end_idx = start_idx + matches_per_page
        paginated_matches = matches[start_idx:end_idx]

        match_data = []
        for match in paginated_matches:
            match_data.append({
                'uuid': match.UUID,
                'player1_name': match.player1_rel.Name,
                'player2_name': match.player2_rel.Name,
                'winner_name': match.winner_rel.Name,
                'score': match.Score,
            })
        
        context = {
            'matches': match_data,
            'current_page': page,
            'total_pages': total_pages,
            'total_matches': total_matches,
            'player_name_filter': player_name,
            'has_previous': page > 1,
            'has_next': page < total_pages,
            'previous_page': page - 1,
            'next_page': page + 1
        }
        
        html_content = render_template("matches.html", context)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [html_content.encode('utf-8')]
