from pydantic import BaseModel, ConfigDict
from typing import List

from app.schemas.stock import Stock


class PortfolioBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PortfolioCreate(PortfolioBase):
    pass


class Portfolio(PortfolioBase):
    id: int
    user_id: int
    stocks: List[Stock] = []
    current_market_value: float = 0.0
    total_cost_basis: float = 0.0
