from player import Player
from player_service import PlayerSerivice
from game_save import GameSave


class Match:
    def __init__(self, player1_name: str, player2_name: str):
        self.player1 = PlayerSerivice.get_or_create(player1_name)
        self.player2 = PlayerSerivice.get_or_create(player2_name)
        self.score = {}
    
    def add_point(self, winner: Player, loser: Player) -> None:
        if winner.points == 40 and loser.points == 40:
            if loser.has_advantage:
                loser.has_advantage = False
            elif winner.has_advantage:
                winner.has_advantage = False
                self.add_game(winner)
            else:
                winner.has_advantage = True
        
        if winner.has_advantage:
            winner.has_advantage = False
            loser.has_advantage = False
            self.add_game(winner)

        if winner.points == 0:
            winner.points = 15
        elif winner.points == 15:
            winner.points = 30
        elif winner.points == 30:
            winner.points = 40
        elif winner.points == 40:
            self.add_game(winner)

        return None
    
    def add_game(self, winner: Player, loser: Player) -> None:
        winner.games += 1

        if winner.games >= 6 and winner.games - loser.games == 2:
            winner.add_set(winner, loser)
    
    def add_set(self, winner: Player, loser: Player):
        winner.sets += 1
        sets = sum(winner.sets + loser.sets)
        self.score[f"set{sets}"] = [winner.games, loser.games]
        winner.games = 0
        loser.games = 0

        if winner.sets == 2:
            GameSave.save_game(winner, loser, self.score)