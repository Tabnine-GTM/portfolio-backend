from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.portfolio import get_portfolio, create_portfolio
from app.crud import stock as crudStock
from app.database import get_db
from app.models.user import User
from app.schemas.stock import StockCreate, Stock
from app.schemas.portfolio import Portfolio
from app.security import manager
from app.utils.stock_api import fetch_multiple_stock_data, fetch_daily_stock_data
from datetime import datetime, timedelta

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

@router.post("/portfolio/stock/{stock_id}/refresh-history", response_model=Stock)
def refresh_stock_history(
    stock_id: int,
    current_user: User = Depends(manager),
    db: Session = Depends(get_db)
):
    # Get the stock
    stock = crudStock.get_stock(db, stock_id=stock_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Ensure the stock belongs to the current user's portfolio
    portfolio = get_portfolio(db, user_id=current_user.id)
    if stock.portfolio_id != portfolio.id:
        raise HTTPException(status_code=403, detail="Not authorized to refresh this stock")

    try:
        # Fetch daily stock data
        daily_data = fetch_daily_stock_data(stock.ticker_symbol)

        # Get the latest 60 days of data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=60)

        # Clear existing price history
        crudStock.clear_stock_price_history(db, stock_id=stock.id)

        # Add new price history
        for date_str, values in daily_data.items():
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date <= date <= end_date:
                crudStock.add_stock_price_history(
                    db,
                    stock_id=stock.id,
                    date=date,
                    price=float(values["4. close"])
                )

        # Update the current price
        latest_date = max(daily_data.keys())
        current_price = float(daily_data[latest_date]["4. close"])
        stock = crudStock.update_stock_price(db, stock_id=stock.id, current_price=current_price)

        db.refresh(stock)
        return stock
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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