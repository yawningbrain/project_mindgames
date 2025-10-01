#!/bin/bash
# Start Emotiv LSL Server (macOS optimized)

set -e

# Activate venv if exists
[ -d "venv" ] && source venv/bin/activate

# macOS specific
if [[ "$OSTYPE" == "darwin"* ]]; then
    export DYLD_LIBRARY_PATH=/opt/homebrew/lib
    sudo killall -9 CortexService CortexSync 2>/dev/null || true
    
    echo "🚀 Starting server (sudo required for HID access)..."
    sudo bash -c "export DYLD_LIBRARY_PATH=/opt/homebrew/lib && \
                  cd $(pwd) && \
                  source venv/bin/activate 2>/dev/null || true && \
                  python main.py"
else
    python main.py
fi
