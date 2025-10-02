# Getting Started with Emotiv LSL

Complete step-by-step guide to set up and use the Emotiv EPOC X LSL server.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Hardware Setup](#hardware-setup)
4. [Starting the Server](#starting-the-server)
5. [Recording Data](#recording-data)
6. [Analyzing Data](#analyzing-data)
7. [Stopping the Server](#stopping-the-server)
8. [Troubleshooting](#troubleshooting)
9. [Exit Criteria](#exit-criteria)

---

## Prerequisites

### Required Software

- **Python 3.9 or higher** - [Download here](https://www.python.org/downloads/)
- **Homebrew** (macOS only) - [Install here](https://brew.sh/)
- **Emotiv App** - [Download here](https://www.emotiv.com/emotiv-launcher/)

### Required Hardware

- **Emotiv EPOC X** EEG headset
- **USB dongle** (included with headset)
- **USB cable** (for initial configuration)

### Verify Python Version

```bash
python3 --version
# Should show: Python 3.9.x or higher
```

---

## Installation

### Automated Setup (Recommended)

```bash
cd /path/to/emotiv-lsl-main
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

This will automatically:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up system requirements

### Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install the package
pip install -e .

# 5. Install analysis tools (optional but recommended)
pip install -e ".[analysis]"
```

### macOS: Install LSL Library

**Required for macOS only:**

```bash
brew install labstreaminglayer/tap/lsl
```

This installs the Lab Streaming Layer binary library needed for the Python bindings to work.

---

## Hardware Setup

### Step 1: Configure Headset (One-Time Setup)

1. **Open Emotiv App**

2. **Connect EPOC X via USB cable** to your computer
   - Use the USB cable that came with your headset
   - Plug into headset and computer
   - Wait for app to detect device

3. **Disable Motion Data** (CRITICAL):
   - In Emotiv App, find your connected device
   - Click the **hamburger menu** (three dots) next to device name
   - Select **"Configuration"**
   - **Turn OFF "Motion Data"**
   - Click Save/Apply

4. **Disconnect USB cable** from headset

5. **Close Emotiv App** completely
   - Quit from dock/menu bar
   - This is important - app and LSL server cannot run simultaneously

### Step 2: Wireless Connection

1. **Plug in USB dongle** to computer

2. **Turn on headset**
   - Press and hold power button
   - Wait for LED indicators

3. **Wait for connection** (~10-30 seconds)
   - Dongle LED should indicate connection
   - Headset LED should show paired status

---

## Starting the Server

### macOS: Using Helper Script (Easiest)

```bash
./scripts/start_server.sh
```

This script will:
- Stop any running Emotiv services
- Check for required dependencies
- Start server with proper permissions
- Show helpful status messages

**You will be asked for your password** (sudo is required for HID device access on macOS)

### Manual Start (All Platforms)

**macOS:**
```bash
# 1. Stop Emotiv services
sudo killall -9 CortexService CortexSync 2>/dev/null

# 2. Activate environment and set library path
source venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib

# 3. Start server with sudo
sudo bash -c "export DYLD_LIBRARY_PATH=/opt/homebrew/lib && \
              cd $(pwd) && \
              source venv/bin/activate && \
              python main.py"
```

**Linux/Windows:**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

### Expected Output (Success)

```
============================================================
Emotiv EPOC X LSL Server
============================================================
2025-10-01 00:00:00 - EmotivEpocX - INFO - Initializing Emotiv EPOC X...
2025-10-01 00:00:00 - EmotivEpocX - INFO - Searching for Emotiv device...
2025-10-01 00:00:00 - EmotivEpocX - INFO - Found matching device: Brain Computer Interface USB Receiver/Dongle (Serial: UD...)
2025-10-01 00:00:00 - EmotivEpocX - INFO - Encryption cipher initialized successfully
2025-10-01 00:00:00 - EmotivEpocX - INFO - LSL stream 'Epoc X' created successfully
2025-10-01 00:00:00 - EmotivEpocX - INFO - Connected to device: Brain Computer Interface USB Receiver/Dongle
2025-10-01 00:00:00 - EmotivEpocX - INFO - Starting data acquisition...
```

**The server is now streaming!** Leave this terminal open.

---

## Recording Data

Open a **new terminal window** and run one of these:

### Option 1: Quick View (Real-Time Data)

```bash
cd /path/to/emotiv-lsl-main
source venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib  # macOS only
python examples/read_data.py
```

You'll see data streaming:
```
[2375.38, 5426.02, 5856.15, ...] 1222340.624314833
[5583.84, 7351.02, 5550.12, ...] 1222340.631408125
```

Press Ctrl+C to stop.

### Option 2: Record to JSON (Recommended)

```bash
cd /path/to/emotiv-lsl-main
source venv/bin/activate
export DYLD_LIBRARY_PATH=/opt/homebrew/lib  # macOS only
python examples/export_to_json.py
```

This will:
- Record 5 seconds of data (configurable in script)
- Save to `data/json/eeg_data_TIMESTAMP.json`
- Show progress bar
- Validate output

### Option 3: Record to FIF (MNE Format)

```bash
python examples/read_and_export_mne.py
```

Saves to `data/fif/data_TIMESTAMP_raw.fif`

---

## Analyzing Data

### Comprehensive Analysis with Visualizations

```bash
# Analyze most recent JSON file
python examples/analyze_json.py --latest

# Or analyze specific file
python examples/analyze_json.py data/json/eeg_data_20251001_001535.json
```

### Generated Outputs (in `data/plots/`)

1. **`*_timeseries.png`** - Time series for all 14 channels with statistics
2. **`*_frequency.png`** - Power spectral density with frequency bands marked
3. **`*_heatmap.png`** - Activity heatmap showing all channels over time
4. **`*_correlation.png`** - Inter-channel correlation matrix
5. **`*_bandpower.png`** - Frequency band power (Delta, Theta, Alpha, Beta, Gamma)
6. **`*_statistics.json`** - Complete numerical statistics

### Read JSON Data Programmatically

```python
import json

# Load data
with open('data/json/eeg_data_20251001_001535.json', 'r') as f:
    data = json.load(f)

# Access metadata
metadata = data['metadata']
channels = metadata['channels']  # ['AF3', 'F7', ...]
sample_rate = metadata['sample_rate_hz']  # 256
duration = metadata['duration_sec']  # 5.0

# Access samples
samples = data['samples']
first_sample = samples[0]
print(first_sample['time_sec'])  # 0.000
print(first_sample['AF3'])       # Channel value
print(first_sample['lsl_timestamp'])  # Absolute timestamp

# Extract specific channel
af3_values = [s['AF3'] for s in samples]
times = [s['time_sec'] for s in samples]
```

---

## Stopping the Server

### Method 1: Using Helper Script

```bash
./scripts/stop_server.sh
```

### Method 2: From Server Terminal

In the terminal where the server is running:

1. Press **Ctrl+C** multiple times
2. If that doesn't work, press **Ctrl+Z** to suspend
3. Then run: `sudo pkill -f "python main.py"`

### Method 3: From Any Terminal

```bash
sudo pkill -f "python main.py"
```

### Verify Server Stopped

```bash
ps aux | grep "python main.py" | grep -v grep
```

If no output, the server is stopped.

---

## Troubleshooting

### Device Not Found

**Symptoms:**
```
ERROR - Emotiv EPOC X not found. Please ensure the device is connected...
```

**Solutions:**
1. ✅ Check USB dongle is plugged in
2. ✅ Turn headset on and wait for connection lights
3. ✅ Try unplugging and replugging dongle
4. ✅ Check battery level on headset

### Permission Denied / Open Failed

**Symptoms:**
```
OSError: open failed
```

**Solutions (macOS):**
1. ✅ Run server with `sudo` (required on macOS)
2. ✅ Close Emotiv App completely
3. ✅ Run: `sudo killall -9 CortexService CortexSync`
4. ✅ Use `./scripts/start_server.sh` helper

**Solutions (Linux):**
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Logout and login again
```

### LSL Library Not Found (macOS)

**Symptoms:**
```
RuntimeError: LSL binary library file was not found
```

**Solution:**
```bash
brew install labstreaminglayer/tap/lsl
```

Then always set the library path:
```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib
```

Or add to your `~/.zshrc`:
```bash
echo 'export DYLD_LIBRARY_PATH=/opt/homebrew/lib' >> ~/.zshrc
```

### No Stream Found

**Symptoms:**
```
❌ No EEG stream found!
```

**Solutions:**
1. ✅ Make sure LSL server is running
2. ✅ Check server terminal for errors
3. ✅ Verify device is connected
4. ✅ Try restarting the server

### Ctrl+C Doesn't Stop Server

**Solutions:**
1. Use `./scripts/stop_server.sh`
2. Or run: `sudo pkill -f "python main.py"`
3. Press Ctrl+Z then run stop command

---

## Exit Criteria

### Proper Shutdown Procedure

1. **Stop data recording** (Ctrl+C in recording terminal)
2. **Stop LSL server** (`./scripts/stop_server.sh`)
3. **Turn off headset** (save battery)
4. **Deactivate virtual environment** (optional): `deactivate`

### Verification Checklist

- [ ] No Python processes running: `ps aux | grep main.py`
- [ ] Data files saved to `data/` directory
- [ ] Headset is turned off
- [ ] Virtual environment deactivated (if done for the day)

### Optional Cleanup

```bash
# Clean up old data files
./scripts/cleanup_data.sh

# Or manually
rm data/json/*.json    # Delete recordings
rm data/plots/*.png    # Delete visualizations
```

---

## File Organization

### Data Directory Structure

```
data/
├── json/          # JSON recordings
│   └── eeg_data_YYYYMMDD_HHMMSS.json
├── fif/           # MNE format files
│   └── data_YYYYMMDD_HHMMSS_raw.fif
└── plots/         # Analysis visualizations
    ├── *_timeseries.png
    ├── *_frequency.png
    ├── *_heatmap.png
    ├── *_correlation.png
    ├── *_bandpower.png
    └── *_statistics.json
```

### File Sizes (Typical)

| File Type | Duration | Size |
|-----------|----------|------|
| JSON | 5 sec | ~500 KB |
| JSON | 60 sec | ~6 MB |
| FIF | 5 sec | ~100 KB |
| PNG plots | - | 100-500 KB each |

---

## Common Workflows

### Workflow 1: Quick Test

```bash
# Terminal 1: Start server
./scripts/start_server.sh

# Terminal 2: View real-time data
source venv/bin/activate && export DYLD_LIBRARY_PATH=/opt/homebrew/lib
python examples/read_data.py
```

### Workflow 2: Record and Analyze

```bash
# Terminal 1: Start server
./scripts/start_server.sh

# Terminal 2: Record
source venv/bin/activate && export DYLD_LIBRARY_PATH=/opt/homebrew/lib
python examples/export_to_json.py

# Analyze
python examples/analyze_json.py --latest

# Stop server
./scripts/stop_server.sh
```

### Workflow 3: Long Recording Session

```bash
# Edit export_to_json.py first:
# Change: DURATION_SEC = 60  # or desired duration

# Then run
python examples/export_to_json.py
```

---

## Next Steps

### Learn More

- Read [README.md](README.md) for detailed documentation
- Check [examples/](examples/) for more usage patterns
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

### Customize

- Edit `config.py` for default settings
- Create `.env` file for environment-specific config
- Modify analysis scripts for your needs

### Get Help

- Check troubleshooting section above
- Review logs with `--log-level DEBUG`
- Open an issue on GitHub

---

## Quick Reference Card

```
START SERVER:     ./scripts/start_server.sh
STOP SERVER:      ./scripts/stop_server.sh
RECORD JSON:      python examples/export_to_json.py
ANALYZE:          python examples/analyze_json.py --latest
VIEW REAL-TIME:   python examples/read_data.py
CLEANUP DATA:     ./scripts/cleanup_data.sh

DATA LOCATION:    data/json/    (recordings)
PLOTS LOCATION:   data/plots/   (visualizations)
```

---

**You're all set! Happy brain-hacking! 🧠✨**

