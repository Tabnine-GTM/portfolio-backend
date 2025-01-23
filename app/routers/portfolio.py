from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..utils import auth
from ..database import get_db

router = APIRouter()

@router.get("/portfolio", response_model=schemas.Portfolio)
def read_portfolio(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    portfolio = crud.get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        portfolio = crud.create_portfolio(db, user_id=current_user.id)
    return portfolio

@router.post("/portfolio/stock", response_model=schemas.Stock)
def add_stock(stock: schemas.StockCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    portfolio = crud.get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        portfolio = crud.create_portfolio(db, user_id=current_user.id)
    return crud.add_stock(db=db, stock=stock, portfolio_id=portfolio.id)

@router.put("/portfolio/stock/{stock_id}", response_model=schemas.Stock)
def update_stock(stock_id: int, stock: schemas.StockCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_stock = crud.update_stock(db, stock_id=stock_id, stock=stock)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock

@router.delete("/portfolio/stock/{stock_id}", status_code=204)
def delete_stock(stock_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_stock = crud.delete_stock(db, stock_id=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"ok": True}