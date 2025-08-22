from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload

from src.models.match import MatchOrm
from src.models.player import PlayerOrm
from src.database import session_factory

class SearchMatch:

    @staticmethod
    def by_name(name: str) -> list:
        with session_factory() as session:

            player_stmt = select(PlayerOrm.ID).where(PlayerOrm.Name == name)
            player_id = session.execute(player_stmt).scalar()

            if not player_id:
                return []

            stmt = select(MatchOrm).options(
                joinedload(MatchOrm.player1_rel),
                joinedload(MatchOrm.player2_rel),
                joinedload(MatchOrm.winner_rel)
            ).where(
                or_(MatchOrm.Player1 == player_id, MatchOrm.Player2 == player_id))
            
            result = session.execute(stmt).unique().scalars().all()
            
            return result
    
    @staticmethod
    def all() -> list:
        with session_factory() as session:
            result = session.query(MatchOrm).options(
                joinedload(MatchOrm.player1_rel),
                joinedload(MatchOrm.player2_rel),
                joinedload(MatchOrm.winner_rel)
            ).all()
            result = session.query(MatchOrm).all()
            return result