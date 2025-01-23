import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models, schemas
from ..config import settings

def add_stock(db: Session, stock: schemas.StockCreate, portfolio_id: int):
    # Fetch stock data from Alpha Vantage API
    api_key = settings.ALPHA_VANTAGE_API_KEY
    symbol = stock.ticker_symbol
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError("Unable to fetch stock data from Alpha Vantage API")

    daily_data = data["Time Series (Daily)"]
    latest_date = max(daily_data.keys())

    # Get the stock name
    overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    overview_response = requests.get(overview_url)
    overview_data = overview_response.json()
    stock_name = overview_data.get("Name", symbol)

    # Create the stock
    db_stock = models.Stock(
        ticker_symbol=symbol,
        name=stock_name,
        number_of_shares=stock.number_of_shares,
        purchase_price=stock.purchase_price,
        current_price=float(daily_data[latest_date]["4. close"]),
        portfolio_id=portfolio_id
    )
    db.add(db_stock)
    db.flush()  # This assigns an id to db_stock

    # Add price history
    end_date = datetime.strptime(latest_date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=60)

    for date_str, values in daily_data.items():
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if start_date <= date <= end_date:
            price_history = models.StockPriceHistory(
                stock_id=db_stock.id,
                date=date,
                price=float(values["4. close"])
            )
            db.add(price_history)
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