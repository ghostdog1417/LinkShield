#!/bin/bash

# LinkShield Development Environment Setup

echo ""
echo "========================================"
echo "LinkShield - Development Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    exit 1
fi

echo "[1/4] Setting up backend..."
cd backend
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi
cd ..

echo "[2/4] Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

echo "[3/4] Creating .env file if not exists..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from .env.example"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start development:"
echo "  1. Backend (in one terminal):"
echo "     cd backend && source .venv/bin/activate && python app.py"
echo ""
echo "  2. Frontend (in another terminal):"
echo "     cd frontend && npm start"
echo ""
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
