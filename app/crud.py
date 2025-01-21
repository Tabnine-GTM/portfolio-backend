from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_portfolio(db: Session, user_id: int):
    return db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id).first()

def create_portfolio(db: Session, user_id: int):
    db_portfolio = models.Portfolio(user_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def add_stock(db: Session, stock: schemas.StockCreate, portfolio_id: int):
    db_stock = models.Stock(**stock.dict(), portfolio_id=portfolio_id)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def update_stock(db: Session, stock_id: int, stock: schemas.StockCreate):
    db_stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if db_stock:
        for key, value in stock.dict().items():
            setattr(db_stock, key, value)
        db.commit()
        db.refresh(db_stock)
    return db_stock

def delete_stock(db: Session, stock_id: int):
    db_stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if db_stock:
        db.delete(db_stock)
        db.commit()
    return db_stock