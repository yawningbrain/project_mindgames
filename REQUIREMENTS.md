# Requirements and Dependencies

Complete documentation of all system and software requirements for emotiv-lsl.

---

## System Requirements

### Operating Systems

| OS | Version | Status | Notes |
|-----|---------|--------|-------|
| macOS | 10.14+ | ✅ Tested | Requires Homebrew for LSL library |
| Linux (Ubuntu) | 18.04+ | ✅ Tested | May need udev rules |
| Linux (Debian) | 11+ | ✅ Tested | May need udev rules |
| Windows | 10/11 | ✅ Supported | No special requirements |

### Python Versions

| Version | Status | Notes |
|---------|--------|-------|
| 3.9 | ✅ Tested | Minimum required |
| 3.10 | ✅ Tested | Recommended |
| 3.11 | ✅ Tested | Fully supported |
| 3.12 | ✅ Supported | Compatible |
| 3.13 | ⚠️ Untested | May work |
| < 3.9 | ❌ Not supported | Dependencies require 3.9+ |

---

## Hardware Requirements

### Required

- **Emotiv EPOC X EEG Headset** with 14 channels
- **USB Dongle** (included with headset)
- **USB Port** (USB 2.0 or higher)

### For Initial Setup

- **USB Cable** (to connect headset to computer for configuration)

### Recommended

- **Battery**: Ensure headset is charged for reliable operation
- **USB Extension Cable**: If dongle placement needs optimization

---

## Software Dependencies

### Core Dependencies (Production)

These are required for the LSL server to function:

```
hidapi>=0.14.0         # USB HID device interface
pycryptodome>=3.19.0   # AES encryption/decryption
pylsl>=1.16.1          # Lab Streaming Layer Python bindings
```

**Installation:**
```bash
pip install -e .
```

### System Libraries (macOS)

**Lab Streaming Layer Binary Library:**
```bash
brew install labstreaminglayer/tap/lsl
```

This installs `liblsl.dylib` which is required by pylsl on macOS.

**Why needed?**  
The Python `pylsl` package is just a wrapper. It needs the actual LSL library binary to function.

### Analysis Dependencies (Optional but Recommended)

For data export and analysis features:

```
mne>=1.5.1             # EEG/MEG analysis and visualization
numpy>=1.26.0          # Numerical computing
scipy>=1.11.3          # Scientific computing and signal processing
matplotlib>=3.9.0      # Plotting and visualization
```

**Installation:**
```bash
pip install -e ".[analysis]"
```

### Development Dependencies (Optional)

For contributing to the project:

```
pytest>=7.4.0          # Testing framework
pytest-cov>=4.1.0      # Coverage reporting
black>=23.9.0          # Code formatting
flake8>=6.1.0          # Linting
mypy>=1.5.0            # Type checking
pyshark>=0.6           # Network packet capture (optional)
```

**Installation:**
```bash
pip install -e ".[dev]"
```

---

## Platform-Specific Requirements

### macOS

**Required:**
1. **Homebrew** package manager
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **LSL library** via Homebrew
   ```bash
   brew install labstreaminglayer/tap/lsl
   ```

3. **sudo access** - Required for HID device access
   - You'll be prompted for password when starting server
   - This is a macOS security feature for USB device access

4. **Environment variable** - Set before running
   ```bash
   export DYLD_LIBRARY_PATH=/opt/homebrew/lib
   ```
   
   Or add to `~/.zshrc` for persistence:
   ```bash
   echo 'export DYLD_LIBRARY_PATH=/opt/homebrew/lib' >> ~/.zshrc
   source ~/.zshrc
   ```

**Important:** Close Emotiv App before running LSL server (they cannot run simultaneously)

### Linux

**Required:**

1. **udev rules** for HID device access
   
   Create `/etc/udev/rules.d/99-emotiv.rules`:
   ```
   KERNEL=="hidraw*", ATTRS{idVendor}=="21a1", MODE="0666"
   KERNEL=="hidraw*", ATTRS{idVendor}=="1234", MODE="0666"
   ```
   
   Then reload:
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

2. **User group** (alternative to udev rules):
   ```bash
   sudo usermod -a -G dialout $USER
   # Logout and login for changes to take effect
   ```

3. **libusb** (usually pre-installed):
   ```bash
   sudo apt-get install libusb-1.0-0  # Ubuntu/Debian
   ```

### Windows

**No special requirements!**

Standard Python installation and pip are sufficient. No admin/sudo needed.

---

## External Services

### Emotiv App

**Required for:**
- Initial device configuration (disable motion data)
- Firmware updates
- Device pairing

**Download:** https://www.emotiv.com/emotiv-launcher/

**Important:** Must be **closed** when running LSL server

### Optional Tools

**For visualization:**
- BSL Stream Viewer: `pip install bsl`
- Any LSL-compatible viewer

**For analysis:**
- Jupyter Notebook/Lab: `pip install jupyter`
- EEGLAB (MATLAB)
- FieldTrip (MATLAB)

