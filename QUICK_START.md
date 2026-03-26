# Quick Start Guide

Get the Stock Prediction application running in 5 minutes!

## ⚡ Fastest Way: Docker Compose

```bash
# 1. Navigate to project
cd StockPrediction

# 2. Start all services
docker-compose up -d

# 3. Wait 30 seconds for services to start

# 4. Train initial model (in new terminal)
docker-compose exec backend python -m ml_model.train --ticker AAPL

# 5. Access the app
```

**Services ready at:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Step 1: Backend Setup (2 min)

```bash
# 1a. Navigate to backend
cd StockPrediction/backend

# 1b. Create Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 1c. Install dependencies
pip install -r requirements.txt

# 1d. Create .env file
echo 'DATABASE_URL=sqlite:///./stock_prediction.db
SECRET_KEY=your-secret-key-here
MODEL_DIR=./models
NEWS_API_KEY=optional' > .env

# 1e. Run backend
python -m uvicorn main:app --reload
```

✅ Backend running at http://localhost:8000

### Step 2: ML Model Training (1-2 min)

```bash
# Open NEW terminal

# 2a. Navigate to ML folder
cd StockPrediction/ml_model

# 2b. Install dependencies
pip install -r requirements.txt

# 2c. Train model
python train.py --ticker AAPL --epochs 20

# ✅ Model trained! Look for:
# - models/AAPL_lstm_model.h5
# - models/AAPL_metadata.json
# - models/AAPL_scaler.pkl
```

### Step 3: Frontend Setup (1-2 min)

```bash
# Open ANOTHER terminal

# 3a. Navigate to frontend
cd StockPrediction/frontend

# 3b. Install dependencies
npm install

# 3c. Create .env file
echo 'VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws' > .env

# 3d. Start development server
npm run dev
```

✅ Frontend running at http://localhost:5173

## 🎯 First Steps in App

### 1. Create Account
- Go to http://localhost:5173
- Click "Register"
- Fill in username, email, password
- Click "Create Account"

### 2. Login
- Username: (what you just created)
- Password: (what you just created)
- Click "Login"

### 3. View Dashboard
- Explore stock data
- See charts and technical indicators
- Check out sentiment analysis

### 4. Make Prediction
- Go to "Predictions"
- Enter ticker (e.g., AAPL)
- Set days ahead (1-30)
- Click "Generate Prediction"
- View predicted price and metrics

### 5. Track Portfolio
- Go to "Portfolio"
- Click "Add Stock"
- Enter ticker, quantity, purchase price
- View gains/losses

## 📊 Test Data

```bash
# Train models for popular stocks
cd StockPrediction/ml_model

python train.py --ticker GOOGL --epochs 20
python train.py --ticker MSFT --epochs 20
python train.py --ticker TSLA --epochs 20
python train.py --ticker AMZN --epochs 20
```

## 🔧 Useful Commands

### Backend
```bash
# Get API docs
curl http://localhost:8000/docs

# Health check
curl http://localhost:8000/api/health

# List available models
curl http://localhost:8000/api/models
```

### Frontend
```bash
# Build for production
npm run build

# Lint code
npm run lint

# Preview production build
npm run preview
```

### Model Training
```bash
# Train with custom parameters
python train.py --ticker AAPL \
  --epochs 100 \
  --batch_size 64 \
  --lstm_units 256

# List all options
python train.py --help
```

### Database (SQLite)
```bash
# View predictions
sqlite3 stock_prediction.db

# Query
> SELECT * FROM predictions;
> SELECT * FROM users;
> SELECT * FROM portfolios;
```

## 🆘 Troubleshooting

### Port Already in Use

**Port 8000 (Backend)**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

**Port 5173 (Frontend)**
```bash
npm run dev -- --port 3000
```

**Port 3000 (Docker Frontend)**
```bash
docker-compose down
docker-compose up -d
```

### Model Error: "No model found"

```bash
# Train a model first
cd ml_model
python train.py --ticker AAPL --epochs 20
```

### Database Connection Error

```bash
# Reset database
rm stock_prediction.db
# Run backend again - it will create new db
```

### API Connection Error

- Ensure backend is running: http://localhost:8000/docs
- Check VITE_API_URL in frontend/.env
- Clear browser cache

### Memory Issues During Training

```bash
# Reduce batch size and LSTM units
python train.py --ticker AAPL \
  --epochs 20 \
  --batch_size 16 \
  --lstm_units 64
```

## 📚 Next Steps

1. **Read Documentation**
   - [API Documentation](API_DOCUMENTATION.md)
   - [Architecture](ARCHITECTURE.md)
   - [Deployment Guide](DEPLOYMENT.md)

2. **Customize**
   - Modify model architecture in `ml_model/model.py`
   - Add new features to frontend
   - Extend API endpoints

3. **Deploy**
   - Docker: `docker-compose up`
   - Azure: Follow DEPLOYMENT.md
   - AWS: Follow DEPLOYMENT.md

4. **Monitor**
   - Check API docs: http://localhost:8000/docs
   - View training logs: `backend/training.log`
   - Monitor frontend console for errors

## 💡 Tips

- **Faster Training**: Use fewer epochs for testing
  ```bash
  python train.py --ticker AAPL --epochs 5
  ```

- **Better Predictions**: Train more epochs
  ```bash
  python train.py --ticker AAPL --epochs 100
  ```

- **Multiple Stocks**: Train different tickers
  ```bash
  for ticker in AAPL GOOGL MSFT TSLA
  do
    python train.py --ticker $ticker --epochs 30
  done
  ```

- **Debug API**: Use Swagger docs
  http://localhost:8000/docs

- **Watch Logs**: In separate terminal
  ```bash
  tail -f backend/training.log
  ```

## ⚠️ Important Reminders

✅ This is for **educational purposes**
✅ Predictions are **not financial advice**
✅ Do extensive research before investing
✅ Always consult a financial advisor
✅ Stock market carries **real financial risk**

## 🎓 Learning Resources

- [TensorFlow/Keras Documentation](https://www.tensorflow.org/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LSTM for Time Series](https://www.deeplearningwizard.com/deep-learning/recurrent-neural-network/lstm/)

## 🐛 Report Issues

If you encounter issues:
1. Check troubleshooting section
2. Review logs (backend/training.log)
3. Check API docs (http://localhost:8000/docs)
4. Review documentation files

## 🚀 Ready to Deploy?

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment options.

---

**Enjoy building with AI and Machine Learning!** 🤖📈
