from src.models.base import Base
# from src.models.match import MatchOrm
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index

class PlayerOrm(Base):
    __tablename__ = "players"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(unique=True)
    Games: Mapped[int]
    Wins: Mapped[int]
    Loses: Mapped[int] 

    __table_args__ = (
        Index("ix_players_name", "Name"),
    )

    matches_as_player1: Mapped[list["MatchOrm"]] = relationship(
        "MatchOrm", foreign_keys="MatchOrm.Player1", back_populates="player1_rel"
    )
    matches_as_player2: Mapped[list["MatchOrm"]] = relationship(
        "MatchOrm", foreign_keys="MatchOrm.Player2", back_populates="player2_rel"
    )
