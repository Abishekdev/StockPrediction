# Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Devices                                │
│              (Web Browser / Mobile Browser)                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ HTTPS/WS
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                   Frontend (React.js)                            │
├─────────────────────────────────────────────────────────────────┤
│ • Dashboard (Price charts, sentiment analysis)                  │
│ • Prediction Page (Make predictions, view history)              │
│ • Portfolio Management (Buy/sell tracking)                      │
│ • Settings (Model retraining, system info)                      │
│ • Authentication (JWT token management)                         │
│ • Real-time Updates (WebSocket integration)                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ REST API + WebSocket
                     │ (HTTP/WS)
┌────────────────────▼────────────────────────────────────────────┐
│                    FastAPI Backend                               │
├─────────────────────────────────────────────────────────────────┤
│ Authentication Layer                                            │
│ • User registration & login                                     │
│ • JWT token generation                                          │
│ • Password hashing (bcrypt)                                     │
│                                                                 │
│ API Endpoints                                                   │
│ • Stock data retrieval                                          │
│ • Price predictions                                             │
│ • Model management                                              │
│ • Portfolio operations                                          │
│ • Sentiment analysis                                            │
│                                                                 │
│ Middleware                                                      │
│ • CORS configuration                                            │
│ • Error handling                                                │
│ • Request validation (Pydantic)                                 │
│ • Logging & monitoring                                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┬──────────────┐
         │           │           │              │
         │           │           │              │
    External APIs   ML Model   Database       Cache
    (Yahoo Finance, (TensorFlow) (PostgreSQL)  (Redis)
     NewsAPI)
```

## Component Architecture

### Frontend Layer (React.js)

#### Structure
```
frontend/
├── src/
│   ├── App.tsx                 # Root component & routing
│   ├── pages/                  # Page components
│   │   ├── Login.tsx           # Authentication page
│   │   ├── Register.tsx        # User registration
│   │   ├── Dashboard.tsx       # Main dashboard
│   │   ├── Prediction.tsx      # Prediction interface
│   │   ├── Portfolio.tsx       # Portfolio management
│   │   └── Settings.tsx        # Settings & model info
│   ├── components/             # Reusable components
│   │   └── Navigation.tsx      # Top navigation bar
│   ├── lib/
│   │   └── api.ts              # API client (axios)
│   ├── index.css               # Global styles
│   └── main.tsx                # React entry point
├── vite.config.ts              # Vite bundler config
├── tailwind.config.ts          # Tailwind CSS config
├── tsconfig.json               # TypeScript config
└── package.json                # Dependencies
```

#### Key Technologies
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Bundler**: Vite
- **State Management**: React hooks
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React
- **Routing**: React Router v6

#### Features
- Responsive design (mobile-first)
- Real-time price updates via WebSocket
- JWT token management
- Error handling & user feedback
- Loading states
- Dark theme/Glass UI design

### Backend Layer (FastAPI)

#### Structure
```
backend/
├── main.py                 # FastAPI application
├── database.py             # SQLAlchemy models
├── schemas.py              # Pydantic request/response
├── sentiment_analysis.py   # NLP sentiment module
├── requirements.txt        # Python dependencies
└── .env.example           # Environment variables
```

#### API Architecture
```
FastAPI Application
│
├── Authentication Routes
│   ├── POST /auth/register
│   └── POST /auth/login
│
├── Stock Data Routes
│   └── GET /stock/data/{ticker}
│
├── Prediction Routes
│   ├── POST /predict
│   ├── GET /predictions
│   └── POST /retrain
│
├── Portfolio Routes
│   ├── GET /portfolio
│   ├── POST /portfolio
│   └── DELETE /portfolio/{id}
│
├── Sentiment Routes
│   └── GET /sentiment/{ticker}
│
├── System Routes
│   ├── GET /health
│   ├── GET /models
│   └── WS /ws/prices/{ticker}
│
└── Middleware
    ├── CORS
    ├── Error handling
    ├── Logging
    └── Authentication
