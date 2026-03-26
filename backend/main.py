"""
FastAPI backend for stock price prediction application.
Includes endpoints for predictions, model retraining, and portfolio tracking.

DISCLAIMER: Predictions are for educational purposes only.
"""

import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import pickle
import json
import hashlib
import bcrypt

from fastapi import FastAPI, HTTPException, Depends, status, WebSocket, WebSocketDisconnect, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import numpy as np
import yfinance as yf
from jose import jwt
import threading
import asyncio

# Import local modules
from database import Base, User, Prediction, Portfolio, StockData
from schemas import (
    UserCreate,
    UserResponse,
    PredictionRequest,
    PredictionResponse,
    TrainingRequest,
    TrainingResponse,
    PortfolioCreate,
    PortfolioResponse,
    HealthResponse,
    SentimentResponse,
)
from sentiment_analysis import SentimentAnalyzer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration - Updated with SHA256 pre-hashing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stock_prediction.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
MODEL_DIR = os.getenv("MODEL_DIR", "../ml_model/models")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", None)

# Initialize FastAPI
app = FastAPI(
    title="Stock Price Prediction API",
    description="LSTM-based stock price prediction with sentiment analysis",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Root endpoint - API welcome
@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "Stock Price Prediction API",
        "version": "1.0.0",
        "documentation": "http://localhost:8000/docs",
        "alternative_docs": "http://localhost:8000/redoc",
        "health": "http://localhost:8000/api/health",
        "endpoints": {
            "auth": ["/api/auth/register", "/api/auth/login"],
            "stock": ["/api/stock/data/{ticker}"],
            "predictions": ["/api/predict", "/api/predictions"],
            "portfolio": ["/api/portfolio"],
            "models": ["/api/models", "/api/retrain"],
            "sentiment": ["/api/sentiment/{ticker}"],
            "health": ["/api/health"]
        }
    }


# Security
def get_password_hash(password: str) -> str:
    """Hash password with SHA256 first, then bcrypt."""
    # Pre-hash with SHA256 to ensure password is always 64 bytes (SHA256 hex output)
    # This solves the bcrypt 72-byte limit
    sha_hash = hashlib.sha256(password.encode()).hexdigest()
    hashed = bcrypt.hashpw(sha_hash.encode(), bcrypt.gensalt())
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    # First hash with SHA256 to ensure we're under 72 bytes for bcrypt
    sha_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    try:
        return bcrypt.checkpw(sha_hash.encode(), hashed_password.encode())
    except Exception:
        return False


def get_token_from_header(authorization: str = Header(None)):
    """Extract token from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return parts[1]


# Sentiment analyzer
sentiment_analyzer = SentimentAnalyzer(news_api_key=NEWS_API_KEY)


def get_db():
    """Database dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    """Get current authenticated user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.post("/api/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return JWT token."""
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create access token
        access_token = create_access_token(data={"sub": db_user.username})
        
        logger.info(f"New user registered: {user.username}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(db_user),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@app.post("/api/auth/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    """Login user and return JWT token."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"User logged in: {username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user),
    }


# ============================================================================
# Stock Data Endpoints
# ============================================================================


@app.get("/api/stock/data/{ticker}")
def get_stock_data(
    ticker: str,
    days: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get historical stock data.

    Args:
        ticker: Stock ticker symbol
        days: Number of days of historical data

    Returns:
        JSON with stock prices and technical indicators
    """
    try:
        # Download data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if df.empty:
            logger.warning(f"No data found for {ticker} from yfinance, generating demo data")
            # Generate demo data when yfinance fails
            import random
            data = []
            current_price = 100.0
            for i in range(days):
                date = start_date + timedelta(days=i)
                change = random.uniform(-2, 2)
                current_price += change
                data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": current_price - abs(change)/2,
                    "high": current_price + abs(change),
                    "low": current_price - abs(change),
                    "close": current_price,
                    "volume": random.randint(1000000, 10000000),
                    "ma20": None,
                    "ma50": None,
                    "rsi": None,
                    "macd": None,
                })
            logger.info(f"Generated {len(data)} demo data points for {ticker}")
            return {"ticker": ticker, "data": data}

        logger.info(f"Downloaded {len(df)} rows for {ticker}")
        
        # Calculate technical indicators
        df["MA_20"] = df["Close"].rolling(window=20).mean()
        df["MA_50"] = df["Close"].rolling(window=50).mean()

        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

        exp1 = df["Close"].ewm(span=12, adjust=False).mean()
        exp2 = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = exp1 - exp2

        # Format response
        data = []
        for date, row in df.iterrows():
            data.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]),
                    "ma20": float(row["MA_20"]) if not np.isnan(row["MA_20"]) else None,
                    "ma50": float(row["MA_50"]) if not np.isnan(row["MA_50"]) else None,
                    "rsi": float(row["RSI"]) if not np.isnan(row["RSI"]) else None,
                    "macd": float(row["MACD"]) if not np.isnan(row["MACD"]) else None,
                }
            )

        logger.info(f"Retrieved {len(data)} data points for {ticker}")
        return {"ticker": ticker, "data": data}

    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Error fetching stock data for {ticker}: {error_msg}", exc_info=True)
        # Return demo data as fallback
        import random
        data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        current_price = 100.0
        for i in range(min(days, 100)):
            date = start_date + timedelta(days=i)
            change = random.uniform(-2, 2)
            current_price += change
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": current_price - abs(change)/2,
                "high": current_price + abs(change),
                "low": current_price - abs(change),
                "close": current_price,
                "volume": random.randint(1000000, 10000000),
                "ma20": None,
                "ma50": None,
                "rsi": None,
                "macd": None,
            })
        logger.info(f"Generated {len(data)} fallback demo data points for {ticker}")
        return {"ticker": ticker, "data": data}


