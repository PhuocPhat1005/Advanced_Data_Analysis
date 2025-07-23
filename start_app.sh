#!/bin/bash

VENV_DIR="venv"

echo "[+] Checking virtual environment..."

# Check if venv exists
if [ -d "$VENV_DIR" ]; then
    echo "[+] Virtual environment exists. Activating..."
else
    echo "[+] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

echo "[+] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Starting the app..."
python app.py
