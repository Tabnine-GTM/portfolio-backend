from fastapi import Depends
from sqlalchemy.orm import Session
from app.crud.portfolio import get_portfolio, create_portfolio
from app.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.security import manager

async def get_or_create_user_portfolio(
    current_user: User = Depends(manager),
    db: Session = Depends(get_db)
) -> Portfolio:
    portfolio = get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        portfolio = create_portfolio(db, user_id=current_user.id)
    return portfolio