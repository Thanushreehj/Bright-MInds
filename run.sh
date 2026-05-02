#!/bin/bash
# run.sh - Startup script for Bright Minds

echo "=========================================="
echo "🧠 Bright Minds - AI Learning Platform"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r backend/requirements.txt

# Start the backend server
echo ""
echo "🚀 Starting Bright Minds AI Backend..."
echo "📍 API will run at: http://localhost:5000"
echo "📱 Open frontend/index.html in your browser"
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

cd backend
python app.py