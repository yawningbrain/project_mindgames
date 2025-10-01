#!/bin/bash
# Streamlit Application Launcher
# Improved script to launch the Emotiv LSL Streamlit app

set -e

echo "🧠 Emotiv LSL Streamlit Application"
echo "====================================="
echo ""

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Function to check if we're in a virtual environment
in_virtualenv() {
    # Check if VIRTUAL_ENV is set or if Python is from a venv
    [ -n "$VIRTUAL_ENV" ] || python3 -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>/dev/null
}

# Check if we're already in a virtual environment
if in_virtualenv; then
    echo "✓ Virtual environment detected"
else
    # Check if local venv exists
    if [ -d "venv" ]; then
        echo "✓ Activating local virtual environment..."
        source venv/bin/activate
    else
        echo "⚠️  No virtual environment detected!"
        echo ""
        echo "Options:"
        echo "  1. Activate an existing virtual environment:"
        echo "     source /path/to/venv/bin/activate"
        echo ""
        echo "  2. Create a new virtual environment:"
        echo "     python3 -m venv venv"
        echo "     source venv/bin/activate"
        echo "     pip install -r requirements.txt"
        echo ""
        exit 1
    fi
fi

# Set library path for macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    export DYLD_LIBRARY_PATH=/opt/homebrew/lib
fi

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Streamlit not found. Installing required packages..."
    pip install -q streamlit plotly pandas python-dotenv
    echo "✓ Installation complete"
fi

# Check for other required packages
if ! python -c "import plotly, pandas" 2>/dev/null; then
    echo "📦 Installing additional dependencies..."
    pip install -q plotly pandas
fi

# Launch Streamlit app
echo ""
echo "🚀 Launching Streamlit application..."
echo ""
echo "ℹ️  The app will open in your browser automatically."
echo "   If not, navigate to: http://localhost:8501"
echo ""
echo "⚠️  Note: Server start/stop requires sudo access on macOS"
echo "          for HID device access"
echo ""

streamlit run streamlit_app.py
