from src.services.player import Player
from src.services.player_service import PlayerSerivice
from src.services.game_save import GameSave


class Match:
    def __init__(self, player1_name: str, player2_name: str):
        self.player1 = PlayerSerivice.get_or_create(player1_name)
        self.player2 = PlayerSerivice.get_or_create(player2_name)

        self.score = {'set1': [0, 0]}
        self.current_set = 1
        self.is_match_finished = False
    
    def add_point(self, winner_name: str) -> None:
        if winner_name == self.player1.name:
            winner = self.player1
            loser = self.player2
        else:
            winner = self.player2
            loser = self.player1
            
        if winner.points == 40 and loser.points == 40:
            if loser.has_advantage:
                loser.has_advantage = False
            elif winner.has_advantage:
                self.add_game(winner, loser)
            else:
                winner.has_advantage = True
        
        if winner.has_advantage:
            self.add_game(winner, loser)

        if winner.points == 0:
            winner.points = 15
        elif winner.points == 15:
            winner.points = 30
        elif winner.points == 30:
            winner.points = 40
        elif winner.points == 40:
            self.add_game(winner, loser)

        return None
    
    def add_game(self, winner: Player, loser: Player) -> None:
        winner.games += 1

        winner.points = 0
        loser.points = 0
        winner.has_advantage = False
        loser.has_advantage = False

        self.score[f'set{self.current_set}'] = [winner.games, loser.games]

        if winner.games >= 6 and winner.games - loser.games == 2:
            winner.add_set(winner, loser)
    
    def add_set(self, winner: Player, loser: Player):
        winner.sets += 1

        self.score[f"set{self.current_set}"] = [winner.games, loser.games]
        self.current_set += 1

        winner.games = 0
        loser.games = 0

        if winner.sets == 2:
            self.finish_match(winner, loser)
    
    def finish_match(self, winner, loser):
        self.is_match_finished = True

        GameSave.save_game(winner, loser, self.score)

        PlayerSerivice.update_stats(winner.db_id, wins=1, games=1)
        PlayerSerivice.update_stats(loser.db_id, loses=1, games=1)
    
    def is_finished(self):
        return self.is_match_finished
    
    def get_score_display(self):
        return {
            'player1': {
                'name': self.player1.name,
                'points': self.player1.points,
                'games': self.player1.games,
                'sets': self.player1.sets,
                'advantage': self.player1.has_advantage
            },
            'player2': {
                'name': self.player2.name,
                'points': self.player2.points,
                'games': self.player2.games,
                'sets': self.player2.sets,
                'advantage': self.player2.has_advantage
            },
            'current_set': self.current_set,
            'score': self.score,
            'match_finished': self.is_finished()
        }