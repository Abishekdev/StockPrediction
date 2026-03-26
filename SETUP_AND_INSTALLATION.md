# Setup & Installation Guide

Complete step-by-step guide to get the Stock Prediction app running on Windows.

---

## Step 1: Choose Your Approach

### Option A: Docker (Recommended - No Extra Installation)
- **Requirements**: Docker Desktop only
- **Time**: ~2 minutes
- **Easier**: Yes, single command
- **Best for**: Quick testing, production-like environment

### Option B: Local Development (Maximum Control)
- **Requirements**: Python 3.11+, Node.js 18+
- **Time**: ~15 minutes
- **Easier**: More setup, but hot reload and direct control
- **Best for**: Active development, debugging

---

## Prerequisites Check

Open PowerShell and run these commands to see what you have installed:

```powershell
# Check Python
python --version

# Check Node.js
node --version

# Check npm
npm --version

# Check Docker
docker --version
docker-compose --version
```

**Requirements Summary:**
- ✅ Windows 10/11
- ✅ PowerShell (included with Windows)
- ✅ One of: Docker Desktop OR (Python 3.11+ AND Node.js 18+)

---

## 🐳 Method 1: Docker Setup (FASTEST - 2 MINUTES)

### Step 1: Install Docker Desktop

If Docker is not installed on your system:

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Restart your computer when prompted
4. Verify installation:
   ```powershell
   docker --version
   docker-compose --version
   ```

### Step 2: Start All Services

```powershell
# Navigate to project
cd c:\Users\Admin\Documents\StockPrediction

# Start all services in background
docker-compose up -d

# Wait 30 seconds for services to initialize...

# Verify all services are running
docker-compose ps
```

**Expected output from `docker-compose ps`:**
```
CONTAINER ID   IMAGE                              NAMES                STATUS
...            postgres:15-alpine                 stock_prediction_db         Up (healthy)
...            stock-prediction-backend           stock_prediction_backend    Up
...            stock-prediction-frontend          stock_prediction_frontend   Up (healthy)
...            redis:7-alpine                     stock_prediction_cache      Up (healthy)
```

### Step 3: Access the Application

Open your browser and navigate to:

- **Frontend App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### Step 4: Train ML Models (Optional but Recommended)

```powershell
# Enter backend container
docker-compose exec backend bash

# Train a model
cd ml_model
python train.py --ticker AAPL --epochs 50 --batch_size 32

# Train more models (optional)
python train.py --ticker GOOGL --epochs 50
python train.py --ticker MSFT --epochs 50

# Exit container
exit
```

### Step 5: Create Account & Login

1. Go to http://localhost:3000
2. Click "Register"
3. Enter username, email, password
4. Click "Login" and enter your credentials
5. Start exploring!

### Docker Useful Commands

```powershell
# View logs of specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose stop

# Start stopped services
docker-compose start

# Remove containers and data
docker-compose down

# Remove everything including volumes (CAREFUL - loses data!)
docker-compose down -v

# Rebuild images after code changes
docker-compose up -d --build
```

---

## 💻 Method 2: Local Development Setup (15 MINUTES)

### Prerequisites Installation

#### Install Python 3.11+

1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```powershell
   python --version
   ```

#### Install Node.js 18+

