"""
Main training script for stock price prediction model.
Downloads data, preprocesses, trains the LSTM model, and saves results.

DISCLAIMER: Predictions are for educational purposes only.
Stock market predictions carry inherent uncertainty and should not be used
as the sole basis for investment decisions.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import argparse

import numpy as np
import pandas as pd
from data_preprocessing import StockDataPreprocessor
from model import StockLSTMModel

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("training.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def train_stock_model(
    ticker: str = "AAPL",
    epochs: int = 50,
    batch_size: int = 32,
    lstm_units: int = 128,
    lookback_window: int = 60,
    model_dir: str = "models",
) -> Dict:
    """
    Train the LSTM model for stock price prediction.

    Args:
        ticker: Stock ticker symbol
        epochs: Number of training epochs
        batch_size: Batch size for training
        lstm_units: Number of LSTM units
        lookback_window: Number of days for sequence generation
        model_dir: Directory to save models

    Returns:
        Dictionary with training results and metrics
    """
    logger.info("=" * 80)
    logger.info(
        f"Starting training for {ticker} with hyperparameters: "
        f"epochs={epochs}, batch_size={batch_size}, lstm_units={lstm_units}"
    )
    logger.info("=" * 80)

    # Create model directory
    Path(model_dir).mkdir(exist_ok=True)

    try:
        # Step 1: Download and preprocess data
        logger.info("Step 1: Downloading stock data...")
        preprocessor = StockDataPreprocessor(lookback_window=lookback_window)

        # Calculate date range (last 5 years)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5 * 365)

        df = preprocessor.download_stock_data(
            ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
        )

        logger.info("Step 2: Calculating technical indicators...")
        df = preprocessor.calculate_technical_indicators(df)

        logger.info("Step 3: Preparing data sequences...")
        X_train, X_test, y_train, y_test, test_index = preprocessor.prepare_data(df)

        # Validate data
        split_idx = int(len(X_train) * 0.8)
        X_train_split = X_train[:split_idx]
        y_train_split = y_train[:split_idx]
        X_val = X_train[split_idx:]
        y_val = y_train[split_idx:]

        # Step 2: Build and train model
        logger.info("Step 4: Building LSTM model...")
        model = StockLSTMModel(lookback_window=lookback_window)
        model.build_model(input_features=9, lstm_units=lstm_units)

        logger.info("Step 5: Training model...")
        training_history = model.train(
            X_train_split,
            y_train_split,
            X_val,
            y_val,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
        )

        # Step 3: Evaluate model
        logger.info("Step 6: Evaluating model...")
        train_metrics = model.evaluate(X_train, y_train)
        test_metrics = model.evaluate(X_test, y_test)

        # Step 4: Make predictions
        logger.info("Step 7: Making predictions...")
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Step 5: Save model and metadata
        logger.info("Step 8: Saving model and metadata...")
        model_path = os.path.join(model_dir, f"{ticker}_lstm_model.h5")
        model.save_model(model_path)

        # Save metadata
        metadata = {
            "ticker": ticker,
            "trained_at": datetime.now().isoformat(),
            "lookback_window": lookback_window,
            "lstm_units": lstm_units,
            "batch_size": batch_size,
            "epochs": epochs,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "train_metrics": train_metrics,
            "test_metrics": test_metrics,
            "model_path": model_path,
            "disclaimer": "Predictions are for educational purposes only. "
            "Stock market carries inherent risk and uncertainty.",
        }

        metadata_path = os.path.join(model_dir, f"{ticker}_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

        # Save preprocessor scaler
        import pickle
        scaler_path = os.path.join(model_dir, f"{ticker}_scaler.pkl")
        with open(scaler_path, "wb") as f:
            pickle.dump(preprocessor.scaler, f)

        logger.info("=" * 80)
        logger.info("TRAINING RESULTS")
        logger.info("=" * 80)
        logger.info(f"Ticker: {ticker}")
        logger.info(f"Model saved to: {model_path}")
        logger.info(f"Metadata saved to: {metadata_path}")
        logger.info(f"\nTrain Metrics:")
        for metric, value in train_metrics.items():
            logger.info(f"  {metric}: {value:.6f}")
        logger.info(f"\nTest Metrics:")
        for metric, value in test_metrics.items():
            logger.info(f"  {metric}: {value:.6f}")
        logger.info("=" * 80)
        logger.info(
            "DISCLAIMER: Predictions are for educational purposes only. "
            "Do not use as sole basis for investment decisions."
        )
        logger.info("=" * 80)

        return metadata

    except Exception as e:
        logger.error(f"Error in training pipeline: {str(e)}", exc_info=True)
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Train LSTM model for stock price prediction"
    )
    parser.add_argument(
        "--ticker", type=str, default="AAPL", help="Stock ticker symbol (default: AAPL)"
    )
    parser.add_argument(
        "--epochs", type=int, default=50, help="Number of epochs (default: 50)"
    )
    parser.add_argument(
        "--batch_size", type=int, default=32, help="Batch size (default: 32)"
    )
    parser.add_argument(
        "--lstm_units",
        type=int,
        default=128,
        help="Number of LSTM units (default: 128)",
    )
    parser.add_argument(
        "--lookback",
        type=int,
        default=60,
        help="Lookback window (default: 60 days)",
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default="models",
        help="Directory to save models (default: models)",
    )

    args = parser.parse_args()

    train_stock_model(
        ticker=args.ticker,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lstm_units=args.lstm_units,
        lookback_window=args.lookback,
        model_dir=args.model_dir,
    )


if __name__ == "__main__":
    main()
