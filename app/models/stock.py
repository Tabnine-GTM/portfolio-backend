from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker_symbol = Column(String, index=True)
    name = Column(String)
    issue_date = Column(Date)
    number_of_shares = Column(Float)
    purchase_price = Column(Float)
    current_price = Column(Float)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))

    portfolio = relationship("Portfolio", back_populates="stocks")
    price_history = relationship("StockPriceHistory", back_populates="stock")

class StockPriceHistory(Base):
    __tablename__ = "stock_price_history"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(Date)
    price = Column(Float)

    stock = relationship("Stock", back_populates="price_history")