```

#### Security Features
- **Authentication**: JWT tokens
- **Password Security**: bcrypt hashing
- **Input Validation**: Pydantic schemas
- **CORS**: Configured for frontend
- **Error Handling**: Comprehensive exception handling
- **Logging**: Activity tracking

### Machine Learning Layer

#### Model Architecture
```
LSTM Deep Learning Model
│
├── Input Layer
│   └── Shape: (60, 9) - 60 days × 9 features
│
├── LSTM Block 1
│   ├── LSTM(128 units, ReLU, return_sequences=True)
│   ├── Dropout(0.2)
│   └── Output: (60, 128)
│
├── LSTM Block 2
│   ├── LSTM(64 units, ReLU, return_sequences=False)
│   ├── Dropout(0.2)
│   └── Output: (64,)
│
├── Dense Layers
│   ├── Dense(64, ReLU)
│   ├── Dropout(0.2)
│   ├── Dense(32, ReLU)
│   └── Dropout(0.2)
│
└── Output Layer
    └── Dense(1, Linear) - Price prediction
```

#### Input Features (9 dimensions)
1. Close Price
2. Open Price
3. High Price
4. Low Price
5. Volume
6. Moving Average (20-day)
7. Moving Average (50-day)
8. RSI (14-period)
9. MACD

#### Training Pipeline
```
train.py
│
├── 1. Download Data
│   └── yfinance (last 5 years)
│
├── 2. Feature Engineering
│   ├── Calculate technical indicators
│   └── Normalize features (MinMaxScaler)
│
├── 3. Data Preparation
│   ├── Create sequences (60-day window)
│   └── 80/20 train/test split
│
├── 4. Model Training
│   ├── Build LSTM model
│   ├── Train with Adam optimizer
│   ├── Early stopping
│   └── Save model checkpoint
│
└── 5. Evaluation
    ├── Calculate metrics (RMSE, MAE, MAPE)
    ├── Save metadata
    └── Save scaler
```

#### Performance Metrics
- **RMSE** (Root Mean Square Error): Average prediction error
- **MAE** (Mean Absolute Error): Average absolute deviation
- **MAPE** (Mean Absolute Percentage Error): Percentage error

### Database Layer

#### Entity Relationship Diagram
```
Users (1) ──────────── (Many) Predictions
  │                           
  │                           
  └─────────────────────(Many) Portfolio
                              
StockData (independent)
  └─ Cached historical data
```

#### Tables

**Users**
```sql
id (PK)           → Primary key
username          → Unique username
email             → Unique email
hashed_password   → bcrypt hash
created_at        → Timestamp
```

**Predictions**
```sql
id (PK)                 → Primary key
user_id (FK)            → Foreign key to Users
ticker                  → Stock symbol
prediction_date         → When prediction was made
predicted_price         → Model output price
actual_price            → Actual price (nullable)
prediction_window       → Days ahead
metrics (JSON)          → RMSE, MAE, MAPE
created_at              → Timestamp
```

**Portfolio**
```sql
id (PK)                 → Primary key
user_id (FK)            → Foreign key to Users
ticker                  → Stock symbol
quantity                → Number of shares
purchase_price          → Price paid per share
purchase_date           → When purchased
created_at              → Timestamp
```

**StockData** (Optional caching)
```sql
id (PK)          → Primary key
ticker           → Stock symbol
date             → Trading date
open, high, low
close, volume    → OHLCV data
created_at       → Timestamp
```

### External Integrations

#### Yahoo Finance API
```
yfinance
├── Download: Historical stock data (OHLCV)
├── Frequency: Daily
├── Resolution: Historical or real-time quotes
└── Data: 5 years history for model training
```

#### NewsAPI
```
newsapi.org
├── Endpoint: /v2/everything
├── Purpose: Fetch news articles about stocks
├── Usage: Sentiment analysis
└── Integration: sentiment_analysis.py
```

#### Real-time Price Updates
```
WebSocket
├── Protocol: ws://
├── Purpose: Real-time price streaming
├── Frequency: Every 30 seconds
├── Format: JSON { ticker, price, timestamp }
└── Client: Frontend receives updates
```

## Data Flow

### Prediction Request Flow
```
User (Frontend)
    │
    ├─ Enter ticker & days ahead
    │
    ▼
Frontend
    │
    ├─ Validate input
    ├─ Add JWT token
    │
    ▼