1. Download from [nodejs.org](https://nodejs.org/) (LTS version recommended)
2. Run installer
3. Accept default settings
4. Complete installation
5. Verify installation:
   ```powershell
   node --version
   npm --version
   ```

#### Install PostgreSQL (Optional - SQLite used by default)

For development, SQLite is sufficient. Only install PostgreSQL if you want production-like setup:

1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer with defaults
3. Remember the password you set

### Local Setup

You'll need **3 PowerShell windows/terminals** open simultaneously.

#### Terminal 1: Backend API

```powershell
# Navigate to backend
cd c:\Users\Admin\Documents\StockPrediction\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (takes 2-3 minutes)
pip install -r requirements.txt

# Create .env file with default values
# (This file already exists with defaults, but here's what it contains:)
# DATABASE_URL=sqlite:///./stock_prediction.db
# SECRET_KEY=dev-secret-key-change-in-production
# MODEL_DIR=../ml_model/models
# NEWS_API_KEY=         (leave empty or add your NewsAPI key)

# Run backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# INFO:     Started server process [XXXX]
# INFO:     Application startup complete
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open and running!**

#### Terminal 2: Frontend React App

```powershell
# Open NEW PowerShell window

# Navigate to frontend
cd c:\Users\Admin\Documents\StockPrediction\frontend

# Install npm packages (takes 1-2 minutes)
npm install

# Create .env file (already exists with defaults)
# VITE_API_URL=http://localhost:8000/api
# VITE_WS_URL=ws://localhost:8000

# Start development server
npm run dev

# You should see:
# VITE v4.x.x  build xxx MB
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

**Keep this terminal open and running!**

#### Terminal 3: ML Model Training

```powershell
# Open NEW PowerShell window

# Navigate to ml_model
cd c:\Users\Admin\Documents\StockPrediction\ml_model

# Create virtual environment (can reuse backend's or create new)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create models directory
mkdir models -ErrorAction SilentlyContinue

# Train first model (takes 5-10 minutes)
python train.py --ticker AAPL --epochs 50 --batch_size 32

# You should see training progress:
# Downloading stock data for AAPL...
# [████████████████████] 100%
# Preparing data sequences...
# Building LSTM model...
# Training model...
# Epoch 1/50
# [████████████████████] 100%
# ...
# Model trained successfully!
```

**Optional: Train more models for other tickers**
```powershell
python train.py --ticker GOOGL --epochs 50
python train.py --ticker MSFT --epochs 50
python train.py --ticker TSLA --epochs 50
```

### Local Development - Access Application

Once all 3 terminals are running, open browser to:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **API Documentation**: http://localhost:8000/docs

### First Steps

1. Browse to http://localhost:5173
2. Register a new account
3. Login with your credentials
4. Go to Dashboard (requires trained model from Terminal 3)
5. Try making a prediction
6. Add stocks to Portfolio
7. Check Settings to retrain models

### Stopping Local Development

```powershell
# In each terminal:
# Press Ctrl+C to stop the service

# All three services stop independently
# Data persists in stock_prediction.db
```

### Restarting Local Development

```powershell
# Just repeat the same commands:
# Terminal 1: uvicorn command
# Terminal 2: npm run dev
# Terminal 3: python train.py or just keep it ready for new training
```

---

## 🆘 Troubleshooting

### Issue: "Port XXXX is already in use"

**Docker solution:**
```powershell
# Edit docker-compose.yml, change port mapping
# For example, change "3000:3000" to "3001:3000"
```

**Local solution:**
```powershell
# Find what's using the port
netstat -ano | findstr :3000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or just use different port:
# Backend: uvicorn main:app --reload --port 8001
# Frontend: npm run dev -- --port 5174
```

### Issue: "ModuleNotFoundError" or package errors

**For Backend/ML:**
```powershell
# Ensure virtual environment is activated
# Look for (venv) at start of PowerShell line

# Reinstall requirements
pip install --upgrade -r requirements.txt

# Or clean and reinstall
pip install --force-reinstall -r requirements.txt
```

**For Frontend:**
```powershell
# Clear node modules and reinstall
rm -r node_modules package-lock.json
npm install
```

### Issue: Frontend can't connect to backend

**Check:**
1. Backend is running on http://localhost:8000/api/health
2. .env file has: `VITE_API_URL=http://localhost:8000/api`
3. No firewall blocking ports
4. Restart frontend: Ctrl+C then `npm run dev`

### Issue: ML models aren't training

```powershell
# Check internet connection (needs to download stock data)
# Try with a different ticker
python train.py --ticker GOOGL

# Check if yfinance can fetch data
python
>>> import yfinance as yf
>>> yf.Ticker('AAPL').info
# Should show stock info
```

### Issue: Database locked or corrupted

**Local (SQLite):**
```powershell
cd backend
del stock_prediction.db
# Database recreates automatically
```

**Docker:**
```powershell
docker-compose down -v
docker-compose up -d
```

---

## 📊 Comparison Table

| Feature | Docker | Local |
|---------|--------|-------|
| Setup Time | 2 min | 15 min |
| System Deps | Docker only | Python, Node.js |
| Commands | 1 command | 3 terminals |
| Code Changes | Rebuild needed | Auto hot-reload |
| Database | PostgreSQL | SQLite (default) |
| Production-like | ✅ Yes | ⚠️ No |
| Development | ⚠️ Harder | ✅ Easier |
| Debugging | docker logs | Direct console |

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] All services running (docker ps or 3 terminals)
- [ ] Frontend loads at http://localhost:3000 or 5173
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Can create account and login
- [ ] ML models are trained (in ml_model/models/)
- [ ] Can make a prediction
- [ ] Can add stocks to portfolio

---

## 🎓 Next Steps

**After everything is running:**

1. **Explore the API** - Visit http://localhost:8000/docs
2. **Train more models** - Add more tickers (AAPL, GOOGL, MSFT, TSLA)
3. **Read Architecture** - See ARCHITECTURE.md
4. **Review Code** - Understand the implementation
5. **Deploy to Cloud** - See DEPLOYMENT.md for Azure/AWS/Heroku

---

## 📞 Need Help?

- **General questions?** → See README.md
- **Running issues?** → See RUNNING_LOCAL_OR_DOCKER.md
- **API details?** → See API_DOCUMENTATION.md
- **System design?** → See ARCHITECTURE.md
- **Quick start?** → See QUICK_START.md

---

**You're all set! Choose Docker or Local, follow the steps, and you'll be running in minutes! 🚀**
