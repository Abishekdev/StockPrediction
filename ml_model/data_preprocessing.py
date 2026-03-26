"""
Data preprocessing module for stock price prediction.
Handles downloading data, normalization, and sequence generation.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class StockDataPreprocessor:
    """Preprocesses stock data for LSTM model training."""

    def __init__(self, lookback_window: int = 60):
        """
        Initialize the preprocessor.

        Args:
            lookback_window: Number of days to use for sequence generation (default: 60)
        """
        self.lookback_window = lookback_window
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.feature_scaler = MinMaxScaler(feature_range=(0, 1))

    def download_stock_data(
        self, ticker: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        Download stock data from Yahoo Finance.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'

        Returns:
            DataFrame with stock data
        """
        try:
            logger.info(f"Downloading data for {ticker} from {start_date} to {end_date}")
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            logger.info(f"Downloaded {len(df)} days of data for {ticker}")
            return df
        except Exception as e:
            logger.error(f"Error downloading data for {ticker}: {str(e)}")
            raise

    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators (RSI, MACD, Moving Averages).

        Args:
            df: DataFrame with OHLCV data

        Returns:
            DataFrame with technical indicators added
        """
        # Copy to avoid modifying original
        df = df.copy()

        # Moving Averages
        df["MA_20"] = df["Close"].rolling(window=20).mean()
        df["MA_50"] = df["Close"].rolling(window=50).mean()

        # RSI (Relative Strength Index)
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = df["Close"].ewm(span=12, adjust=False).mean()
        exp2 = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = exp1 - exp2
        df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()

        # Drop NaN values
        df = df.dropna()

        logger.info(f"Technical indicators calculated. Data shape: {df.shape}")
        return df

    def prepare_data(
        self, df: pd.DataFrame, test_split: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
        """
        Prepare data for LSTM training.

        Args:
            df: DataFrame with features and target
            test_split: Ratio for test split (default: 0.2 for 80/20 split)

        Returns:
            Tuple of (X_train, X_test, y_train, y_test, scaler)
        """
        try:
            # Select features
            features = ["Close", "Open", "High", "Low", "Volume", "MA_20", "MA_50", "RSI", "MACD"]
            data = df[features].values

            # Normalize data
            scaled_data = self.scaler.fit_transform(data)

            # Create sequences
            X, y = self._create_sequences(scaled_data)

            # Split into train and test
            split_idx = int(len(X) * (1 - test_split))
            X_train = X[:split_idx]
            X_test = X[split_idx:]
            y_train = y[:split_idx]
            y_test = y[split_idx:]

            logger.info(
                f"Data prepared - Train shape: {X_train.shape}, Test shape: {X_test.shape}"
            )
            return X_train, X_test, y_train, y_test, df[split_idx:].index

        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise

    def _create_sequences(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for LSTM training using sliding window.

        Args:
            data: Normalized data array

        Returns:
            Tuple of (X sequences, y targets)
        """
        X, y = [], []
        for i in range(len(data) - self.lookback_window):
            X.append(data[i : i + self.lookback_window])
            y.append(data[i + self.lookback_window, 0])  # Target is Close price

        return np.array(X), np.array(y)

    def inverse_transform(self, scaled_data: np.ndarray) -> np.ndarray:
        """
        Inverse transform scaled data back to original scale.

        Args:
            scaled_data: Scaled data array

        Returns:
            Original scale data
        """
        return self.scaler.inverse_transform(scaled_data)
