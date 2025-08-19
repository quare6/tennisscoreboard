from sqlalchemy import select, or_

from models.match import MatchOrm
from models.player import PlayerOrm
from src.database import session_factory

class SearchMatch:

    @staticmethod
    def by_name(name: str) -> list:
        with session_factory() as session:

            player_stmt = select(PlayerOrm.ID).where(PlayerOrm.Name == name)
            player_id =  session.execute(player_stmt).scalar().first()

            if not player_id:
                raise # хз какую ошибку

            stmt = select(MatchOrm).where(or_(MatchOrm.Player1 == player_id, MatchOrm.Player2 == player_id))
            result = session.execute(stmt).scalars().all()
            return result
    
    @staticmethod
    def all() -> list:
        with session_factory() as session:
            stmt = select(MatchOrm)
            result = session.execute(stmt).scalars().all()
            return result