Backend (POST /predict)
    │
    ├─ Authenticate user
    ├─ Load LSTM model
    ├─ Fetch last 60 days data
    ├─ Calculate technical indicators
    ├─ Normalize features
    ├─ Generate prediction
    ├─ Inverse transform to price
    ├─ Save to database
    │
    ▼
Response: { predicted_price, metrics, ... }
    │
    ▼
Frontend
    │
    ├─ Display prediction
    ├─ Show metrics
    ├─ Update history
    │
    ▼
User
```

### Portfolio Update Flow
```
User (Frontend)
    │
    ├─ Add stock to portfolio
    │
    ▼
Frontend
    │
    ├─ Validate input
    ├─ Add JWT token
    │
    ▼
Backend (POST /portfolio)
    │
    ├─ Authenticate user
    ├─ Validate ticker
    ├─ Insert into database
    ├─ Fetch current price
    │
    ▼
Response: { portfolio_item, current_price, ... }
    │
    ▼
Frontend
    │
    ├─ Add to portfolio list
    ├─ Calculate gain/loss
    ├─ Update total value
    │
    ▼
User
```

## Deployment Architecture

### Development
```
Developer Machine
├── Backend (localhost:8000)
├── Frontend (localhost:5173)
├── Database (SQLite)
├── ML Model (local filesystem)
└── Redis (optional)
```

### Docker
```
Docker Networks
├── Backend Container
│   ├── FastAPI application
│   ├── Model weights
│   └── Environment variables
├── Frontend Container
│   ├── React build
│   ├── Nginx server
│   └── Environment variables
├── PostgreSQL Container
│   └── Database
└── Redis Container (optional)
    └── Cache
```

### Cloud (Azure)
```
Azure Resource Group
├── Container Registry
│   ├── Backend image
│   └── Frontend image
├── Container Instances
│   └── Backend (with PostgreSQL)
├── Static Web App
│   └── Frontend (with CDN)
├── PostgreSQL Server
│   └── Database
└── Application Insights
    └── Monitoring & logging
```

## Scalability Considerations

### Horizontal Scaling
- Load balancer (nginx, HAProxy)
- Multiple backend instances
- Database read replicas

### Performance Optimization
- Redis caching (predictions, user data)
- CDN for frontend assets
- Database indexing
- Query optimization

### Asynchronous Processing
- Celery for model training
- RabbitMQ for task queue
- Background jobs for retraining

## Security Architecture

```
                      HTTPS
          ┌──────────────────────┐
          │   Frontend (Client)   │
          └──────────┬───────────┘
                     │
                     ▼
              CORS Validation
          ┌──────────────────────┐
          │    FastAPI Backend    │
          ├──────────────────────┤
          │  JWT Authentication  │
          ├──────────────────────┤
          │  Input Validation    │
          │  (Pydantic)          │
          ├──────────────────────┤
          │  Rate Limiting       │
          ├──────────────────────┤
          │  SQLInjection        │
          │  Prevention (ORM)    │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │     PostgreSQL       │
          │  (Encrypted Pass)    │
          └──────────────────────┘
```

## Monitoring & Logging

```
Application Logs
├── Backend logs → File + Console
├── Frontend errors → Browser console
└── Database queries → Query logs

Monitoring
├── Application performance
├── API response times
├── Database performance
├── Error rates
├── Resource usage (CPU, memory)
└── Availability

Alerts
├── High error rate
├── Slow API response
├── Database connection errors
├── Model accuracy degradation
└── System outages
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18, TypeScript, Tailwind, Vite | User interface |
| **Backend** | FastAPI, Python 3.11, Uvicorn | API server |
| **ML** | TensorFlow, Keras, scikit-learn | Model training & prediction |
| **Database** | PostgreSQL, SQLAlchemy | Data persistence |
| **Cache** | Redis | Performance optimization |
| **Authentication** | JWT, bcrypt | Security |
| **External APIs** | yfinance, NewsAPI | Data sources |
| **Deployment** | Docker, Docker Compose | Containerization |
| **Cloud** | Azure, AWS, Heroku | Hosting |

---

For implementation details, see [README.md](README.md) and [DEPLOYMENT.md](DEPLOYMENT.md).
