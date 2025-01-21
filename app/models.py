from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    portfolio = relationship("Portfolio", back_populates="user", uselist=False)

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="portfolio")
    stocks = relationship("Stock", back_populates="portfolio")

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