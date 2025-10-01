# Emotiv LSL (Project MindGames)

[![CI/CD Pipeline](https://github.com/yawningbrain/project_mindgames/actions/workflows/ci.yml/badge.svg)](https://github.com/yawningbrain/project_mindgames/actions/workflows/ci.yml)
[![Streamlit App](https://github.com/yawningbrain/project_mindgames/actions/workflows/streamlit-deploy.yml/badge.svg)](https://github.com/yawningbrain/project_mindgames/actions/workflows/streamlit-deploy.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Lab Streaming Layer (LSL) server for Emotiv EPOC X EEG headset**

Stream real-time EEG data from your Emotiv EPOC X headset via the Lab Streaming Layer protocol for integration with various neuroscience and BCI applications.

Original code adapted from [CyKit](https://github.com/CymatiCorp/CyKit).

---

## 🚀 Quick Reference

```bash
# Setup (one-time)
./scripts/setup_env.sh

# Start server
./scripts/start_server.sh

# Record data (in new terminal)
python examples/export_to_json.py

# Analyze
python examples/analyze_json.py --latest

# Stop server
./scripts/stop_server.sh
```

**📁 Data Location:** `data/json/` (recordings), `data/plots/` (visualizations)

**📖 New User?** Start with [GETTING_STARTED.md](GETTING_STARTED.md)

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Data Management](#data-management)
- [Usage Examples](#usage-examples)
- [Server Management](#server-management)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Features

- ✅ Real-time EEG data streaming via LSL protocol
- ✅ Support for Emotiv EPOC X (14 channels)
- ✅ Automatic device detection and connection
- ✅ AES encryption/decryption of device data
- ✅ Configurable sampling rates (128Hz, 256Hz)
- ✅ **JSON export** with full metadata and timestamps
- ✅ **Comprehensive data analysis** with visualizations
- ✅ Integration with MNE-Python for data export
- ✅ Comprehensive logging and error handling
- ✅ Easy to use Python API
- ✅ Organized data management (json, fif, plots)

## Requirements

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.9 or higher
- **USB**: Available USB port for Emotiv dongle

### Hardware Requirements

- Emotiv EPOC X EEG headset
- Emotiv USB dongle (included with headset)

### Software Requirements

- **Emotiv App** (for initial device setup and configuration)
- **Homebrew** (macOS only) - for installing LSL library
- LSL-compatible software for data reception (e.g., [BSL Stream Viewer](https://github.com/bsl-tools/bsl)) - optional

## Installation

### Quick Start (Automated - Recommended)

```bash
# Clone the repository
git clone https://github.com/yawningbrain/project_mindgames.git
cd project_mindgames

# Run automated setup
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

### macOS: Install LSL Library (Required)

```bash
brew install labstreaminglayer/tap/lsl
```

### Option 1: Using pip

```bash
# Install with pip
pip install -e .

# For data analysis (includes MNE, numpy, scipy, matplotlib) - Recommended
pip install -e ".[analysis]"

# For development (includes testing tools)
pip install -e ".[dev]"
```

### Option 2: Using Pipenv

```bash
# Clone the repository
git clone https://github.com/yawningbrain/project_mindgames.git
cd project_mindgames

# Install pipenv if you don't have it
pip install pipenv

# Install dependencies
pipenv install

# For development dependencies
pipenv install --dev
```

### Option 3: Using requirements.txt

```bash
# Clone the repository
git clone https://github.com/yawningbrain/project_mindgames.git
cd project_mindgames

# Install core dependencies
pip install -r requirements.txt

# For development dependencies
pip install -r requirements-dev.txt
```

## Quick Start

### 1. Prepare Your Headset

1. **Install Emotiv App**: Download and install the [Emotiv App](https://www.emotiv.com/emotiv-launcher/)
2. **Connect EPOC X via USB**: Connect your EPOC X headset to the computer using a USB cable (required for configuration)
3. **Disable Motion Data** (important!):
   - In Emotiv App, click the hamburger menu (three dots) next to your connected device
   - Select "Configuration"
   - Turn off "Motion Data"
   - Disconnect the USB cable after configuration
4. **Connect Wirelessly**: 
   - Plug in the USB dongle
   - Turn on the headset
   - Wait for both indicators to light up (dongle and headset connection)

### 2. Configure Sampling Rate

Make sure the sampling rate in `config.py` matches your Emotiv App settings:

```python
# In config.py or set environment variable
SRATE = 256  # or 128
```

### 3. Start the LSL Server

**macOS (Recommended - Using Helper Script):**
```bash
./scripts/start_server.sh
```

**macOS (Manual):**
```bash
# Stop Emotiv services first
sudo killall -9 CortexService CortexSync 2>/dev/null

# Start server with sudo (required for HID access)
source venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib

sudo bash -c "export DYLD_LIBRARY_PATH=/opt/homebrew/lib && \
              cd $(pwd) && \
              source venv/bin/activate && \
              python main.py"
```

**Linux/Windows:**
```bash
# Using Python directly
python main.py

# Or with Pipenv
pipenv run python main.py

# With debug logging
python main.py --log-level DEBUG
```

**Success Output:**
```
============================================================
Emotiv EPOC X LSL Server
============================================================
INFO - Initializing Emotiv EPOC X...
INFO - Found matching device: Brain Computer Interface USB Receiver/Dongle
INFO - Encryption cipher initialized successfully
INFO - LSL stream 'Epoc X' created successfully
INFO - Starting data acquisition...
```

**Leave this terminal running!**

### 4. Record and Analyze Data

Open a **new terminal** while the server is running.

#### Record to JSON (Recommended):

```bash
cd /path/to/emotiv-lsl-main
source venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib  # macOS only

# Record 5 seconds of data
python examples/export_to_json.py
```

Output saved to: `data/json/eeg_data_TIMESTAMP.json`

#### Analyze Data with Visualizations:

```bash
# Analyze most recent recording
python examples/analyze_json.py --latest

# Or analyze specific file
python examples/analyze_json.py data/json/eeg_data_20251001_001535.json
```

**Generates 5 plots + statistics** in `data/plots/`:
- Time series for all channels
- Power spectral density
- Activity heatmap
- Channel correlation matrix
- Frequency band power analysis

#### View Real-Time Data:

```bash
python examples/read_data.py
```

Expected output:
```
looking for an EEG stream...
[2375.38, 5426.02, 5856.15, ...] 1222340.624314833
[5583.84, 7351.02, 5550.12, ...] 1222340.631408125
```

### 5. Stop the Server

**Using Helper Script:**
```bash
./scripts/stop_server.sh
```

**Manual:**
```bash
# From any terminal
sudo pkill -f "python main.py"

# Or press Ctrl+Z in server terminal, then:
sudo pkill -f "python main.py"
```

## Data Management

### Directory Structure

All data files are automatically organized into:

```
data/
├── json/          # JSON recordings (export_to_json.py)
├── fif/           # MNE format files (read_and_export_mne.py)
└── plots/         # Analysis visualizations (analyze_json.py)
```

### File Naming Convention

- **JSON**: `eeg_data_YYYYMMDD_HHMMSS.json`
- **FIF**: `data_YYYYMMDD_HHMMSS_raw.fif`
- **Plots**: `eeg_data_YYYYMMDD_HHMMSS_[type].png`
- **Statistics**: `eeg_data_YYYYMMDD_HHMMSS_statistics.json`

### Cleanup Data Files

```bash
# Interactive cleanup utility
./scripts/cleanup_data.sh

# Manual cleanup
rm data/json/*.json      # Delete recordings
rm data/plots/*.png      # Delete visualizations
rm data/fif/*.fif        # Delete FIF files
```

### File Size Estimates

| Type | Duration | Size |
|------|----------|------|
| JSON | 5 sec | ~500 KB |
| JSON | 1 min | ~6 MB |
| JSON | 10 min | ~36 MB |
| Plots (set) | - | ~10 MB |
| FIF | 5 sec | ~100 KB |

**Tip:** For long recordings, consider recording in segments or using a database.

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```bash
# Sampling rate (must match Emotiv app)
SRATE=256

# Logging
LOG_LEVEL=INFO
LOG_FILE=  # Leave empty for console only, or specify path like "logs/emotiv.log"

# LSL Stream settings
STREAM_NAME=Epoc X
STREAM_TYPE=EEG

# Device settings
DEVICE_MANUFACTURER=Emotiv
```

### config.py

Alternatively, modify `config.py` directly:

```python
# Device sampling rate (must match Emotiv app settings)
# Common values: 128, 256
SRATE = 256

# Logging configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = ''  # Path to log file, or empty string for console only

# LSL Stream configuration
STREAM_NAME = 'Epoc X'
STREAM_TYPE = 'EEG'
```

## Usage Examples

### Example 1: Record and Analyze (Complete Workflow)

```bash
# Terminal 1: Start server
./scripts/start_server.sh

# Terminal 2: Record data
source venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib  # macOS only
python examples/export_to_json.py

# Analyze the recording
python examples/analyze_json.py --latest

# Stop server
./scripts/stop_server.sh
```

This generates:
- `data/json/eeg_data_*.json` - Full recording with metadata
- `data/plots/*_timeseries.png` - Time series visualization
- `data/plots/*_frequency.png` - Frequency analysis
- `data/plots/*_heatmap.png` - Channel activity heatmap
- `data/plots/*_correlation.png` - Inter-channel correlations
- `data/plots/*_bandpower.png` - Frequency band analysis
- `data/plots/*_statistics.json` - Numerical statistics

### Example 2: Load and Use JSON Data

```python
import json

# Load recording
with open('data/json/eeg_data_20251001_001535.json', 'r') as f:
    data = json.load(f)

# Access metadata
metadata = data['metadata']
print(f"Device: {metadata['device']}")
print(f"Channels: {metadata['channels']}")
print(f"Sample Rate: {metadata['sample_rate_hz']} Hz")
print(f"Duration: {metadata['duration_sec']} seconds")

# Access samples
samples = data['samples']
first_sample = samples[0]
print(f"Time: {first_sample['time_sec']}")
print(f"AF3: {first_sample['AF3']}")

# Extract specific channel
af3_values = [s['AF3'] for s in samples]
timestamps = [s['time_sec'] for s in samples]

# Plot with matplotlib
import matplotlib.pyplot as plt
plt.plot(timestamps, af3_values)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('AF3 Channel')
plt.show()
```

### Example 3: Real-Time Viewing

```python
from pylsl import StreamInlet, resolve_byprop

# Find the EEG stream
print("Looking for an EEG stream...")
streams = resolve_byprop('type', 'EEG', timeout=5.0)
inlet = StreamInlet(streams[0])

# Read samples
while True:
    sample, timestamp = inlet.pull_sample()
    print(f"Channels: {sample}, Time: {timestamp}")
```

### Example 4: Record and Export to MNE

```python
import numpy as np
from mne import create_info
from mne.io.array import RawArray
from pylsl import StreamInlet, resolve_stream
from datetime import datetime

# Configuration
SRATE = 256
DURATION = 10  # seconds
ch_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 
            'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

# Connect to stream
print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# Collect data
buffer = []
n_samples = SRATE * DURATION

print(f"Recording {DURATION} seconds of data...")
for _ in range(n_samples):
    sample, _ = inlet.pull_sample()
    # Convert to volts (data is in microvolts)
    sample = [x / 1000000.0 for x in sample]
    buffer.append(sample)

# Create MNE Raw object
info = create_info(
    sfreq=SRATE,
    ch_names=ch_names,
    ch_types=['eeg'] * len(ch_names)
)

raw = RawArray(np.array(buffer).T, info)

# Save to file
filename = f"data_{datetime.now()}_raw.fif"
raw.save(filename)
print(f"Data saved to {filename}")
```

### Example 5: Custom Processing Pipeline

```python
from pylsl import StreamInlet, resolve_stream
import numpy as np
from scipy import signal

class EEGProcessor:
    def __init__(self, srate=256):
        self.srate = srate
        # Design a bandpass filter (1-50 Hz)
        self.b, self.a = signal.butter(4, [1, 50], 'bandpass', fs=srate)
        
    def filter_sample(self, sample):
        """Apply bandpass filter to a sample"""
        # Note: For real-time filtering, you'd need to use lfilter_zi
        # This is simplified for demonstration
        return signal.lfilter(self.b, self.a, sample)

# Initialize
processor = EEGProcessor()
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# Process samples
while True:
    sample, timestamp = inlet.pull_sample()
    filtered = processor.filter_sample(sample)
    # Do something with filtered data
    print(f"Filtered channels: {filtered}")
```

## Server Management

### Starting the Server

**macOS (Using Helper Script - Recommended):**
```bash
./scripts/start_server.sh
```

This handles:
- Stopping Emotiv services
- Setting library paths
- Running with sudo
- Clear status messages

**All Platforms (Manual):**
```bash
source venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib  # macOS only
python main.py  # Linux/Windows
sudo python main.py  # macOS (if not using helper script)
```

### Stopping the Server

**Using Helper Script:**
```bash
./scripts/stop_server.sh
```

**Manual Methods:**
1. Press `Ctrl+C` in server terminal (may need multiple times on macOS/sudo)
2. Press `Ctrl+Z` then run: `sudo pkill -f "python main.py"`  
3. From any terminal: `sudo pkill -f "python main.py"` (macOS)

**Verify Server Stopped:**
```bash
ps aux | grep "python main.py" | grep -v grep
# No output = server stopped
```

### Server Status Check

```bash
# Check if server is running
ps aux | grep "python main.py" | grep -v grep

# Check for Emotiv service conflicts
ps aux | grep -i emotiv | grep -v grep
```

### Exit Procedures

**Clean Shutdown:**
1. Stop all data recording scripts (Ctrl+C)
2. Stop LSL server (`./scripts/stop_server.sh`)
3. Turn off headset (save battery)
4. Optionally deactivate virtual environment: `deactivate`

**Emergency Shutdown:**
```bash
sudo pkill -9 -f "python main.py"
```

---

## Troubleshooting

### Device Not Found

**Problem**: `RuntimeError: Emotiv EPOC X not found`

**Solutions**:
1. Ensure the USB dongle is plugged in
2. Turn on the headset and wait for connection lights
3. Check if device appears in Emotiv App
4. On Linux, you may need udev rules (see below)
5. Try unplugging and replugging the dongle

### Linux: Permission Denied

**Problem**: `IOError: [Errno 13] Permission denied`

**Solution**: Create udev rules for hidraw device access

```bash
# Create udev rules file
sudo nano /etc/udev/rules.d/99-emotiv.rules

# Add this line (replace VENDOR_ID if needed)
KERNEL=="hidraw*", ATTRS{idVendor}=="21a1", MODE="0666"

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Replug the device
```

### Data Validation Errors

**Problem**: Seeing many "Data validation failed" warnings

**Solutions**:
1. Ensure motion data is disabled in Emotiv App
2. Check headset battery level
3. Verify all electrodes have good contact
4. Try restarting the headset
5. Check sampling rate matches between app and config

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'emotiv_lsl'`

**Solutions**:
1. Ensure you're in the correct directory
2. Install in development mode: `pip install -e .`
3. Or run with: `python -m main` instead of `python main.py`
4. Check your Python version: `python --version` (need 3.9+)

### macOS: Requires sudo

**Problem**: `OSError: open failed` even though device is found

**Solution**:  
On macOS, HID device access requires root privileges. **This is normal behavior.**

```bash
# Use the helper script (recommended)
./scripts/start_server.sh

# Or run manually with sudo
sudo bash -c "export DYLD_LIBRARY_PATH=/opt/homebrew/lib && ..."
```

### macOS: Emotiv Services Conflict

**Problem**: Server starts but then fails with `OSError: open failed`

**Solution**:  
Emotiv's background services (CortexService, CortexSync) claim exclusive access to the device.

```bash
# Stop Emotiv services before starting server
sudo killall -9 CortexService CortexSync

# Or use the helper script which does this automatically
./scripts/start_server.sh
```

### macOS: hidapi Issues

**Problem**: `ImportError: cannot import name 'device' from 'hid'`

**Solution**:
```bash
# Uninstall conflicting packages
pip uninstall hid hidapi

# Install the correct one
pip install hidapi
```

### Can't Stop Server with Ctrl+C

**Problem**: Ctrl+C doesn't stop the server when running with sudo

**Solution**:
```bash
# Use the stop script
./scripts/stop_server.sh

# Or manually
sudo pkill -f "python main.py"
```

### Sampling Rate Mismatch

**Problem**: Data seems incorrect or timestamps are wrong

**Solution**: 
- Ensure `SRATE` in `config.py` matches Emotiv App settings
- Common values are 128 Hz or 256 Hz
- Restart both Emotiv App and emotiv-lsl server after changing

## Architecture

### Channel Layout

The EPOC X provides 14 EEG channels following the international 10-20 system:

```
        AF3    AF4
    F7   F3      F4   F8
        FC5    FC6
    T7             T8
    P7             P8
        O1      O2
```

Channel order: `['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']`

### Data Flow

```
Emotiv Headset → USB Dongle → HID Interface → 
emotiv-lsl (decrypt & decode) → LSL Stream → 
Your Application
```

### Project Structure

```
emotiv-lsl/
├── emotiv_lsl/              # Main package
│   ├── __init__.py          # Package initialization
│   ├── emotiv_base.py       # Base class for Emotiv devices
│   ├── emotiv_epoc_x.py     # EPOC X implementation
│   ├── emotiv_epoc_x_pyshark.py  # Alternative PyShark implementation
│   └── logger.py            # Logging configuration
│
├── examples/                # Usage examples
│   ├── read_data.py         # Real-time data viewing
│   ├── export_to_json.py    # Record to JSON format ⭐ NEW
│   ├── analyze_json.py      # Comprehensive analysis ⭐ NEW
│   ├── read_json.py         # JSON data utilities
│   └── read_and_export_mne.py  # MNE format export
│
├── scripts/                 # Utility scripts
│   ├── setup_env.sh         # Automated environment setup
│   ├── start_server.sh      # Start LSL server ⭐ NEW
│   ├── stop_server.sh       # Stop LSL server ⭐ NEW
│   └── cleanup_data.sh      # Data cleanup utility ⭐ NEW
│
├── data/                    # Data directory (auto-created) ⭐ NEW
│   ├── json/                # JSON recordings
│   ├── fif/                 # MNE format files
│   └── plots/               # Analysis visualizations
│
├── config.py                # Configuration file
├── main.py                  # Main entry point
├── setup.py                 # Package installation
├── requirements.txt         # Core dependencies
├── requirements-dev.txt     # Development dependencies
├── Pipfile                  # Pipenv configuration
├── .gitignore              # Git ignore rules
│
├── README.md               # This file (comprehensive guide)
├── GETTING_STARTED.md      # Step-by-step tutorial ⭐ NEW
├── QUICKSTART.md           # 5-minute quick start
├── CONTRIBUTING.md         # Contribution guidelines
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT License
└── PROJECT_SUMMARY.md      # Technical summary
```

## Performance

- **Sampling Rate**: 128 Hz or 256 Hz (configurable)
- **Latency**: < 10ms typical
- **Channels**: 14 EEG channels
- **Resolution**: ~0.51 μV per bit

## Compatibility

### Tested Operating Systems

- ✅ macOS 12+ (Monterey, Ventura, Sonoma)
- ✅ Windows 10/11
- ✅ Ubuntu 20.04+
- ✅ Debian 11+

### Tested Python Versions

- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12

## Documentation

This project includes comprehensive documentation for different needs:

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Complete reference guide | All users |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Step-by-step tutorial | First-time users |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute quick start | Experienced users |
| [REQUIREMENTS.md](REQUIREMENTS.md) | Dependencies & system requirements | All users |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development guidelines | Contributors |
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | Visual project guide | All users |
| [CHANGELOG.md](CHANGELOG.md) | Version history | All users |

### Quick Links

- 🆕 **New to this project?** → Start with [GETTING_STARTED.md](GETTING_STARTED.md)
- ⚡ **Just want to run it?** → See [QUICKSTART.md](QUICKSTART.md)
- 🔧 **Having issues?** → Check [Troubleshooting](#troubleshooting) section
- 🤝 **Want to contribute?** → Read [CONTRIBUTING.md](CONTRIBUTING.md)
- 📊 **Understanding data?** → See [Data Management](#data-management) section

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yawningbrain/project_mindgames.git
cd project_mindgames

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Run tests (when available)
pytest

# Format code
black .

# Type checking
mypy emotiv_lsl/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original [CyKit](https://github.com/CymatiCorp/CyKit) implementation
- [Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) project
- [MNE-Python](https://mne.tools/) for EEG analysis tools
- Emotiv Inc. for the EPOC X hardware

## Citation

If you use this software in your research, please cite:

```bibtex
@software{emotiv_lsl,
  title = {Emotiv LSL: Lab Streaming Layer Server for Emotiv EPOC X},
  author = {Emotiv LSL Contributors},
  year = {2025},
  url = {https://github.com/your-repo/emotiv-lsl}
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/emotiv-lsl/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/emotiv-lsl/discussions)
- **Emotiv Support**: https://www.emotiv.com/support/

## Related Projects

- [pylsl](https://github.com/labstreaminglayer/liblsl-Python) - Python bindings for LSL
- [BSL](https://github.com/bsl-tools/bsl) - Brain Streaming Layer tools
- [MNE-Python](https://mne.tools/) - MEG + EEG analysis in Python
- [BrainFlow](https://github.com/brainflow-dev/brainflow) - Library for biosignal acquisition

---

**Made with ❤️ for the neuroscience and BCI community**
