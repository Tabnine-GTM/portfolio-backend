from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio

def get_portfolio(db: Session, user_id: int):
    return db.query(Portfolio).filter(Portfolio.user_id == user_id).first()

def create_portfolio(db: Session, user_id: int):
    db_portfolio = Portfolio(user_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio