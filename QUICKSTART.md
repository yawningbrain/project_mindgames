# Emotiv LSL - Quick Start Guide

Get started with Emotiv LSL in 5 minutes!

## Prerequisites

- ✅ Python 3.9 or higher
- ✅ Emotiv EPOC X headset with USB dongle
- ✅ Emotiv App installed

## Installation

### Linux/macOS (Automated)

```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

### Windows (Automated)

```bash
scripts\setup_env.bat
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install
pip install -e .
```

## Setup Headset

1. **Open Emotiv App**
2. **Connect EPOC X via USB cable** to your computer (needed for configuration)
3. **Disable Motion Data**:
   - Click the hamburger menu (three dots) next to your device in Emotiv App
   - Select "Configuration"
   - Turn off "Motion Data"
   - Disconnect USB cable
4. **Connect Wirelessly**:
   - Plug in USB dongle
   - Turn on headset
   - Wait for green lights (dongle and headset connected)

## Run Server

```bash
# Activate environment (if not already)
source venv/bin/activate  # or venv\Scripts\activate

# Start server
python main.py
```

You should see:
```
INFO - Emotiv EPOC X LSL Server
INFO - Found matching device: EPOC X
INFO - Starting data acquisition...
```

## Test Reception

### Option 1: BSL Stream Viewer

```bash
# Install BSL
pip install bsl

# Run viewer
bsl_stream_viewer
```

### Option 2: Example Script

```bash
# In a new terminal
python examples/read_data.py
```

You should see data streaming:
```
[4179.35, 4320.51, 4263.84, ...]
```

## Common Issues

### Device Not Found
- ✅ Check USB dongle is plugged in
- ✅ Turn headset on/off
- ✅ Restart Emotiv App

### Permission Denied (Linux)
```bash
sudo usermod -a -G dialout $USER
# Then logout/login
```

### Import Errors
```bash
pip install -e .
```

## Configuration

Edit `config.py` or create `.env`:

```bash
SRATE=256          # Match Emotiv App
LOG_LEVEL=INFO     # DEBUG for troubleshooting
```

## Next Steps

- 📖 Read full [README.md](README.md)
- 💡 Check [examples/](examples/) for more
- 🐛 [Troubleshooting Guide](README.md#troubleshooting)
- 🤝 [Contributing](CONTRIBUTING.md)

## Getting Help

- 🔍 Check [README.md](README.md) troubleshooting section
- 💬 Open an [issue](https://github.com/your-repo/emotiv-lsl/issues)
- 📧 Contact maintainers

---

**Pro Tip**: Run with `--log-level DEBUG` to see detailed information:
```bash
python main.py --log-level DEBUG
```

Happy Streaming! 🧠✨

