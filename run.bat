@echo off
echo Discord Utils Bot Launcher
echo ========================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please run setup.py first or create .env file manually
    echo.
    set /p choice="Do you want to run setup now? (y/N): "
    if /i "%choice%"=="y" (
        python setup.py
        if %errorlevel% neq 0 (
            echo Setup failed. Please check the errors above.
            pause
            exit /b 1
        )
    ) else (
        echo Please create .env file and try again.
        pause
        exit /b 1
    )
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import discord" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting Discord Utils Bot...
echo Press Ctrl+C to stop the bot
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo Bot exited with an error. Check the error messages above.
    pause
)
