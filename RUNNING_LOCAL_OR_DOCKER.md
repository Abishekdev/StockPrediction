# Running the Stock Prediction App - Local vs Docker

Choose the approach that works best for you:
- **🐳 Docker (Recommended)** - One command, everything included
- **💻 Local Development** - More control, direct code access

---

## 🐳 Option 1: Run with Docker Compose (Easiest)

### Prerequisites
Install on your system:
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker & Docker Compose)

### Quick Start (1 Command)

```bash
cd c:\Users\Admin\Documents\StockPrediction

# Start all services
docker-compose up -d

# Wait 30 seconds for services to start...

# Access the application
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
```

### Verify Everything is Running

```bash
# Check service status
docker-compose ps

# Expected output:
# NAME                        STATUS
# stock_prediction_db         Up (healthy)
# stock_prediction_backend    Up
# stock_prediction_frontend   Up
# stock_prediction_cache      Up (healthy)
```

### Train the ML Model (Docker)

```bash
# SSH into backend container
docker-compose exec backend bash

# Train AAPL model
cd ml_model
python train.py --ticker AAPL --epochs 50 --batch_size 32

# Train other tickers (optional)
python train.py --ticker GOOGL --epochs 50
python train.py --ticker MSFT --epochs 50

# Exit container
exit
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service (backend)
docker-compose logs -f backend

# Specific service (frontend)
docker-compose logs -f frontend
```

### Stop the Application

```bash
# Stop and remove containers
docker-compose down

# Stop but keep data (database will persist)
docker-compose stop

# Restart without rebuilding
docker-compose start
```

### Troubleshooting Docker

**Port already in use?**
```bash
# Change ports in docker-compose.yml and access at new port
# Or kill existing process on that port

# Windows: Find process on port 3000
netstat -ano | findstr :3000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Database connection issues?**
```bash
# Reset database (CAUTION: loses all data)
docker-compose down -v
docker-compose up -d
```

**Services stuck starting?**
```bash
# Complete restart
docker-compose down
docker system prune -a
docker-compose up -d
```

---

## 💻 Option 2: Run Locally (Development)

### Prerequisites

**Windows:**
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- PostgreSQL 15+ (optional - SQLite used by default)

**Verify installations:**
```bash
python --version      # Should be 3.11+
node --version        # Should be 18+
npm --version         # Should be 8+
```

### Setup Local Environment

#### 1. Backend Setup (Terminal 1)

```bash
cd c:\Users\Admin\Documents\StockPrediction\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (if not exists)
# Copy content from .env.example or create:
# DATABASE_URL=sqlite:///./stock_prediction.db
# SECRET_KEY=dev-secret-key-change-in-production
# MODEL_DIR=../ml_model/models
# NEWS_API_KEY=your-optional-key

# Run backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Started server process [XXXX]
# INFO:     Application startup complete
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 2. Machine Learning Setup (Terminal 2)

```bash
cd c:\Users\Admin\Documents\StockPrediction\ml_model

# Create virtual environment (or reuse backend's if desired)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create models directory if it doesn't exist
mkdir models

# Train initial model
python train.py --ticker AAPL --epochs 50 --batch_size 32

# Expected output:
# Downloading stock data for AAPL...
# Calculating technical indicators...
# Preparing data sequences...
# Building LSTM model...
# Training model...
# [Training progress...]
# Model trained successfully!
# Saved to: models/AAPL_lstm_model.h5

# Train more tickers (takes 5 minutes per ticker)
python train.py --ticker GOOGL
python train.py --ticker MSFT
python train.py --ticker TSLA
```

**Training Parameters (Optional):**
```bash
python train.py \
  --ticker AAPL \
  --epochs 100 \
  --batch_size 16 \
  --lstm_units 128 \
  --lookback_window 60

# Default values:
# --epochs: 50
# --batch_size: 32
# --lstm_units: 128
# --lookback_window: 60
```

#### 3. Frontend Setup (Terminal 3)

```bash
cd c:\Users\Admin\Documents\StockPrediction\frontend

# Install dependencies
npm install

# Create .env file (if not exists):
# Copy from .env.example or create with:
# VITE_API_URL=http://localhost:8000/api
# VITE_WS_URL=ws://localhost:8000

# Start development server
npm run dev

# Expected output:
#   VITE v4.x.x  build xx.xx MB
#   ➜  Local:   http://localhost:5173/
#   ➜  press h to show help
```

### Access Local Application

Once all three terminals are running:

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | http://localhost:5173 | Main App (development) |
| **Backend API** | http://localhost:8000 | API Endpoints |
| **API Docs** | http://localhost:8000/docs | Swagger Documentation |
| **Alternative Docs** | http://localhost:8000/redoc | ReDoc Documentation |

### First Steps

1. **Open http://localhost:5173** in your browser
2. **Register** - Create a new account
3. **Login** - Use credentials you created
4. **Dashboard** - View stock data and charts
5. **Predict** - Make a price prediction (requires trained model)
6. **Portfolio** - Add stocks to your portfolio
7. **Settings** - Retrain models with custom parameters

