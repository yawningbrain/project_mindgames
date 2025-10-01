#!/bin/bash
# Stop the Emotiv LSL server

echo "🛑 Stopping Emotiv LSL Server..."

# Find and kill the Python process
sudo pkill -f "python main.py" 2>/dev/null

# Wait a moment
sleep 1

# Check if still running
if pgrep -f "python main.py" > /dev/null; then
    echo "⚠️  Server still running, force killing..."
    sudo pkill -9 -f "python main.py" 2>/dev/null
    sleep 1
fi

# Verify stopped
if ! pgrep -f "python main.py" > /dev/null; then
    echo "✓ Server stopped successfully"
else
    echo "❌ Failed to stop server. Try manually:"
    echo "   sudo pkill -9 -f 'python main.py'"
fi

