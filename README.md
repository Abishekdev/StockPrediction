# Stock Price Prediction Web Application

AI-powered stock price prediction using LSTM deep learning models with real-time sentiment analysis and portfolio tracking.

## 🎯 Features

### Machine Learning
- **LSTM Neural Network**: Advanced deep learning model for time-series forecasting
- **Technical Indicators**: RSI, MACD, Moving Averages
- **Data Normalization**: MinMaxScaler for feature scaling
- **Model Evaluation**: RMSE, MAE, MAPE metrics
- **Hyperparameter Tuning**: Configurable epochs, batch size, LSTM units

### Backend (FastAPI)
- RESTful API with JWT authentication
- Stock data fetching from Yahoo Finance
- Real-time price predictions
- Model retraining endpoint
- WebSocket support for live price updates
- News sentiment analysis using NLP
- User management and prediction history
- Portfolio tracking

### Frontend (React)
- Modern, responsive UI with Tailwind CSS
- Interactive price charts with Recharts
- Real-time stock price visualization
- Sentiment analysis display
- Portfolio management dashboard
- User authentication
- WebSocket real-time updates

### Database
- PostgreSQL for production
- SQLite for development
- User authentication
- Prediction history storage
- Portfolio tracking

### Extra Features
✅ JWT Authentication
✅ News Sentiment Analysis
✅ WebSocket Real-time Updates
✅ Portfolio Tracking
✅ Dockerized Deployment
✅ Comprehensive Error Handling
✅ Logging and Monitoring

## ⚠️ Disclaimer

**IMPORTANT**: Predictions are for educational purposes only. Stock market predictions carry inherent uncertainty and should NEVER be used as your sole basis for investment decisions. Always conduct thorough research and consult with financial professionals before making investment decisions.

## 🏗️ Architecture

```
Stock Prediction App
├── Backend (FastAPI)
│   ├── API Endpoints
│   ├── ML Model Integration
│   ├── Database Layer
│   └── Authentication
├── Machine Learning
│   ├── LSTM Model
│   ├── Data Preprocessing
│   └── Training Pipeline
├── Frontend (React)
│   ├── Dashboard
│   ├── Predictions
│   ├── Portfolio
│   └── Settings
└── Deployment
    ├── Docker
    ├── Docker Compose
    └── Deployment Instructions
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or SQLite for development)
- Docker & Docker Compose (for containerized deployment)
- pip and npm package managers

## 🚀 Installation & Setup

### Option 1: Local Development Setup

#### 1. Clone and Setup Project Structure

```bash
cd StockPrediction
```

#### 2. Create Virtual Environment (Backend)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create Backend .env file

```bash
cp .env.example .env
```

Edit `.env` and update:
```
DATABASE_URL=sqlite:///./stock_prediction.db
SECRET_KEY=your-secret-key-change-in-production
MODEL_DIR=./models
NEWS_API_KEY=your-newsapi-org-key-here
```

#### 5. Install ML Model Dependencies

```bash
cd ../ml_model
pip install -r requirements.txt
```

#### 6. Train Initial Model

```bash
python train.py --ticker AAPL --epochs 50 --batch_size 32 --lstm_units 128
```

This will create `models/AAPL_lstm_model.h5` and metadata files.

#### 7. Setup Frontend

```bash
cd ../frontend
npm install
```

Create `.env`:

```bash
cp .env.example .env
```

Edit `.env`:
```
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

### Option 2: Docker Deployment

#### 1. Build and Run with Docker Compose

```bash
# From project root
docker-compose up -d
```

This will:
- Start PostgreSQL database
- Build and run FastAPI backend
- Build and run React frontend
- Start Redis cache

#### 2. Verify Services

```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

#### 3. Stop Services

```bash
docker-compose down
```

## 🎮 Running the Application

### Local Development

#### Terminal 1: Start Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API docs: `http://localhost:8000/docs`

#### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

#### Terminal 3 (Optional): Train New Models

```bash
cd ml_model
python train.py --ticker GOOGL --epochs 100 --batch_size 32
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Stock Data
- `GET /api/stock/data/{ticker}` - Get historical stock data with technical indicators

### Predictions
- `POST /api/predict` - Generate price prediction
- `GET /api/predictions` - Get user's prediction history
- `GET /api/predictions?ticker=AAPL` - Filter by ticker

### Model Management
- `POST /api/retrain` - Retrain model for a ticker
- `GET /api/models` - List available trained models

### Portfolio
- `POST /api/portfolio` - Add stock to portfolio
- `GET /api/portfolio` - Get user's portfolio
- `DELETE /api/portfolio/{id}` - Remove stock from portfolio

### Sentiment Analysis
- `GET /api/sentiment/{ticker}` - Get news sentiment for ticker

### System
- `GET /api/health` - Health check

### WebSocket
- `WS /ws/prices/{ticker}` - Real-time price stream

## 📊 Model Training Details

### Features Used
- Close Price
- Open Price
- High Price
- Low Price
- Volume
- Moving Average (20-day)
- Moving Average (50-day)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)

### Model Architecture
```
Input Layer (60 timesteps x 9 features)
    ↓
