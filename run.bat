@echo off
REM run.bat - Startup script for Bright Minds (Windows)

echo ==========================================
echo 🧠 Bright Minds - AI Learning Platform
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
pip install -r backend\requirements.txt

REM Start the backend server
echo.
echo 🚀 Starting Bright Minds AI Backend...
echo 📍 API will run at: http://localhost:5000
echo 📱 Open frontend\index.html in your browser
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo ==========================================
echo.

cd backend
python app.py