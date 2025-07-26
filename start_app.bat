@echo off
SETLOCAL
SET VENV_DIR=venv
SET FRONTEND_DIR=frontend

echo [+] === Backend setup ===

REM Create virtual environment if not exists
IF EXIST %VENV_DIR%\Scripts\activate (
    echo [+] Virtual environment exists.
) ELSE (
    echo [+] Creating virtual environment...
    python -m venv %VENV_DIR%
    IF %ERRORLEVEL% NEQ 0 (
        echo [!] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call %VENV_DIR%\Scripts\activate
IF NOT DEFINED VIRTUAL_ENV (
    echo [!] Failed to activate virtual environment.
    pause
    exit /b 1
)

echo [+] Upgrading pip...
pip install --upgrade pip

echo [+] Installing Python dependencies...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Failed to install Python dependencies.
    pause
    exit /b 1
)

echo [+] === Frontend setup ===

echo [+] Installing Node dependencies...
cd %FRONTEND_DIR%
call npm install
IF %ERRORLEVEL% NEQ 0 (
    echo [!] npm install failed.
    pause
    exit /b 1
)

echo [+] Building frontend...
call npm run build
IF %ERRORLEVEL% NEQ 0 (
    echo [!] npm run build failed.
    pause
    exit /b 1
)

echo [+] === Start app ===

echo [+] Starting frontend...
start cmd /k "cd %CD% & cd %FRONTEND_DIR% & npm run start"

cd ..

echo [+] Starting the app...
python app.py

pause
ENDLOCAL
