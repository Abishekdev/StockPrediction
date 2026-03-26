# Complete Stock Prediction Application Setup Guide

## 🚀 Quick Start (All-in-One)

### Option 1: One-Click Startup (Windows)
```bash
double-click: start_application.bat
```
This will:
1. Create Python virtual environment (if needed)
2. Install all dependencies
3. Start Backend (FastAPI) on port 8000
4. Start Frontend (React) on port 5173
5. Open the application in your browser

---

## 📋 Manual Setup (For Troubleshooting)

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm 8+
- Git (optional)

### Step 1: Backend Setup

```bash
# Navigate to project
cd e:\StockPrediction

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate    # Windows
# or for PowerShell:
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt

# Start backend
cd backend
uvicorn main:app --reload --port 8000
```

**Backend Running at**: http://localhost:8000

### Step 2: Frontend Setup (New Terminal)

```bash
cd e:\StockPrediction\frontend

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev
```

**Frontend Running at**: http://localhost:5173

### Step 3: (Optional) ML Model Training

```bash
cd e:\StockPrediction\ml_model

# Optional: Create separate venv for ML
python -m venv ml_venv
ml_venv\Scripts\activate

# Install ML dependencies
pip install tensorflow keras

# Train a model
python train.py --ticker AAPL --epochs 50
```

---

## 🌐 Accessing the Application

### Frontend URLs
- **Main App**: http://localhost:5173
- **React Hot Reload**: Changes auto-refresh

### Backend API URLs
- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **Health Check**: http://localhost:8000/api/health

### Database
- **Type**: SQLite (development)
- **File**: `backend/stock_prediction.db`
- **Auto-created** on first run

---

## 👤 First Time Usage

### 1. Register Account
```
Go to http://localhost:5173
Click "Register"
Fill in username, email, password
Submit
```

### 2. Login
```
Enter credentials from registration
Click "Login"
```

### 3. Dashboard
```
View available stocks
See historical data
Current prices
Sentiment analysis
```

### 4. Make Predictions
```
Go to "Prediction" tab
Enter stock ticker (e.g., AAPL, GOOGL, MSFT)
Select days ahead (1-30)
Click "Predict"
View results
```

### 5. Manage Portfolio
```
Go to "Portfolio" tab
Add new holding
Enter quantity, purchase price, date
View portfolio value
Track gains/losses
```

---

## 🔌 API Usage Examples

### Register User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

Response includes JWT token - use in Authorization header:
```bash
-H "Authorization: Bearer <token>"
```

### Get Stock Data
```bash
curl "http://localhost:8000/api/stock/data/AAPL?days=30"
```

### Make Prediction
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "days_ahead": 5
  }'
```

### Get Sentiment Analysis
```bash
curl "http://localhost:8000/api/sentiment/AAPL"
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

---

## 🔧 Configuration

### Environment Variables
Create `.env` file in project root:

```env
# Backend
DATABASE_URL=sqlite:///./stock_prediction.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
NEWS_API_KEY=your-api-key-optional

# Frontend
VITE_API_URL=http://localhost:8000
```

### Port Configuration

#### Change Backend Port
```bash
# In backend terminal
uvicorn main:app --port 8001
# Update frontend API URL
```

#### Change Frontend Port
```bash
# In frontend terminal
npm run dev -- --port 3000
```

---

## 📁 Project Structure

```
StockPrediction/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── database.py         # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── sentiment_analysis.py
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── ml_model/               # ML training
│   ├── model.py            # LSTM model
│   ├── train.py            # Training script
│   ├── data_preprocessing.py
│   └── requirements.txt
├── docker-compose.yml      # Docker deployment
└── README.md
```

---

## 🐛 Troubleshooting

### Problem: Port 8000 Already in Use
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

### Problem: npm install fails
```bash
# Clear npm cache
npm cache clean --force

# Reinstall with legacy peer deps
npm install --legacy-peer-deps
```

### Problem: Python module not found
```bash
# Verify virtual environment is activated
where python  # Should show path in .venv

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Problem: Frontend won't connect to backend
```bash
# Check CORS is enabled in backend (it is by default)
# Verify backend URL in frontend:
# src/ check for API_BASE_URL or similar

# Test backend health
curl http://localhost:8000/api/health
```

### Problem: Database errors
```bash
# Remove old database
rm backend/stock_prediction.db

# Restart backend - it will recreate
```

---

## 📊 Features Overview

### Authentication
- User registration and login
- JWT token-based security
- Password hashing with bcrypt

### Stock Data
- Real-time price fetching (Yahoo Finance)
- Historical data retrieval
- Technical indicators

### Predictions
- LSTM neural network
- Customizable parameters
- Accuracy metrics (RMSE, MAE, MAPE)

### Sentiment Analysis
- News sentiment scoring
- TextBlob NLP
- Real-time analysis

### Portfolio Management
- Add/remove holdings
- Track purchases
- Calculate gains/losses

### Web Features
- Interactive charts (Recharts)
- Real-time updates (WebSocket ready)
- Responsive UI (Tailwind CSS)
- Dark mode support

---

## 📈 Model Training

### Train New Models
```bash
cd ml_model
python train.py --ticker AAPL --epochs 100 --batch_size 32
```

### Parameters
- `--ticker`: Stock symbol (e.g., AAPL, GOOGL, MSFT)
- `--epochs`: Training epochs (default: 50)
- `--batch_size`: Batch size (default: 32)
- `--lstm_units`: LSTM units (default: 128)

### Output
- Trained model saved
- Metrics reported
- Ready for predictions

---

## 🚢 Deployment

### Docker Deployment
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production Checklist
- [ ] Change SECRET_KEY
- [ ] Set DATABASE_URL to PostgreSQL
- [ ] Enable HTTPS
- [ ] Add NEWS_API_KEY
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Set up CI/CD

---

## 📝 Logs

### Backend Logs
- Location: Backend terminal output
- Check for: errors, warnings, INFO messages
- Uvicorn reload info: watches for file changes

### Frontend Logs
- Browser console: F12 → Console tab
- Terminal: Shows build info, HMR updates

### Database Logs
- Location: `backend/stock_prediction.db`
- SQLite doesn't have separate log files

---

## 🔐 Security Notes

⚠️ **Development Only**
- These defaults are for development
- Change SECRET_KEY for production
- Use environment variables for secrets
- Enable HTTPS
- Add rate limiting
- Implement API key rotation

---

## 📞 Support & Help

### Common Commands

```bash
# Stop all services
Ctrl+C in each terminal

# Restart backend
# In backend terminal: Ctrl+C, then run command again

# Clear all cache
# Python: find . -type d -name __pycache__ -exec rm -r {} +
# npm: npm cache clean --force

# Full rebuild
rm -rf backend/.venv frontend/node_modules
python -m venv backend/.venv
npm install
```

### System Info
```bash
python --version
node --version
npm --version
git --version  (if installed)
```

---

## ✅ Verification Checklist

- [ ] Backend running (http://localhost:8000/api/health returns 200)
- [ ] Frontend running (http://localhost:5173 shows app)
- [ ] Can register new account
- [ ] Can login with account
- [ ] Dashboard loads with data
- [ ] Can make predictions
- [ ] API documentation accessible

---

**Status**: ✅ Application Ready
**Last Updated**: March 26, 2026
**Version**: 1.0.0
