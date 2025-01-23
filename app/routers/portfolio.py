from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from ..utils import auth
from ..utils.stock_api import fetch_multiple_stock_data

router = APIRouter()

@router.get("/portfolio", response_model=schemas.Portfolio)
def get_user_portfolio(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    portfolio = crud.get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.post("/portfolio/stock", response_model=schemas.Stock)
def add_stock(stock: schemas.StockCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    portfolio = crud.get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        portfolio = crud.create_portfolio(db, user_id=current_user.id)
    try:
        return crud.add_stock(db=db, stock=stock, portfolio_id=portfolio.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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

@router.post("/portfolio/refresh", response_model=schemas.Portfolio)
def refresh_portfolio(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    portfolio = crud.get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Get all stocks in the portfolio
    stocks = crud.get_stocks_in_portfolio(db, portfolio_id=portfolio.id)

    if not stocks:
        return portfolio  # Return early if there are no stocks to update

    # Fetch current prices for all stocks in one API call
    symbols = [stock.ticker_symbol for stock in stocks]
    try:
        stock_data = fetch_multiple_stock_data(symbols)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update each stock's current price
    for stock in stocks:
        if stock.ticker_symbol in stock_data:
            current_price = float(stock_data[stock.ticker_symbol]['price'])
            crud.update_stock_price(db, stock_id=stock.id, current_price=current_price)

    # Refresh the portfolio to get updated data
    db.refresh(portfolio)
    return portfolio