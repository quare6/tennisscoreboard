
from src.database import session_factory
from sqlalchemy import insert
from src.services.player import Player
from src.models.player import PlayerOrm

class PlayerSerivice:

    @staticmethod
    def get_or_create(name: str) -> Player:
        with session_factory() as session:
            db_player = session.query(PlayerOrm).filter_by(Name=name).scalar() # scalar или first
            if not db_player:

                db_player = PlayerOrm(Name=name, Games=0, Wins=0, Loses=0)

                session.add(db_player)
                session.commit()
            
            return Player(db_player.Name, db_player.ID)
    
    @staticmethod
    def update_stats(player_id: int, wins: int = 0, loses: int = 0, games: int = 0):
        with session_factory() as session:
            player = session.get(PlayerOrm, player_id)
            if player:
                player.Wins += wins
                player.Loses += loses
                player.Games += games
                session.commit()