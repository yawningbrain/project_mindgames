#!/bin/bash
# Start the Emotiv LSL server
# macOS-specific version with sudo and proper library paths

set -e

echo "========================================"
echo "Starting Emotiv LSL Server"
echo "========================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This script is for macOS. For other OS, run: python main.py"
    exit 1
fi

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Project directory: $PROJECT_DIR"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv venv && pip install -e ."
    exit 1
fi

# Check if liblsl is installed
if [ ! -f "/opt/homebrew/lib/liblsl.dylib" ]; then
    echo "⚠️  LSL library not found!"
    echo "   Install with: brew install labstreaminglayer/tap/lsl"
    read -p "   Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Stop any running Emotiv services
echo "🛑 Stopping Emotiv services..."
sudo killall -9 CortexService CortexSync 2>/dev/null || true
echo ""

# Inform user
echo "ℹ️  Starting server with sudo (required for HID device access)"
echo "   You may be prompted for your password."
echo ""
echo "📡 To stop the server:"
echo "   - Press Ctrl+C in this terminal (may need multiple attempts)"
echo "   - Or run: sudo pkill -f 'python main.py'"
echo "   - Or run: ./scripts/stop_server.sh"
echo ""
echo "Press Enter to start..."
read

# Start the server
echo "🚀 Starting LSL server..."
echo ""

sudo bash -c "export DYLD_LIBRARY_PATH=/opt/homebrew/lib && \
              cd '$PROJECT_DIR' && \
              source venv/bin/activate && \
              python main.py"