---

## Dependency Installation Methods

### Method 1: pip with setup.py (Recommended)

```bash
# Core only
pip install -e .

# With analysis tools
pip install -e ".[analysis]"

# Everything (development)
pip install -e ".[dev]"
```

### Method 2: requirements.txt

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt
```

### Method 3: Pipenv

```bash
# Install pipenv
pip install pipenv

# Core dependencies
pipenv install

# With development dependencies
pipenv install --dev
```

---

## Minimum Installation

**Absolute minimum to run LSL server:**

1. Python 3.9+
2. Core packages: `pip install -r requirements.txt`
3. macOS only: `brew install labstreaminglayer/tap/lsl`

**Disk space needed:**
- Python packages: ~50 MB
- LSL library (macOS): ~5 MB
- Total: ~55 MB

---

## Recommended Installation

**For full features (record, analyze, visualize):**

1. Python 3.10+
2. All analysis tools: `pip install -e ".[analysis]"`
3. macOS: LSL library via Homebrew

**Disk space needed:**
- Python packages: ~300 MB (includes scipy, matplotlib, mne)
- LSL library: ~5 MB
- Total: ~305 MB

---

## Disk Space for Data

### Recorded Data Files

| Format | Duration | Typical Size |
|--------|----------|--------------|
| JSON (raw) | 5 seconds | ~500 KB |
| JSON (raw) | 60 seconds | ~6 MB |
| JSON (raw) | 10 minutes | ~36 MB |
| FIF (MNE) | 5 seconds | ~100 KB |
| FIF (MNE) | 60 seconds | ~1.2 MB |

### Analysis Outputs

| Type | Per Recording | Notes |
|------|---------------|-------|
| PNG plots | ~10 MB | 5 high-res images |
| Statistics JSON | ~6 KB | Numerical data |

**Recommendation:** Budget 50-100 MB per hour of recording + analysis

---

## Network Requirements

### Local Network (Default)

LSL uses local network multicast for stream discovery:
- **Ports:** UDP ports for LSL (auto-configured)
- **No internet required** for basic operation

### Firewall

No special firewall rules needed for local use. If using across networks, LSL uses:
- UDP port 16571-16574 (default range)

---

## Performance Requirements

### CPU

- **Minimum:** Any modern CPU (2 cores)
- **Recommended:** 4+ cores for concurrent analysis
- **Usage:** < 5% single core for streaming

### RAM

- **Minimum:** 2 GB available
- **Recommended:** 4 GB+ for analysis
- **Usage:** 
  - LSL server: ~50 MB
  - Recording: ~100 MB per 10 minutes
  - Analysis: ~200-500 MB

### Disk I/O

- **Required:** Standard HDD acceptable
- **Recommended:** SSD for large recordings and analysis

---

## Verification Checklist

Use this to verify your installation:

```bash
# 1. Python version
python3 --version
# Expected: Python 3.9.x or higher

# 2. Core packages installed
python -c "import hid, pylsl; from Crypto.Cipher import AES; print('✓ Core packages OK')"

# 3. Analysis packages (if installed)
python -c "import numpy, scipy, matplotlib, mne; print('✓ Analysis packages OK')"

# 4. macOS: LSL library
ls /opt/homebrew/lib/liblsl.dylib
# Expected: file exists

# 5. Virtual environment
which python
# Expected: /path/to/emotiv-lsl/venv/bin/python

# 6. Package installed
python -c "from emotiv_lsl import EmotivEpocX; print('✓ Package installed')"
```

---

## Upgrade Instructions

### Update Python Packages

```bash
# Activate environment
source venv/bin/activate

# Upgrade all packages
pip install --upgrade -e ".[analysis]"
```

### Update LSL Library (macOS)

```bash
brew upgrade labstreaminglayer/tap/lsl
```

### Clean Install

```bash
# Remove virtual environment
rm -rf venv

# Recreate
python3 -m venv venv
source venv/bin/activate
pip install -e ".[analysis]"
```

---

## Troubleshooting Installation

### pip install fails

**Check:**
- Python version: `python --version` (need 3.9+)
- pip version: `pip --version` (upgrade with `pip install --upgrade pip`)
- Virtual environment activated: `which python`

### macOS: brew install fails

**Solution:**
```bash
# Update Homebrew
brew update

# Try again
brew install labstreaminglayer/tap/lsl
```

### Import errors after installation

**Solution:**
```bash
# Verify you're in the virtual environment
which python  # Should show venv/bin/python

# Reinstall
pip install -e ".[analysis]" --force-reinstall
```

---

## Uninstallation

### Remove Package

```bash
pip uninstall emotiv-lsl
```

### Complete Removal

```bash
# Remove virtual environment
rm -rf venv

# Remove data files (optional)
rm -rf data/

# Remove the entire directory
cd ..
rm -rf emotiv-lsl
```

---

**Last Updated:** October 1, 2025  
**Tested Platforms:** macOS 14.6 (Sonoma), Ubuntu 22.04, Windows 11

