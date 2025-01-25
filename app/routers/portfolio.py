from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.portfolio import Portfolio as PortfolioModel
from app.schemas.portfolio import Portfolio
from app.utils.stock_api import fetch_multiple_stock_data
from app.dependencies import get_or_create_user_portfolio

from .stock import router as stock_router

router = APIRouter()

router.include_router(stock_router, prefix="/portfolio", tags=["stock"])

@router.get("/portfolio", response_model=Portfolio)
def get_user_portfolio(
    portfolio: PortfolioModel = Depends(get_or_create_user_portfolio),
    db: Session = Depends(get_db)
):
    # Calculate the total value of the portfolio
    total_value = sum(stock.current_price * stock.number_of_shares for stock in portfolio.stocks)

    # Create a Portfolio object with the calculated total value
    return Portfolio(
        id=portfolio.id,
        user_id=portfolio.user_id,
        stocks=portfolio.stocks,
        total_value=total_value
    )

@router.post("/portfolio/refresh", response_model=Portfolio)
def refresh_portfolio(
    portfolio: PortfolioModel = Depends(get_or_create_user_portfolio),
    db: Session = Depends(get_db)
):
    # Get all stocks in the portfolio
    stocks = portfolio.stocks

    if not stocks:
        return Portfolio(
            id=portfolio.id,
            user_id=portfolio.user_id,
            stocks=[],
            total_value=0
        )

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
            stock.current_price = current_price
            db.add(stock)

    db.commit()
    db.refresh(portfolio)

    # Calculate the total value of the portfolio
    total_value = sum(stock.current_price * stock.number_of_shares for stock in portfolio.stocks)

    return Portfolio(
        id=portfolio.id,
        user_id=portfolio.user_id,
        stocks=portfolio.stocks,
        total_value=total_value
    )