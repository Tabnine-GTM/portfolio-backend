from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    ticker_symbol = Column(String, index=True)
    name = Column(String)
    issue_date = Column(Date)
    number_of_shares = Column(Float)
    purchase_price = Column(Float)

    portfolio = relationship("Portfolio", back_populates="stocks")