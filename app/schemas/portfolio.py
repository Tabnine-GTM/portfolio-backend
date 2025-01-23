from pydantic import BaseModel
from typing import List
from .stock import Stock

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