from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class StockBase(BaseModel):
    ticker_symbol: str
    name: Optional[str] = None
    issue_date: Optional[date] = None
    number_of_shares: float
    purchase_price: float

class StockCreate(StockBase):
    pass

class StockPriceHistory(BaseModel):
    date: date
    price: float
class Stock(StockBase):
    id: int
    current_price: float
    price_history: List[StockPriceHistory]

    class Config:
        from_attributes = True