### Local Development Tips

**Hot Reload:**
- Backend changes automatically reload (Uvicorn --reload)
- Frontend changes automatically reload (Vite HMR)
- No need to restart servers

**Database:**
- Local development uses SQLite (stock_prediction.db)
- No database setup required
- Data persists between sessions

**Check Backend Health:**
```bash
# In browser or terminal
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy"}
```

**Clear Cache/Database (Local):**
```bash
# Remove SQLite database
cd backend
del stock_prediction.db

# Remove trained models
cd ../ml_model/models
del *.h5 *.pkl

# Start fresh
```

**Stop Local Services:**
```bash
# Terminal 1: Press Ctrl+C (Backend)
# Terminal 2: Press Ctrl+C (ML training)
# Terminal 3: Press Ctrl+C (Frontend)
```

### Troubleshooting Local Setup

**Port already in use?**
```bash
# Change port in respective service
# Backend: uvicorn main:app --port 8001
# Frontend: npm run dev -- --port 5174

# Or kill process on port
# For port 8000:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Module not found errors?**
```bash
# Ensure virtual environment is activated
# Backend: source venv\Scripts\activate
# Python dependencies: pip install -r requirements.txt
# Frontend: npm install
```

**Database locked?**
```bash
# Close all connections and delete SQLite DB
cd backend
del stock_prediction.db

# Database recreates automatically on first API call
```

**Frontend can't connect to backend?**
```bash
# Verify backend is running: http://localhost:8000/api/health
# Check .env file has correct VITE_API_URL
# VITE_API_URL=http://localhost:8000/api
# Restart frontend: npm run dev
```

**ML model training fails?**
```bash
# Ensure dependencies are installed
pip install -r ml_model/requirements.txt

# Check internet connection (downloads stock data)
# Check yfinance can access Yahoo Finance:
python -c "import yfinance; print(yfinance.Ticker('AAPL').info['symbol'])"
```

---

## 🔄 Comparison: Docker vs Local

| Feature | Docker | Local |
|---------|--------|-------|
| **Setup Time** | 2 minutes | 10-15 minutes |
| **System Dependencies** | Only Docker Desktop | Python, Node.js, optionally PostgreSQL |
| **Port Conflicts** | Can modify in docker-compose.yml | Need to kill processes or change ports |
| **Code Changes** | Rebuild image | Auto-reload (hot reload) |
| **Database** | PostgreSQL in container | SQLite (default) |
| **Production-like** | ✅ Closer to production | ⚠️ Development setup |
| **Performance** | Slight overhead | Faster (no container overhead) |
| **Multiple Versions** | Run multiple versions simultaneously | Need to manage paths |
| **Debugging** | View logs with docker-compose logs | Direct console output |

---

## 🚀 Recommended Workflow

### For Quick Testing (< 5 min)
```bash
docker-compose up -d
# Application ready in 30 seconds
```

### For Development
```bash
# Terminal 1: Backend (Local Python)
cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload

# Terminal 2: Frontend (Local Node.js)
cd frontend && npm install && npm run dev

# Terminal 3: ML Training (as needed)
cd ml_model && python train.py --ticker AAPL
```

### For Production-like Testing
```bash
# Use Docker Compose with production settings
docker-compose -f docker-compose.yml up -d

# Access at http://localhost:3000
```

---

## 📊 Next Steps

### 1. Train Models (if not already done)

**Docker:**
```bash
docker-compose exec backend python ml_model/train.py --ticker AAPL
```

**Local:**
```bash
cd ml_model
python train.py --ticker AAPL --epochs 50
```

### 2. Create Account & Login

- Visit http://localhost:3000 (Docker) or http://localhost:5173 (Local)
- Click "Register"
- Enter username, email, password
- Login with your credentials

### 3. Make Your First Prediction

- Go to Dashboard
- Search for a stock ticker
- Go to Predictions page
- Enter ticker and days ahead
- Click "Predict"

### 4. Explore Features

- **Dashboard** - View stock charts and technicals
- **Predictions** - Make price forecasts
- **Portfolio** - Track your stocks
- **Settings** - Retrain models

---

## 🆘 Getting Help

**Check logs:**
```bash
# Docker
docker-compose logs -f backend

# Local
# Check terminal output directly
```

**API Documentation:**
- Interactive: http://localhost:8000/docs
- Alternative: http://localhost:8000/redoc

**Verify connections:**
```bash
# Backend health
curl http://localhost:8000/api/health

# Database (Docker)
docker-compose exec postgres psql -U stockuser -d stock_prediction -c "SELECT version();"
```

**Still stuck?**
- Check [QUICK_START.md](QUICK_START.md) for additional help
- Review [README.md](README.md) for architecture details
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for endpoint info

---

**Happy coding! 🚀**
