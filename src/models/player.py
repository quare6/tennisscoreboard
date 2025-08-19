from base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index

class PlayerOrm(Base):
    __tablename__ = "players"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(unique=True)
    Games: Mapped[int]
    Wins: Mapped[int]
    Loses: Mapped[int] 

    __table_args__ = (
        Index("ix_players_name", "Name")
    )