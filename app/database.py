from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DBContext:
    def __init__(self):
        self.db = db_session()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


def get_db():
    """Returns the current db connection"""
    with DBContext() as db:
        yield db
