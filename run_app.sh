#!/bin/bash
# Launch Streamlit App

set -e

echo "🧠 Emotiv LSL Streamlit App"
echo "=============================="
echo ""

# Activate venv if exists, or use current Python
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No virtual environment found"
    echo "Run: ./scripts/setup_env.sh"
    exit 1
fi

# macOS library path
[[ "$OSTYPE" == "darwin"* ]] && export DYLD_LIBRARY_PATH=/opt/homebrew/lib

# Install streamlit if needed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Installing Streamlit..."
    pip install -q streamlit plotly pandas python-dotenv
fi

# Launch
echo "🚀 Launching..."
streamlit run streamlit_app.py
