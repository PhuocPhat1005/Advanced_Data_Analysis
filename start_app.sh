#!/bin/bash

set -e  # Exit on first error
VENV_DIR="venv"
FRONTEND_DIR="frontend"

echo "[+] === Backend setup ==="

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "[+] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "[+] Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "[+] Installing Python dependencies..."
pip install -r requirements.txt

echo "[+] === Frontend setup ==="

# Install Node.js dependencies
cd "$FRONTEND_DIR"
echo "[+] Installing Node dependencies..."
npm install

# Build frontend
echo "[+] Building frontend..."
npm run build

echo "[+] === Start app ==="

# Start frontend in background
echo "[+] Starting frontend in background..."
npm run start &

# Return to root directory
cd ..

# Start backend
echo "[+] Starting backend..."
python app.py
