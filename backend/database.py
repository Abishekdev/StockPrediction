"""
Database models for stock prediction application.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    predictions = relationship("Prediction", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")


class StockData(Base):
    """Cached stock data."""
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    date = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class Prediction(Base):
    """Store prediction history."""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    ticker = Column(String, index=True)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    predicted_price = Column(Float)
    actual_price = Column(Float, nullable=True)
    prediction_window = Column(Integer)  # days ahead
    metrics = Column(JSON)  # Store RMSE, MAE, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")


class Portfolio(Base):
    """User portfolio tracking."""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    ticker = Column(String, index=True)
    quantity = Column(Float)
    purchase_price = Column(Float)
    purchase_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="portfolios")
