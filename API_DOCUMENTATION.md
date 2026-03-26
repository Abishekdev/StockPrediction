# API Documentation

Complete API reference for Stock Prediction application.

## Base URL
```
http://localhost:8000/api
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require JWT token in Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication Endpoints

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123"
}
```

**Response (200)**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Login
```http
POST /auth/login?username=john_doe&password=secure_password_123
```

**Response (200)**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

### Stock Data Endpoints

#### Get Stock Data
```http
GET /stock/data/AAPL?days=100
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "ticker": "AAPL",
  "data": [
    {
      "date": "2024-01-01",
      "open": 150.25,
      "high": 152.30,
      "low": 149.50,
      "close": 151.89,
      "volume": 50000000,
      "ma20": 151.23,
      "ma50": 150.45,
      "rsi": 65.23,
      "macd": 0.75
    }
  ]
}
```

**Query Parameters**
- `days` (integer): Number of days of historical data (default: 100)

### Prediction Endpoints

#### Make Prediction
```http
POST /predict
Authorization: Bearer <token>
Content-Type: application/json

{
  "ticker": "AAPL",
  "days_ahead": 1
}
```

**Response (200)**
```json
{
  "id": 1,
  "ticker": "AAPL",
  "predicted_price": 152.45,
  "prediction_window": 1,
  "metrics": {
    "rmse": 2.341567,
    "mae": 1.876543,
    "mape": 1.23
  },
  "created_at": "2024-01-15T10:30:00"
}
```

**Request Parameters**
- `ticker` (string): Stock ticker symbol (required)
- `days_ahead` (integer): Number of days to predict ahead (1-30, default: 1)

**Error Response (404)**
```json
{
  "detail": "Model not trained for AAPL. Please retrain."
}
```

#### Get Predictions
```http
GET /predictions?ticker=AAPL
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "id": 1,
    "ticker": "AAPL",
    "predicted_price": 152.45,
    "prediction_window": 1,
    "metrics": {...},
    "created_at": "2024-01-15T10:30:00"
  }
]
```

**Query Parameters**
- `ticker` (string, optional): Filter by stock ticker

### Model Management Endpoints

#### Retrain Model
```http
POST /retrain
Authorization: Bearer <token>
Content-Type: application/json

{
  "ticker": "AAPL",
  "epochs": 50,
  "batch_size": 32,
  "lstm_units": 128
}
```

**Response (200)**
```json
{
  "ticker": "AAPL",
  "status": "training_started",
  "message": "Model retraining started for AAPL",
  "metrics": {},
  "timestamp": "2024-01-15T10:30:00"
}
```

**Request Parameters**
- `ticker` (string): Stock ticker (required)
- `epochs` (integer, 10-200): Number of training epochs (default: 50)
- `batch_size` (integer, 8-128): Training batch size (default: 32)
- `lstm_units` (integer, 64-512): LSTM units (default: 128)

#### Get Available Models
```http
GET /models
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "models": [
    {
      "ticker": "AAPL",
      "trained_at": "2024-01-10T12:00:00",
      "lookback_window": 60,
      "lstm_units": 128,
      "batch_size": 32,
      "epochs": 50,
      "training_samples": 1000,
      "test_samples": 250,
      "train_metrics": {
        "rmse": 1.234,
        "mae": 0.987,
        "mape": 0.65
      },
      "test_metrics": {
        "rmse": 2.341,
        "mae": 1.876,
        "mape": 1.23
      }
    }
  ]
}
```

### Portfolio Endpoints

#### Add to Portfolio
```http
POST /portfolio
Authorization: Bearer <token>
Content-Type: application/json

{
  "ticker": "AAPL",
  "quantity": 10.5,
  "purchase_price": 150.00,
  "purchase_date": "2024-01-01T00:00:00"
}
```

**Response (200)**
```json
{
  "id": 1,
  "ticker": "AAPL",
  "quantity": 10.5,
  "purchase_price": 150.00,
  "purchase_date": "2024-01-01T00:00:00",
  "current_price": 152.45,
  "total_value": 1600.725
}
```

#### Get Portfolio
```http
GET /portfolio
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "id": 1,
    "ticker": "AAPL",
    "quantity": 10.5,
    "purchase_price": 150.00,
    "purchase_date": "2024-01-01T00:00:00",
    "current_price": 152.45,
    "total_value": 1600.725
  }
]
```

#### Delete from Portfolio
```http
DELETE /portfolio/1
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "message": "Portfolio item deleted"
}
```

### Sentiment Analysis Endpoints

#### Get Sentiment
```http
GET /sentiment/AAPL
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "ticker": "AAPL",
  "sentiment_score": 0.35,
  "positive_count": 15,
  "negative_count": 5,
  "neutral_count": 10,
  "articles_analyzed": 30,
  "interpretation": "Positive",
  "timestamp": "2024-01-15T10:30:00"
}
```

### System Endpoints

#### Health Check
```http
GET /health
```

**Response (200)**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

## WebSocket Endpoints

### Subscribe to Real-time Prices
```
WS /ws/prices/{ticker}
```

**Example (JavaScript)**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/prices/AAPL');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`${data.ticker}: $${data.price}`);
  // {
  //   "ticker": "AAPL",
  //   "price": 152.45,
  //   "timestamp": "2024-01-15T10:30:00"
  // }
};
```

**Message Format**
```json
{
  "ticker": "AAPL",
  "price": 152.45,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Messages are sent every 30 seconds with the latest stock price.

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid token"
}
```

### 404 Not Found
```json
{
  "detail": "Model not trained for XYZ"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input or parameters
- `401 Unauthorized`: Missing or invalid authentication
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently no rate limiting is implemented. For production, consider implementing:
- API key-based rate limiting
- Per-user rate limits
- Time-based throttling

## Pagination

Currently, endpoints return full result sets. For large datasets, implement pagination:

```http
GET /predictions?page=1&limit=10
```

## OpenAPI Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Code Examples

### Python Requests
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "john",
    "email": "john@example.com",
    "password": "password123"
})

# Login
response = requests.post(f"{BASE_URL}/auth/login", params={
    "username": "john",
    "password": "password123"
})
token = response.json()["access_token"]

# Make prediction
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/predict", 
    json={"ticker": "AAPL", "days_ahead": 1},
    headers=headers
)
print(response.json())
```

### JavaScript (Fetch)
```javascript
const BASE_URL = "http://localhost:8000/api";

// Register
const registerResponse = await fetch(`${BASE_URL}/auth/register`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "john",
    email: "john@example.com",
    password: "password123"
  })
});

// Login
const loginResponse = await fetch(`${BASE_URL}/auth/login?username=john&password=password123`, {
  method: "POST"
});
const { access_token } = await loginResponse.json();

// Make prediction
const predictResponse = await fetch(`${BASE_URL}/predict`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${access_token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    ticker: "AAPL",
    days_ahead: 1
  })
});
const prediction = await predictResponse.json();
console.log(prediction);
```

### cURL
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "password123"
  }'

# Login
curl -X POST "http://localhost:8000/api/auth/login?username=john&password=password123"

# Make prediction
curl -X POST http://localhost:8000/api/predict \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "days_ahead": 1
  }'
```

---

For more information, visit the [README](README.md) or [Deployment Guide](DEPLOYMENT.md).
