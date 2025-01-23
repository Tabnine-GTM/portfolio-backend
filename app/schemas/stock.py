from pydantic import BaseModel
from typing import Optional
from datetime import date

class StockBase(BaseModel):
    ticker_symbol: str
    name: Optional[str] = None
    issue_date: Optional[date] = None
    number_of_shares: float
    purchase_price: float

class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id: int

    class Config:
        from_attributes = True