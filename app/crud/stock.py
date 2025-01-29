from datetime import datetime, timedelta, date
from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from typing import Optional

from app.models.stock import Stock, StockPriceHistory
from app.schemas.stock import StockCreate
from app.utils.stock_api import fetch_daily_stock_data, fetch_stock_overview


def add_stock(db: Session, stock: StockCreate, portfolio_id: int) -> Stock:
    symbol = stock.ticker_symbol

    try:
        # Fetch stock data
        daily_data = fetch_daily_stock_data(symbol)
        if not daily_data:
            raise HTTPException(
                status_code=404, detail=f"No data found for stock symbol: {symbol}"
            )

        latest_date = max(daily_data.keys())

        # Get the stock name and additional information
        overview_data = fetch_stock_overview(symbol)
        if not overview_data:
            raise HTTPException(
                status_code=404,
                detail=f"No overview data found for stock symbol: {symbol}",
            )

        # Create the stock
        stock_name = overview_data.get("Name", symbol)
        market_cap = float(overview_data.get("MarketCapitalization", 0))
        pe_ratio = (
            float(overview_data.get("PERatio", 0))
            if overview_data.get("PERatio") not in ["None", None]
            else None
        )
        week_52_high = float(overview_data.get("52WeekHigh", 0))
        week_52_low = float(overview_data.get("52WeekLow", 0))

        # Create the stock
        db_stock = Stock(
            ticker_symbol=symbol,
            name=stock_name,
            number_of_shares=stock.number_of_shares,
            issue_date=stock.issue_date,
            purchase_price=stock.purchase_price,
            current_price=float(daily_data[latest_date]["4. close"]),
            market_cap=market_cap,
            pe_ratio=pe_ratio,
            week_52_high=week_52_high,
            week_52_low=week_52_low,
            portfolio_id=portfolio_id,
        )
        db.add(db_stock)
        db.flush()

        # Add price history
        end_date = datetime.strptime(latest_date, "%Y-%m-%d").date()
        start_date = end_date - timedelta(days=60)

        for date_str, values in daily_data.items():
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date <= date <= end_date:
                add_stock_price_history(
                    db, stock_id=db_stock.id, date=date, price=float(values["4. close"])
                )

        db.commit()
        return db_stock

    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while adding the stock: {str(e)}",
        )


def update_stock(db: Session, stock_id: int, stock: StockCreate) -> Optional[Stock]:
    stmt = select(Stock).filter_by(id=stock_id)
    result = db.execute(stmt)
    db_stock = result.scalar_one_or_none()
    if db_stock:
        for key, value in stock.model_dump().items():
            setattr(db_stock, key, value)
        db.commit()
        db.refresh(db_stock)
    return db_stock


def delete_stock(db: Session, stock_id: int) -> Optional[Stock]:
    stmt = select(Stock).filter_by(id=stock_id)
    result = db.execute(stmt)
    db_stock = result.scalar_one_or_none()
    if db_stock:
        db.delete(db_stock)
        db.commit()
    return db_stock


def get_stocks_in_portfolio(db: Session, portfolio_id: int) -> list[Stock]:
    return (
        db.execute(select(Stock).filter_by(portfolio_id=portfolio_id)).scalars().all()
    )


def update_stock_price(
    db: Session, stock_id: int, current_price: float
) -> Optional[Stock]:
    stmt = select(Stock).filter_by(id=stock_id)
    result = db.execute(stmt)
    db_stock = result.scalar_one_or_none()
    if db_stock:
        db_stock.current_price = current_price
        db.commit()
        db.refresh(db_stock)
    return db_stock


def get_stock(db: Session, stock_id: int) -> Optional[Stock]:
    return db.execute(select(Stock).filter_by(id=stock_id)).scalar_one_or_none()


def clear_stock_price_history(db: Session, stock_id: int) -> None:
    stmt = delete(StockPriceHistory).where(StockPriceHistory.stock_id == stock_id)
    db.execute(stmt)
    db.commit()


def add_stock_price_history(
    db: Session, stock_id: int, date: date, price: float
) -> StockPriceHistory:
    price_history = StockPriceHistory(stock_id=stock_id, date=date, price=price)
    db.add(price_history)
    db.commit()
    return price_history


def get_stock_with_price_history(db: Session, stock_id: int) -> Optional[Stock]:
    stmt = select(Stock).options(joinedload(Stock.price_history)).filter_by(id=stock_id)
    return db.execute(stmt).scalar_one_or_none()
