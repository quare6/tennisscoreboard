from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings


engine = create_engine(
    url=settings.DATABASE_url,
    echo=True,
)


session_factory = sessionmaker(bind=engine)