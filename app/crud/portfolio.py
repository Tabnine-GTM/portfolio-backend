from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio


def get_portfolio(db: Session, user_id: int):
    stmt = select(Portfolio).where(Portfolio.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def create_portfolio(db: Session, user_id: int):
    db_portfolio = Portfolio(user_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio
