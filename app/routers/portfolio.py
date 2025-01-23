from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.portfolio import get_portfolio, create_portfolio
from app.crud import stock as crudStock
from app.database import get_db
from app.models.user import User
from app.schemas.stock import StockCreate, Stock
from app.schemas.portfolio import Portfolio
from app.security import manager
from app.utils.stock_api import fetch_multiple_stock_data

router = APIRouter()

@router.get("/portfolio", response_model=Portfolio)
def get_user_portfolio(current_user: User = Depends(manager), db: Session = Depends(get_db)):
    db_portfolio = get_portfolio(db, user_id=current_user.id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio

@router.post("/portfolio/stock", response_model=Stock)
def add_stock(stock: StockCreate, current_user: User = Depends(manager), db: Session = Depends(get_db)):
    portfolio = get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        portfolio = create_portfolio(db, user_id=current_user.id)
    try:
        return crudStock.add_stockdd_stock(db=db, stock=stock, portfolio_id=portfolio.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/portfolio/stock/{stock_id}", response_model=Stock)
def update_stock(stock_id: int, stock: StockCreate, current_user: User = Depends(manager), db: Session = Depends(get_db)):
    stock = crudStock.update_stock(db, stock_id=stock_id, stock=stock)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.delete("/portfolio/stock/{stock_id}", status_code=204)
def delete_stock(stock_id: int, current_user: User = Depends(manager), db: Session = Depends(get_db)):
    stock = crudStock.delete_stock(db, stock_id=stock_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"ok": True}

@router.post("/portfolio/refresh", response_model=Portfolio)
def refresh_portfolio(current_user: User = Depends(manager), db: Session = Depends(get_db)):
    portfolio = get_portfolio(db, user_id=current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Get all stocks in the portfolio
    stocks = portfolio.get_stocks_in_portfolio(db, portfolio_id=portfolio.id)

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
            stock.update_stock_price(db, stock_id=stock.id, current_price=current_price)

    # Refresh the portfolio to get updated data
    db.refresh(portfolio)
    return portfolio