LSTM Layer (128 units, ReLU activation)
Dropout (0.2)
    ↓
LSTM Layer (64 units, ReLU activation)
Dropout (0.2)
    ↓
Dense Layer (64 units, ReLU activation)
Dropout (0.2)
    ↓
Dense Layer (32 units, ReLU activation)
    ↓
Output Layer (1 unit, Linear activation)
```

### Training Parameters
- **Optimizer**: Adam
- **Loss Function**: Mean Squared Error (MSE)
- **Metrics**: Mean Absolute Error (MAE)
- **Lookback Window**: 60 days
- **Train/Test Split**: 80/20

## 📈 Model Performance

Example metrics from AAPL model:

```
Test Metrics:
- RMSE: 2.341567
- MAE: 1.876543
- MAPE: 1.23%
```

*Note: Actual performance varies based on market conditions and training data*

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password security
- **CORS**: Configured for frontend communication
- **Input Validation**: Pydantic schemas for request validation
- **Error Handling**: Comprehensive error responses
- **Logging**: Activity tracking and debugging

## 🗄️ Database Schema

### Users Table
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password
- created_at
```

### Predictions Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- ticker
- prediction_date
- predicted_price
- actual_price
- prediction_window
- metrics (JSON)
- created_at
```

### Portfolio Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- ticker
- quantity
- purchase_price
- purchase_date
- created_at
```

## 📝 Configuration

### Backend Configuration (`backend/.env`)

```env
# Database
DATABASE_URL=sqlite:///./stock_prediction.db

# Security
SECRET_KEY=your-secure-key-here

# Model
MODEL_DIR=./models

# APIs
NEWS_API_KEY=your-newsapi-org-key-here
```

### Frontend Configuration (`frontend/.env`)

```env
# API
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Database connection error**
- Ensure PostgreSQL is running or use SQLite
- Check DATABASE_URL in `.env`

### Frontend Issues

**Port 3000 already in use**
```bash
npm run dev -- --port 3001
```

**API connection error**
- Ensure backend is running
- Check VITE_API_URL in `.env`
- Clear browser cache

### Model Issues

**No model found error**
- Train a model first: `python train.py --ticker AAPL`
- Check MODEL_DIR path

## 📚 Project Structure

```
StockPrediction/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── sentiment_analysis.py   # NLP sentiment module
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Main app component
│   │   ├── pages/              # Page components
│   │   ├── components/         # Reusable components
│   │   ├── lib/
│   │   │   └── api.ts          # API client
│   │   └── index.css           # Global styles
│   ├── package.json
│   └── vite.config.ts
├── ml_model/
│   ├── train.py                # Training script
│   ├── model.py                # LSTM model
│   ├── data_preprocessing.py   # Data preprocessing
│   ├── requirements.txt
│   └── models/                 # Trained models
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
└── README.md
```

## 🚀 Deployment

### Production Deployment on Azure

1. **Create Azure Resources**
   ```bash
   az group create --name stock-pred-rg --location eastus
   az storage account create --name stockpredsa --resource-group stock-pred-rg
   ```

2. **Build Docker Images**
   ```bash
   docker build -f docker/Dockerfile.backend -t stockpred-backend:latest .
   docker build -f docker/Dockerfile.frontend -t stockpred-frontend:latest .
   ```

3. **Push to Container Registry**
   ```bash
   az acr push stockpred-backend:latest
   az acr push stockpred-frontend:latest
   ```

4. **Deploy to Container Instances or App Service**
   - Use Azure Container Instances for quick deployment
   - Or Azure App Service for long-term hosting

### Frontend Deployment on Vercel

1. Push frontend to GitHub
2. Connect repository to Vercel
3. Set environment variables:
   ```
   VITE_API_URL=https://your-backend-api.com/api
   VITE_WS_URL=wss://your-backend-api.com/ws
   ```
4. Deploy

### Backend Deployment on Heroku or AWS

1. Build and push Docker image
2. Deploy using container service
3. Set environment variables
4. Configure database (PostgreSQL)

## 📞 Support and Contributing

For issues or contributions:
1. Create an issue describing the problem
2. Submit a pull request with improvements
3. Follow the existing code style and conventions

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- TensorFlow/Keras for ML framework
- FastAPI for backend framework
- React.js for frontend framework
- Yahoo Finance for stock data
- NewsAPI for sentiment analysis

---

## ⚠️ Final Disclaimer

This application is provided for **educational purposes only**. 

**Key Points**:
- ❌ Do NOT rely solely on these predictions for investment decisions
- ❌ Stock market carries significant financial risk
- ✅ Always conduct thorough research
- ✅ Consult with financial advisors
- ✅ Understand the risks before investing

**Remember**: Past performance does not guarantee future results. Use this tool to learn about ML and finance, not as a trading system.

---

Happy investing and learning! 🚀
