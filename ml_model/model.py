"""
LSTM-based deep learning model for stock price prediction.
Includes model architecture, training, and evaluation.
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.metrics import mean_squared_error, mean_absolute_error
import logging
from typing import Tuple, Dict
import json

logger = logging.getLogger(__name__)


class StockLSTMModel:
    """LSTM model for stock price prediction."""

    def __init__(self, lookback_window: int = 60):
        """
        Initialize the LSTM model.

        Args:
            lookback_window: Number of time steps in input sequences
        """
        self.lookback_window = lookback_window
        self.model = None
        self.history = None

    def build_model(
        self,
        input_features: int = 9,
        lstm_units: int = 128,
        dropout_rate: float = 0.2,
        dense_units: int = 64,
    ) -> models.Sequential:
        """
        Build and compile the LSTM model.

        Args:
            input_features: Number of input features
            lstm_units: Number of LSTM units (default: 128)
            dropout_rate: Dropout rate for regularization (default: 0.2)
            dense_units: Dense layer units (default: 64)

        Returns:
            Compiled Keras model
        """
        try:
            self.model = models.Sequential(
                [
                    # First LSTM layer
                    layers.LSTM(
                        lstm_units,
                        activation="relu",
                        input_shape=(self.lookback_window, input_features),
                        return_sequences=True,
                    ),
                    layers.Dropout(dropout_rate),
                    # Second LSTM layer
                    layers.LSTM(lstm_units // 2, activation="relu", return_sequences=False),
                    layers.Dropout(dropout_rate),
                    # Dense layers
                    layers.Dense(dense_units, activation="relu"),
                    layers.Dropout(dropout_rate),
                    layers.Dense(32, activation="relu"),
                    # Output layer
                    layers.Dense(1, activation="linear"),
                ]
            )

            # Compile the model
            self.model.compile(optimizer="adam", loss="mse", metrics=["mae"])

            logger.info("Model built successfully")
            self.model.summary()

            return self.model

        except Exception as e:
            logger.error(f"Error building model: {str(e)}")
            raise

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 50,
        batch_size: int = 32,
        verbose: int = 1,
    ) -> Dict:
        """
        Train the LSTM model.

        Args:
            X_train: Training feature sequences
            y_train: Training targets
            X_val: Validation feature sequences
            y_val: Validation targets
            epochs: Number of training epochs (default: 50)
            batch_size: Batch size (default: 32)
            verbose: Verbosity level (default: 1)

        Returns:
            Training history dictionary
        """
        try:
            if self.model is None:
                raise ValueError("Model not built. Call build_model() first.")

            logger.info(f"Starting training with epochs={epochs}, batch_size={batch_size}")

            # Early stopping to prevent overfitting
            early_stop = keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=10, restore_best_weights=True
            )

            self.history = self.model.fit(
                X_train,
                y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_val, y_val),
                callbacks=[early_stop],
                verbose=verbose,
            )

            logger.info("Model training completed")
            return self.history.history

        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            raise

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the model.

        Args:
            X: Input feature sequences

        Returns:
            Predictions array
        """
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")

        return self.model.predict(X, verbose=0)

    def evaluate(
        self, X_test: np.ndarray, y_test: np.ndarray, scaler=None
    ) -> Dict:
        """
        Evaluate the model on test data.

        Args:
            X_test: Test feature sequences
            y_test: Test targets
            scaler: MinMaxScaler for inverse transform (optional)

        Returns:
            Dictionary with evaluation metrics
        """
        try:
            # Get predictions
            y_pred = self.predict(X_test)

            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            mape = self._calculate_mape(y_test, y_pred)

            metrics = {
                "mse": float(mse),
                "rmse": float(rmse),
                "mae": float(mae),
                "mape": float(mape),
            }

            logger.info(f"Evaluation metrics - RMSE: {rmse:.6f}, MAE: {mae:.6f}, MAPE: {mape:.4f}%")

            return metrics

        except Exception as e:
            logger.error(f"Error during evaluation: {str(e)}")
            raise

    @staticmethod
    def _calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Percentage Error.

        Args:
            y_true: Actual values
            y_pred: Predicted values

        Returns:
            MAPE value
        """
        return np.mean(np.abs((y_true - y_pred.flatten()) / y_true)) * 100

    def save_model(self, filepath: str) -> None:
        """
        Save the trained model to disk.

        Args:
            filepath: Path to save the model
        """
        try:
            if self.model is None:
                raise ValueError("No model to save. Train a model first.")

            self.model.save(filepath)
            logger.info(f"Model saved to {filepath}")

        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

    def load_model(self, filepath: str) -> None:
        """
        Load a trained model from disk.

        Args:
            filepath: Path to the saved model
        """
        try:
            self.model = keras.models.load_model(filepath)
            logger.info(f"Model loaded from {filepath}")

        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
