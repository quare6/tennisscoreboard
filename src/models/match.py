from base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class MatchOrm(Base):
    __tablename__ = "matches"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    UUID: Mapped[str] = mapped_column(unique=True)
    Player1: Mapped[int] = mapped_column(ForeignKey("players.id"))
    Player2: Mapped[int] = mapped_column(ForeignKey("players.id"))
    Winner: Mapped[int]
    Score: Mapped[str] # JSON представление объекта с текущим счётом в матче хуй знает как это сделать
