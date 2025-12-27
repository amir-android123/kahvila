@echo off
title Wolt Crawler - Automatic Product Monitor
color 0A

echo ============================================
echo   Wolt Crawler - Starting...
echo ============================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if requests library is installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install requests beautifulsoup4
    echo.
)

REM Run the crawler
echo Starting crawler...
echo Press Ctrl+C to stop
echo.
python wolt_crawler.py

pause
