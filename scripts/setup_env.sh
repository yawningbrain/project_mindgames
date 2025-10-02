#!/bin/bash
# Simple, robust setup script for emotiv-lsl

set -e

echo "=========================================="
echo "Emotiv LSL - Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Install from: https://www.python.org/"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install
echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install -e . -q

# Create .env if needed
if [ ! -f ".env" ] && [ -f "env.example" ]; then
    cp env.example .env
    echo "✓ Created .env file"
fi

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To start:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
