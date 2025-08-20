from src.models.base import Base
from src.models.player import PlayerOrm

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON


class MatchOrm(Base):
    __tablename__ = "matches"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UUID: Mapped[str] = mapped_column(unique=True)
    Player1: Mapped[int] = mapped_column(ForeignKey("players.id"))
    Player2: Mapped[int] = mapped_column(ForeignKey("players.id"))
    Winner: Mapped[int]
    Score: Mapped[dict] = mapped_column(JSON)

    player1_rel: Mapped["PlayerOrm"] = relationship(
        "PlayerOrm", foreign_keys=[Player1]  # Ссылается на поле Player1
    )
    player2_rel: Mapped["PlayerOrm"] = relationship(
        "PlayerOrm", foreign_keys=[Player2]  # Ссылается на поле Player2
    )
    winner_rel: Mapped["PlayerOrm"] = relationship(
        "PlayerOrm", foreign_keys=[Winner])
