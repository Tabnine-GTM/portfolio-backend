from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

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

class PortfolioBase(BaseModel):
    pass

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    user_id: int
    stocks: List[Stock] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None