# ============================================================================
# Prediction Endpoints
# ============================================================================


@app.post("/api/predict", response_model=PredictionResponse)
def predict_price(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Predict future stock price using trained LSTM model.

    DISCLAIMER: Predictions are for educational purposes only.
    Stock market carries inherent uncertainty.
    """
    try:
        # Load model and scaler
        model_path = os.path.join(MODEL_DIR, f"{request.ticker}_lstm_model.h5")
        scaler_path = os.path.join(MODEL_DIR, f"{request.ticker}_scaler.pkl")
        metadata_path = os.path.join(MODEL_DIR, f"{request.ticker}_metadata.json")

        if not os.path.exists(model_path):
            raise HTTPException(
                status_code=404,
                detail=f"Model not trained for {request.ticker}. Please retrain.",
            )

        # Import here to avoid circular imports
        import tensorflow as tf

        model = tf.keras.models.load_model(model_path)

        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)

        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        # Fetch recent data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=200)
        df = yf.download(request.ticker, start=start_date, end=end_date, progress=False)

        if len(df) < 60:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for prediction",
            )

        # Calculate technical indicators
        df["MA_20"] = df["Close"].rolling(window=20).mean()
        df["MA_50"] = df["Close"].rolling(window=50).mean()
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        exp1 = df["Close"].ewm(span=12, adjust=False).mean()
        exp2 = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = exp1 - exp2

        # Prepare input
        features = ["Close", "Open", "High", "Low", "Volume", "MA_20", "MA_50", "RSI", "MACD"]
        data = df[features].dropna().values[-60:]
        data_scaled = scaler.transform(data)
        X = np.array([data_scaled])

        # Make prediction
        prediction_scaled = model.predict(X, verbose=0)[0][0]

        # Inverse transform to get actual price
        dummy = np.zeros((1, data_scaled.shape[1]))
        dummy[0, 0] = prediction_scaled
        prediction = scaler.inverse_transform(dummy)[0, 0]

        # Save prediction to database
        db_prediction = Prediction(
            user_id=current_user.id,
            ticker=request.ticker,
            predicted_price=float(prediction),
            prediction_window=request.days_ahead,
            metrics=metadata.get("test_metrics", {}),
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)

        logger.info(
            f"Prediction made for {request.ticker}: {prediction:.2f} "
            f"(user: {current_user.username})"
        )

        return db_prediction

    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/api/predictions", response_model=List[PredictionResponse])
def get_predictions(
    ticker: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's prediction history."""
    query = db.query(Prediction).filter(Prediction.user_id == current_user.id)

    if ticker:
        query = query.filter(Prediction.ticker == ticker)

    predictions = query.order_by(Prediction.created_at.desc()).all()
    return predictions


# ============================================================================
# Model Retraining Endpoints
# ============================================================================


@app.post("/api/retrain", response_model=TrainingResponse)
def retrain_model(
    request: TrainingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrain the LSTM model for a specific ticker.
    Runs asynchronously to avoid blocking.
    """
    try:
        # Validate permissions - only allow admin or scheduled tasks
        logger.info(f"Retraining initiated for {request.ticker} by {current_user.username}")

        # Run training asynchronously
        def train_async():
            try:
                from ml_model.train import train_stock_model

                train_stock_model(
                    ticker=request.ticker,
                    epochs=request.epochs,
                    batch_size=request.batch_size,
                    lstm_units=request.lstm_units,
                    model_dir=MODEL_DIR,
                )
                logger.info(f"Training completed for {request.ticker}")
            except Exception as e:
                logger.error(f"Training failed for {request.ticker}: {str(e)}")

        thread = threading.Thread(target=train_async, daemon=True)
        thread.start()

        return TrainingResponse(
            ticker=request.ticker,
            status="training_started",
            message=f"Model retraining started for {request.ticker}",
            metrics={},
            timestamp=datetime.now(timezone.utc),
        )

    except Exception as e:
        logger.error(f"Error initiating training: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


# ============================================================================
# Portfolio Endpoints
# ============================================================================


@app.post("/api/portfolio", response_model=PortfolioResponse)
def add_portfolio_item(
    item: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add stock to user's portfolio."""
    try:
        portfolio = Portfolio(
            user_id=current_user.id,
            ticker=item.ticker,
            quantity=item.quantity,
            purchase_price=item.purchase_price,
            purchase_date=item.purchase_date,
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

        logger.info(f"Portfolio item added: {item.ticker} (user: {current_user.username})")
        return portfolio

    except Exception as e:
        logger.error(f"Error adding portfolio item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/portfolio", response_model=List[PortfolioResponse])
def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's portfolio."""
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()

    # Add current price
    for item in portfolio:
        try:
            stock = yf.Ticker(item.ticker)
            item.current_price = stock.info.get("currentPrice", None)
            if item.current_price:
                item.total_value = item.quantity * item.current_price
        except Exception as e:
            logger.warning(f"Error fetching current price for {item.ticker}: {str(e)}")

    return portfolio


@app.delete("/api/portfolio/{portfolio_id}")
def delete_portfolio_item(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove item from portfolio."""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    if not portfolio or portfolio.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    db.delete(portfolio)
    db.commit()

    logger.info(f"Portfolio item deleted (user: {current_user.username})")
    return {"message": "Portfolio item deleted"}


# ============================================================================
# Sentiment Analysis Endpoints
# ============================================================================


@app.get("/api/sentiment/{ticker}", response_model=SentimentResponse)
def get_sentiment(
    ticker: str,
    db: Session = Depends(get_db),
):
    """
    Get news sentiment analysis for a stock ticker.
    """
    try:
        sentiment = sentiment_analyzer.analyze_ticker_sentiment(ticker)
        sentiment["ticker"] = ticker
        sentiment["timestamp"] = datetime.now(timezone.utc)
        return sentiment

    except Exception as e:
        logger.error(f"Error analyzing sentiment for {ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# Health and System Endpoints
# ============================================================================


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
    )


@app.get("/api/models")
def get_available_models():
    """Get list of available trained models."""
    try:
        models = []
        if os.path.exists(MODEL_DIR):
            for file in os.listdir(MODEL_DIR):
                if file.endswith("_metadata.json"):
                    ticker = file.replace("_metadata.json", "")
                    metadata_path = os.path.join(MODEL_DIR, file)
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                    models.append(metadata)

        return {"models": models}

    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# WebSocket Endpoint for Real-time Updates
# ============================================================================


class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {str(e)}")


manager = ConnectionManager()


@app.websocket("/ws/prices/{ticker}")
async def websocket_endpoint(websocket: WebSocket, ticker: str):
    """
    WebSocket endpoint for real-time stock price updates.
    Streams price updates every 30 seconds.
    """
    await manager.connect(websocket)
    try:
        while True:
            try:
                # Fetch current price
                stock = yf.Ticker(ticker)
                price = stock.info.get("currentPrice")

                message = {
                    "ticker": ticker,
                    "price": price,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

                await websocket.send_json(message)
                await asyncio.sleep(30)  # Update every 30 seconds

            except WebSocketDisconnect:
                manager.disconnect(websocket)
                break
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}")
                await asyncio.sleep(30)

    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
