# 🚀 START HERE - Quick Reference Guide

## Choose Your Path (Pick One)

### ⚡ FASTEST PATH - Docker (Recommended for First-Time)
**Time: 2 minutes | Requirements: Docker Desktop only**

```powershell
cd c:\Users\Admin\Documents\StockPrediction
docker-compose up -d
```

Then open: **http://localhost:3000**

✅ One command starts everything  
✅ No system dependencies  
✅ Database included  
✅ All services configured  

---

### 💻 DEVELOPER PATH - Local Setup
**Time: 10-15 minutes | Requirements: Python 3.11+, Node.js 18+**

Open **3 PowerShell terminals** in `c:\Users\Admin\Documents\StockPrediction`:

**Terminal 1 - Backend:**
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm install
npm run dev
```

**Terminal 3 - ML (Train Models):**
```powershell
cd ml_model
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train.py --ticker AAPL --epochs 50
```

Then open: **http://localhost:5173** (or http://localhost:3000 if using port 3000)

✅ Hot reload on file changes  
✅ Full debugging capability  
✅ Direct code access  
✅ Faster iteration  

---

## What Happens After Startup

After either path is running, you can:

1. **Register** - Create account at http://localhost:3000 (or 5173)
2. **Login** - Use your credentials
3. **View Dashboard** - See stock charts and data
4. **Make Prediction** - Enter ticker and predict price
5. **Track Portfolio** - Add stocks to your portfolio
6. **Retrain Models** - Custom hyperparameters in Settings

---

## 🆘 Troubleshooting Quick Links

- **Docker issues?** → See RUNNING_LOCAL_OR_DOCKER.md "Troubleshooting Docker"
- **Local setup issues?** → See RUNNING_LOCAL_OR_DOCKER.md "Troubleshooting Local Setup"
- **Port conflicts?** → See RUNNING_LOCAL_OR_DOCKER.md "Port already in use?"
- **Full guide?** → Read RUNNING_LOCAL_OR_DOCKER.md (comprehensive 300+ lines)

---

## System Check

Before you start, verify you have what you need:

### For Docker Path:
```powershell
docker --version
docker-compose --version
```
Should show version numbers. If not, install [Docker Desktop](https://www.docker.com/products/docker-desktop)

### For Local Path:
```powershell
python --version      # Need 3.11+
node --version        # Need 18+
npm --version         # Need 8+
```

---

## Next: Pick Your Path & Let's Go! 🎯

Reply with:
- **"docker"** → Start with Docker Compose (easiest)
- **"local"** → Set up local development (most control)
- **"check"** → Verify your system first

I'll guide you through step-by-step! ✨
