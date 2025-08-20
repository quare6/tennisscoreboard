from src.services.match import Match


class MatchService:
    current_matches = {}

    @staticmethod
    def create_match(player1_name: str, player2_name: str, session_id: str) -> Match:
        
        match = Match(player1_name, player2_name)
        MatchService.current_matches[session_id] = match
        return match
    
    @staticmethod
    def get_match(session_id: str) -> Match:
        return MatchService.current_matches[session_id]
    
    @staticmethod
    def end_match(session_id: str) -> Match | None:

        if session_id in MatchService.current_matches:
            match = MatchService.current_matches[session_id]

            del MatchService.current_matches[session_id]
            return match

        return None

