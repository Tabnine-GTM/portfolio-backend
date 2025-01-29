from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DBContext:
    def __init__(self) -> None:
        self.db: Session = SessionLocal()

    def __enter__(self) -> Session:
        return self.db

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        self.db.close()


def get_db() -> Generator[Session, None, None]:
    """Returns the current db connection"""
    with DBContext() as db:
        yield db
