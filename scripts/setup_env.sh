#!/bin/bash
# Setup script for emotiv-lsl environment

set -e  # Exit on error

echo "=========================================="
echo "Emotiv LSL Environment Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.9+ is required. Found: Python $python_version"
    echo "Please install Python 3.9 or higher from https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python $python_version detected"
echo ""

# Detect OS
os_type="$(uname -s)"
echo "Detected OS: $os_type"
echo ""

# OS-specific setup
case "$os_type" in
    Linux*)
        echo "Setting up for Linux..."
        
        # Check if running as root
        if [ "$EUID" -ne 0 ]; then 
            echo "⚠️  Note: You may need sudo privileges for udev rules"
        fi
        
        # Create udev rules for Emotiv device
        if [ -f "/etc/udev/rules.d/99-emotiv.rules" ]; then
            echo "✓ udev rules already exist"
        else
            echo "Creating udev rules for Emotiv device..."
            echo 'KERNEL=="hidraw*", ATTRS{idVendor}=="21a1", MODE="0666"' | sudo tee /etc/udev/rules.d/99-emotiv.rules > /dev/null
            sudo udevadm control --reload-rules
            sudo udevadm trigger
            echo "✓ udev rules created"
        fi
        ;;
    Darwin*)
        echo "Setting up for macOS..."
        echo "✓ No additional OS-specific setup required"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "Setting up for Windows..."
        echo "✓ No additional OS-specific setup required"
        ;;
esac
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || true
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null
echo "✓ pip upgraded"
echo ""

# Install package
echo "Installing emotiv-lsl..."
pip install -e . > /dev/null
echo "✓ emotiv-lsl installed"
echo ""

# Ask about development dependencies
read -p "Install development dependencies? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing development dependencies..."
    pip install -e ".[dev]" > /dev/null
    echo "✓ Development dependencies installed"
fi
echo ""

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Creating .env file from .env.example..."
        cp .env.example .env
        echo "✓ .env file created"
        echo "⚠️  Please review and edit .env file if needed"
    fi
fi
echo ""

echo "=========================================="
echo "Setup Complete! ✓"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Configure settings in .env or config.py"
echo ""
echo "3. Connect your Emotiv EPOC X headset"
echo ""
echo "4. Run the LSL server:"
echo "   python main.py"
echo ""
echo "For more information, see README.md"
echo ""

