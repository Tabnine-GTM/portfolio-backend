from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.portfolio import Portfolio
from sqlalchemy import ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from app.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker_symbol: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String)
    issue_date: Mapped[date] = mapped_column(Date)
    number_of_shares: Mapped[float] = mapped_column(Float)
    purchase_price: Mapped[float] = mapped_column(Float)
    current_price: Mapped[float] = mapped_column(Float)
    market_cap: Mapped[float] = mapped_column(Float)
    pe_ratio: Mapped[float] = mapped_column(Float)
    week_52_high: Mapped[float] = mapped_column(Float)
    week_52_low: Mapped[float] = mapped_column(Float)
    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolios.id"))

    portfolio: Mapped[Portfolio] = relationship("Portfolio", back_populates="stocks")
    price_history: Mapped[list["StockPriceHistory"]] = relationship(
        "StockPriceHistory", back_populates="stock"
    )


class StockPriceHistory(Base):
    __tablename__ = "stock_price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"))
    date: Mapped[date] = mapped_column(Date)
    price: Mapped[float] = mapped_column(Float)

    stock: Mapped["Stock"] = relationship("Stock", back_populates="price_history")
