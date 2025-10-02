#!/bin/bash
# ONE-COMMAND SETUP AND RUN
# Usage: ./QUICK_START.sh

set -e

echo "╔══════════════════════════════════════════╗"
echo "║     Emotiv LSL - One-Command Setup      ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Install from: https://www.python.org/"
    exit 1
fi

# 2. Setup venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📦 Installing dependencies..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    pip install -e . -q
    
    echo "✓ Setup complete"
else
    echo "✓ Already set up"
    source venv/bin/activate
fi

# 3. Create .env
if [ ! -f ".env" ] && [ -f "env.example" ]; then
    cp env.example .env
    echo "✓ Created .env file"
fi

# 4. Verify installation
python -c "import emotiv_lsl, pylsl, hidapi" 2>/dev/null && echo "✓ All dependencies installed"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║              What to run:                ║"
echo "╠══════════════════════════════════════════╣"
echo "║  1. LSL Server:                          ║"
echo "║     ./scripts/start_server.sh            ║"
echo "║                                          ║"
echo "║  2. Streamlit App:                       ║"
echo "║     ./run_app.sh                         ║"
echo "║                                          ║"
echo "║  3. Record Data:                         ║"
echo "║     source venv/bin/activate             ║"
echo "║     python examples/export_to_json.py    ║"
echo "╚══════════════════════════════════════════╝"
echo ""
