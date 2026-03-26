"""
Pydantic schemas for API request/response validation.
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """User creation schema."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class StockDataResponse(BaseModel):
    """Stock data response."""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class PredictionRequest(BaseModel):
    """Prediction request schema."""
    ticker: str = Field(..., min_length=1, max_length=10)
    days_ahead: int = Field(1, ge=1, le=30)


class PredictionResponse(BaseModel):
    """Prediction response schema."""
    id: int
    ticker: str
    predicted_price: float
    prediction_window: int
    metrics: Dict[str, float]
    created_at: datetime

    class Config:
        from_attributes = True


class TrainingRequest(BaseModel):
    """Model retraining request."""
    ticker: str = Field(..., min_length=1, max_length=10)
    epochs: int = Field(50, ge=10, le=200)
    batch_size: int = Field(32, ge=8, le=128)
    lstm_units: int = Field(128, ge=64, le=512)


class TrainingResponse(BaseModel):
    """Model training response."""
    ticker: str
    status: str
    message: str
    metrics: Dict[str, float]
    timestamp: datetime


class PortfolioCreate(BaseModel):
    """Portfolio item creation."""
    ticker: str
    quantity: float = Field(..., gt=0)
    purchase_price: float = Field(..., gt=0)
    purchase_date: datetime


class PortfolioResponse(BaseModel):
    """Portfolio response."""
    id: int
    ticker: str
    quantity: float
    purchase_price: float
    purchase_date: datetime
    current_price: Optional[float] = None
    total_value: Optional[float] = None

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    version: str


class SentimentResponse(BaseModel):
    """News sentiment analysis response."""
    ticker: str
    sentiment_score: float  # -1 to 1
    positive_count: int
    negative_count: int
    neutral_count: int
    articles_analyzed: int
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str
    error_code: str
    timestamp: datetime
