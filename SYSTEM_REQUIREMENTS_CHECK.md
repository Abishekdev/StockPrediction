# ⚠️ System Requirements Not Met

Your system is missing the required tools to run the Stock Prediction application.

## What's Missing

Based on the system check:
- ❌ Python 3.11+ is NOT installed
- ❓ Node.js 18+ (needs verification)
- ❓ Docker Desktop (recommended alternative)

## 🚀 Quick Fix - Choose One Option

### Option A: Install Python + Node.js (Recommended for Development)

**Step 1: Download Python**
- Go to https://www.python.org/downloads/
- Download Python 3.11 or 3.12 (Windows installer)
- Run installer
- ⚠️ **IMPORTANT**: Check "Add Python to PATH"
- Click "Install Now"

**Step 2: Verify Python Installation**
After installation, open PowerShell and run:
```powershell
python --version
py --version
python3 --version
```

One of these should show version 3.11 or higher.

**Step 3: Download Node.js**
- Go to https://nodejs.org/
- Download LTS version (18.x or higher)
- Run installer with defaults
- When complete, restart PowerShell

**Step 4: Verify Node.js Installation**
```powershell
node --version
npm --version
```

---

### Option B: Install Docker Desktop (Easiest - Single Command to Run Everything)

**Step 1: Download Docker Desktop**
- Go to https://www.docker.com/products/docker-desktop
- Download for Windows
- Run installer
- Restart computer when prompted

**Step 2: Verify Docker Installation**
```powershell
docker --version
docker-compose --version
```

**Step 3: Run Application**
```powershell
cd c:\Users\Admin\Documents\StockPrediction
docker-compose up -d
```

Access at: http://localhost:3000

---

## 📋 What Each Tool Does

| Tool | Purpose | Install Time | Why Needed |
|------|---------|--------------|-----------|
| **Python 3.11+** | ML & Backend API | 5 min | Runs FastAPI server and trains models |
| **Node.js 18+** | Frontend React App | 5 min | Builds and runs React user interface |
| **Docker Desktop** | Containerization | 5 min + 30s startup | Runs everything in isolated containers |

---

## 🔄 Next Steps

1. **Install Missing Tools** (pick Option A or B above)
2. **Restart PowerShell** after installation
3. **Run One of These Commands**:

### If you installed Python + Node.js:
```powershell
cd c:\Users\Admin\Documents\StockPrediction

# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2 - Frontend (new PowerShell window)
cd c:\Users\Admin\Documents\StockPrediction\frontend
npm install
npm run dev

# Terminal 3 - ML (new PowerShell window, optional but recommended)
cd c:\Users\Admin\Documents\StockPrediction\ml_model
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train.py --ticker AAPL --epochs 50
```

### If you installed Docker Desktop:
```powershell
cd c:\Users\Admin\Documents\StockPrediction
docker-compose up -d
```

---

## 📱 After Installation & Running

Once services are running, access:
- **Frontend**: http://localhost:3000 (Docker) or http://localhost:5173 (Local)
- **API Documentation**: http://localhost:8000/docs
- **Create Account**: Register → Login → Start using app

---

## 🆘 Still Having Issues?

1. **Restart PowerShell** completely after installing tools
2. **Check PATH**: Run `$env:Path` in PowerShell to verify installation paths
3. **Verify each tool separately**:
   ```powershell
   python --version
   node --version
   npm --version
   docker --version
   ```

4. **If one still fails**, uninstall and reinstall that tool

---

## 📚 Detailed Guides

For complete setup instructions with screenshots, see:
- [SETUP_AND_INSTALLATION.md](SETUP_AND_INSTALLATION.md)
- [RUNNING_LOCAL_OR_DOCKER.md](RUNNING_LOCAL_OR_DOCKER.md)
- [START_HERE.md](START_HERE.md)

---

**Complete these steps and reply when ready! I'll help you run everything.** ✨
