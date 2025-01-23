from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    portfolio = relationship("Portfolio", back_populates="user", uselist=False)