from player import Player
from src.database import session_factory
from sqlalchemy import insert, select, or_
from models.match import MatchOrm
from models.player import PlayerOrm
from uuid import uuid4


class GameSave:
    @staticmethod
    def save_game(winner: Player, loser: Player, score: dict) -> None:
        with session_factory() as session:

            match_result = {"UUID": str(uuid4()),
                            "Player1": winner.db_id, 
                            "Player2": loser.db_id,
                            "Winner": winner.db_id,
                            "Score": score}

            insert_game = insert(MatchOrm).values(match_result)

            session.execute(insert_game)
            session.commit()