@echo off
SET VENV_DIR=venv

REM Check if venv exists
IF EXIST %VENV_DIR%\Scripts\activate (
    echo [+] Virtual environment exists. Activating...
) ELSE (
    echo [+] Creating virtual environment...
    python -m venv %VENV_DIR%
)

call %VENV_DIR%\Scripts\activate

echo [+] Installing dependencies...
pip install --upgrade pip
pip install -r backend\requirements.txt

echo [+] Starting the app...
python app.py

pause
