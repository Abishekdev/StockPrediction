@echo off
REM Backend startup script - no virtual environment needed  for this approach
cd /d c:\Users\Admin\Documents\StockPrediction\backend

echo ===================================
echo Backend Setup and Startup
echo ===================================
echo.

echo Step 1: Installing Python packages...
python -m pip install --upgrade pip setuptools wheel --quiet
python -m pip install -r requirements.txt

echo.
echo Step 2: Starting FastAPI server...
echo Server will start on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
