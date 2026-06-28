@echo off
echo.
echo 🚀 PMI Bot Setup Script - Windows
echo ==================================
echo.

REM Check Python
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Install from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies
echo ✓ Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Install Chromium
echo ✓ Installing Chromium...
python -m playwright install chromium
if errorlevel 1 (
    echo ❌ Failed to install Chromium
    pause
    exit /b 1
)

echo.
echo ✅ SETUP COMPLETE!
echo.
echo 🎯 Next steps:
echo.
echo Option 1: Run bot directly
echo   python bot_pmi.py
echo.
echo Option 2: Setup Windows Task Scheduler (auto-start)
echo   1. Create run_bot.bat with: python bot_pmi.py
echo   2. Open Task Scheduler
echo   3. Create task to run run_bot.bat at startup
echo.
echo Option 3: Use Docker Compose
echo   docker-compose up -d
echo.
echo Then open Telegram and use the bot!
echo.
pause
