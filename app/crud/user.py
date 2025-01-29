from typing import Callable, Iterator, Optional

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.security import hash_password, manager


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


@manager.user_loader(conn_provider=get_db)
def get_user_by_username(
    username: str,
    db: Optional[Session] = None,
    conn_provider: Callable[[], Iterator[Session]] = None,
) -> Optional[User]:
    if db is None and conn_provider is None:
        raise ValueError("db and conn_provider cannot both be None.")

    if db is None:
        db = next(conn_provider())
    user = db.query(User).filter(User.username == username).first()
    return user


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
