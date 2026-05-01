@echo off
REM LinkShield Development Environment Setup

echo.
echo ========================================
echo LinkShield - Development Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/4] Setting up backend...
cd backend
if not exist ".venv" (
    python -m venv .venv
    call .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
) else (
    call .venv\Scripts\Activate.ps1
)
cd ..

echo [2/4] Setting up frontend...
cd frontend
if not exist "node_modules" (
    npm install
)
cd ..

echo [3/4] Creating .env file if not exists...
if not exist ".env" (
    copy .env.example .env
    echo .env file created from .env.example
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start development:
echo   1. Backend (in one terminal):
echo      cd backend && .\.venv\Scripts\Activate.ps1 && python app.py
echo.
echo   2. Frontend (in another terminal):
echo      cd frontend && npm start
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
pause
