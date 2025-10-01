#!/bin/bash
# ONE-COMMAND SETUP AND RUN
# Usage: ./QUICK_START.sh

set -e

echo "╔══════════════════════════════════════════╗"
echo "║     Emotiv LSL - One-Command Setup      ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 1. Setup
if [ ! -d "venv" ]; then
    echo "📦 Setting up..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip -q
    pip install -e . -q
    echo "✓ Setup complete"
else
    echo "✓ Already set up"
    source venv/bin/activate
fi

# 2. Create .env
if [ ! -f ".env" ] && [ -f "env.example" ]; then
    cp env.example .env
fi

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

