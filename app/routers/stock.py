from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import stock as crudStock
from app.database import get_db
from app.models.portfolio import Portfolio
from app.schemas.stock import StockCreate, Stock, StockWithPriceHistory
from app.utils.stock_api import fetch_daily_stock_data
from app.dependencies import get_or_create_user_portfolio
from datetime import datetime, timedelta

router = APIRouter()


def verify_stock_in_portfolio(stock_id: int, portfolio: Portfolio, db: Session):
    stock = crudStock.get_stock(db, stock_id=stock_id)
    if stock is None or stock.portfolio_id != portfolio.id:
        raise HTTPException(
            status_code=404, detail="Stock not found in user's portfolio"
        )
    return stock


@router.post("/stock", response_model=Stock)
def add_stock(
    stock: StockCreate,
    portfolio: Portfolio = Depends(get_or_create_user_portfolio),
    db: Session = Depends(get_db),
):
    try:
        return crudStock.add_stock(db=db, stock=stock, portfolio_id=portfolio.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/stock/{stock_id}", response_model=Stock)
def update_stock(
    stock_id: int,
    stock: StockCreate,
    portfolio: Portfolio = Depends(get_or_create_user_portfolio),
    db: Session = Depends(get_db),
):
    verify_stock_in_portfolio(stock_id, portfolio, db)
    return crudStock.update_stock(db, stock_id=stock_id, stock=stock)


@router.delete("/stock/{stock_id}", status_code=204)
def delete_stock(
    stock_id: int,
    portfolio: Portfolio = Depends(get_or_create_user_portfolio),
    db: Session = Depends(get_db),
):
    verify_stock_in_portfolio(stock_id, portfolio, db)
    crudStock.delete_stock(db, stock_id=stock_id)
    return {"ok": True}


@router.get("/stock/{stock_id}", response_model=StockWithPriceHistory)
def get_stock_with_history(
    stock_id: int,
    portfolio: Portfolio = Depends(get_or_create_user_portfolio),
    db: Session = Depends(get_db),
):
    stock_with_history = crudStock.get_stock_with_price_history(db, stock_id=stock_id)
    if stock_with_history is None or stock_with_history.portfolio_id != portfolio.id:
        raise HTTPException(
            status_code=404, detail="Stock not found in user's portfolio"
        )
    return StockWithPriceHistory.model_validate(stock_with_history)


@router.post("/stock/{stock_id}/refresh-history", response_model=Stock)
def refresh_stock_history(
    stock_id: int,
    portfolio: Portfolio = Depends(get_or_create_user_portfolio),
    db: Session = Depends(get_db),
):
    stock = verify_stock_in_portfolio(stock_id, portfolio, db)

    try:
        daily_data = fetch_daily_stock_data(stock.ticker_symbol)

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=60)

        crudStock.clear_stock_price_history(db, stock_id=stock.id)

        for date_str, values in daily_data.items():
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date <= date <= end_date:
                crudStock.add_stock_price_history(
                    db, stock_id=stock.id, date=date, price=float(values["4. close"])
                )

        latest_date = max(daily_data.keys())
        current_price = float(daily_data[latest_date]["4. close"])
        stock = crudStock.update_stock_price(
            db, stock_id=stock.id, current_price=current_price
        )

        db.refresh(stock)
        return stock
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
