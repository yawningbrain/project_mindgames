#!/bin/bash
# Streamlit Application Launcher
# Simple script to launch the Emotiv LSL Streamlit app

set -e

echo "🧠 Emotiv LSL Streamlit Application"
echo "====================================="
echo ""

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Set library path for macOS
export DYLD_LIBRARY_PATH=/opt/homebrew/lib

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing Streamlit..."
    pip install streamlit plotly pandas
fi

# Launch Streamlit app
echo "🚀 Launching Streamlit application..."
echo ""
echo "ℹ️  The app will open in your browser automatically."
echo "   If not, navigate to: http://localhost:8501"
echo ""
echo "⚠️  Note: You may need to enter your password when starting/stopping the server"
echo "          (This is required for HID device access on macOS)"
echo ""

streamlit run streamlit_app.py

