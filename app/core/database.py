from typing import Generator
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from app.core.settings import get_settings

Base = declarative_base()
settings = get_settings()

engine = create_engine(settings.DATABASE_URI,connect_args={"options": f"-c timezone=America/Santiago"})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()