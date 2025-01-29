from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date


class StockBase(BaseModel):
    ticker_symbol: str
    name: Optional[str] = None
    issue_date: Optional[date] = None
    number_of_shares: float
    purchase_price: float

    model_config = ConfigDict(from_attributes=True)


class StockCreate(StockBase):
    pass


class StockPriceHistory(BaseModel):
    date: date
    price: float

    model_config = ConfigDict(from_attributes=True)


class Stock(StockBase):
    id: int
    current_price: float
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    portfolio_id: int


class StockWithPriceHistory(Stock):
    price_history: List[StockPriceHistory]
