from pydantic import BaseModel
from typing import List

from app.schemas.stock import Stock

class PortfolioBase(BaseModel):
    pass

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    user_id: int
    stocks: List[Stock] = []
    total_value: float = 0.0

    class Config:
        from_attributes = True