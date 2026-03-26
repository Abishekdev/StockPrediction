@echo off
REM Stock Prediction Application - Startup Script
REM This script starts all services

echo ========================================
echo  Stock Prediction Application Launcher
echo ========================================
echo.
echo Starting all services...
echo.

REM Get the script's directory
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Check if Python venv exists
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Installing backend dependencies...
    pip install -r backend/requirements.txt > nul 2>&1
    echo Python environment ready.
)

REM Activate Python venv
call .venv\Scripts\activate.bat

REM Start Backend in new window
echo Starting Backend (FastAPI) on port 8000...
start "Stock Prediction - Backend" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend in new window
echo Starting Frontend (React) on port 5173...
start "Stock Prediction - Frontend" cmd /k "cd frontend && npm run dev -- --host 0.0.0.0 --port 5173"

echo.
echo ========================================
echo  Services Starting...
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend:     http://localhost:5173
echo.
echo Press any key to open the application...
pause

REM Open browser
start http://localhost:5173

echo.
echo All services are running!
echo Close the terminal windows to stop the services.
echo.
