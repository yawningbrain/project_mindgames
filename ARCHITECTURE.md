# Emotiv LSL - Architecture Documentation

**Version:** 1.0.0  
**Last Updated:** October 1, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Design](#component-design)
4. [Data Flow](#data-flow)
5. [Module Structure](#module-structure)
6. [Class Hierarchy](#class-hierarchy)
7. [Configuration System](#configuration-system)
8. [Error Handling Strategy](#error-handling-strategy)
9. [Logging Architecture](#logging-architecture)
10. [Testing Strategy](#testing-strategy)
11. [Security Architecture](#security-architecture)
12. [Performance Considerations](#performance-considerations)
13. [Future Extensibility](#future-extensibility)

---

## Overview

Emotiv LSL is a Python package that provides real-time EEG data streaming from Emotiv EPOC X headsets via the Lab Streaming Layer (LSL) protocol. The architecture is designed for:

- **Reliability**: Robust error handling and recovery
- **Extensibility**: Easy to add support for new Emotiv devices
- **Performance**: Low-latency data streaming (<10ms)
- **Maintainability**: Clean code structure with comprehensive documentation

### Key Technologies

- **Python 3.9+**: Core language
- **hidapi**: USB HID device communication
- **pycryptodome**: AES encryption/decryption
- **pylsl**: Lab Streaming Layer protocol
- **mne-python**: EEG data analysis
- **streamlit**: Web interface

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER LAYER                           │
│  - Python Scripts  - Streamlit App  - CLI Commands      │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                  APPLICATION LAYER                       │
│  - main.py (Entry Point)                                │
│  - examples/ (Usage Examples)                           │
│  - streamlit_app.py (Web Interface)                     │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   CORE LIBRARY                           │
│  emotiv_lsl/                                            │
│  ├── emotiv_base.py (Abstract Base)                    │
│  ├── emotiv_epoc_x.py (EPOC X Implementation)          │
│  ├── logger.py (Logging System)                        │
│  └── __init__.py (Package Exports)                     │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 EXTERNAL INTERFACES                      │
│  - HID (hidapi) - USB Device Access                    │
│  - LSL (pylsl) - Data Streaming                        │
│  - File System - Data Storage                          │
└─────────────────────────────────────────────────────────┘
```

### Physical Architecture

```
Emotiv EPOC X Headset
        │
        │ (Wireless 2.4GHz)
        ▼
USB Dongle (Receiver)
        │
        │ (USB HID)
        ▼
Operating System
        │
        │ (hidapi)
        ▼
emotiv-lsl Package
        │
        │ (pylsl)
        ▼
LSL Network Stream
        │
        │ (Local/Network)
        ▼
Consumer Applications
(MNE, OpenVibe, etc.)
```

---

## Component Design

### Core Components

#### 1. EmotivBase (emotiv_base.py)

**Purpose**: Abstract base class for all Emotiv devices

**Responsibilities**:
- Define device interface contract
- Implement common LSL streaming logic
- Provide main loop for data acquisition
- Handle errors and logging

**Key Methods**:
```python
- get_hid_device() → dict: Find and return device info
- get_stream_info() → StreamInfo: Create LSL stream configuration
- decode_data(data) → list[float]: Decrypt and decode raw data
- validate_data(data) → bool: Verify data integrity
- main_loop(): Run data acquisition loop
```

#### 2. EmotivEpocX (emotiv_epoc_x.py)

**Purpose**: EPOC X specific implementation

**Responsibilities**:
- Device detection and connection
- AES + XOR decryption
- Channel data extraction
- 10-20 electrode mapping

**Key Features**:
- Automatic crypto key generation from serial number
- 14-channel EEG support
- 128/256 Hz sampling rates
- Channel reordering for 10-20 system compliance

#### 3. Logger (logger.py)

**Purpose**: Centralized logging system

**Responsibilities**:
- Configure logging for all modules
- Support multiple output destinations
- Provide formatted, structured logs

**Features**:
- Console and file output
- Configurable log levels
- Module-specific loggers
- Timestamps and context

#### 4. Configuration (config.py)

**Purpose**: Centralized configuration management

**Responsibilities**:
- Environment variable parsing
- Type-safe configuration access
- Default value management

---

## Data Flow

### Streaming Pipeline

```
1. Device Read (32 bytes)
   ↓
2. Data Validation (size check)
   ↓
3. XOR Decryption (0x55)
   ↓
4. AES Decryption (ECB mode)
   ↓
5. Value Extraction (2-byte pairs)
   ↓
6. Microvolts Conversion
   ↓
7. Channel Reordering
   ↓
8. LSL Push (14 channels)
   ↓
9. Consumer Applications
```

### Data Packet Structure

**Raw Packet (32 bytes)**:
```
[0-1]: Header/metadata
[2-15]: Channel data (7 channels × 2 bytes)
[16-17]: Metadata
[18-31]: Channel data (7 channels × 2 bytes)
```

**After Decoding (14 floats)**:
```python
[AF3, F7, F3, FC5, T7, P7, O1, O2, P8, T8, FC6, F4, F8, AF4]
```

### Export Pipeline

```
LSL Stream
   ↓
collect_samples() (export_to_json.py)
   ↓
create_json_structure()
   ↓
JSON File (data/json/)
   ↓
analyze_json.py
   ↓
Visualizations (data/plots/)
```

---

## Module Structure

```
emotiv-lsl-main/
├── emotiv_lsl/           # Core package
│   ├── __init__.py       # Public API exports
│   ├── emotiv_base.py    # Abstract base class
│   ├── emotiv_epoc_x.py  # EPOC X implementation
│   └── logger.py         # Logging system
│
├── examples/             # Usage examples
│   ├── read_data.py      # Basic LSL reading
│   ├── export_to_json.py # JSON export
│   ├── analyze_json.py   # Data analysis
│   └── ...
│
├── tests/                # Test suite
│   ├── test_config.py    # Configuration tests
│   ├── test_logger.py    # Logging tests
│   └── ...
│
├── scripts/              # Helper scripts
│   ├── setup_env.sh      # Environment setup
│   ├── start_server.sh   # Server management
│   └── ...
│
├── data/                 # Data storage
│   ├── json/             # JSON recordings
│   ├── fif/              # MNE format files
│   └── plots/            # Visualizations
│
├── docs/                 # Documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── STREAMLIT_APP.md
│   └── archive/          # Historical docs
│
├── .github/              # GitHub configuration
│   ├── workflows/        # CI/CD
│   └── ISSUE_TEMPLATE/   # Issue templates
│
├── config.py             # Configuration
├── main.py               # Entry point
├── streamlit_app.py      # Web interface
├── setup.py              # Package setup
├── pyproject.toml        # Modern package config
├── requirements.txt      # Dependencies
└── Makefile              # Development commands
```

---

## Class Hierarchy

### Inheritance Structure

```
EmotivBase (Abstract)
    │
    ├── EmotivEpocX (Concrete)
    │
    └── EmotivEpocXPyShark (Alternative)
```

### Class Diagram

```
┌─────────────────────────────────────┐
│         EmotivBase                   │
├─────────────────────────────────────┤
│ + logger: Logger                     │
│ + READ_SIZE: int = 32               │
├─────────────────────────────────────┤
│ + __init__()                        │
│ + get_hid_device() → dict          │
│ + get_stream_info() → StreamInfo   │
│ + decode_data(bytes) → list        │
│ + validate_data(bytes) → bool      │
│ + main_loop()                       │
└─────────────────────────────────────┘
              ▲
              │
┌─────────────┴───────────────────────┐
│      EmotivEpocX                     │
├─────────────────────────────────────┤
│ + cipher: AES                        │
│ + delimiter: str                     │
├─────────────────────────────────────┤
│ + get_crypto_key() → bytearray      │
│ + _convert_value(str, str) → str    │
└─────────────────────────────────────┘
```

---

## Configuration System

### Configuration Hierarchy

1. **Environment Variables** (.env file)
2. **config.py Defaults**
3. **Command-line Arguments**

### Configuration Flow

```python
os.environ → config.py → Application
```

### Key Configuration Parameters

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| SRATE | int | 256 | Sampling rate (Hz) |
| LOG_LEVEL | str | INFO | Logging verbosity |
| STREAM_NAME | str | Epoc X | LSL stream name |
| DEVICE_MANUFACTURER | str | Emotiv | Device filter |

---

## Error Handling Strategy

### Error Handling Levels

1. **Device Level**:
   - RuntimeError for device not found
   - IOError for connection failures
   - Retry logic with exponential backoff

2. **Data Level**:
   - Validation errors logged as warnings
   - Invalid packets skipped
   - Error counter tracked

3. **Application Level**:
   - KeyboardInterrupt for graceful shutdown
   - Exception logging with traceback
   - Clean resource cleanup

### Error Propagation

```
Low-Level Error → Logger → Error Counter → Main Loop Decision
                                              ↓
                                    Continue or Shutdown?
```

---

## Logging Architecture

### Log Levels Usage

- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational messages
- **WARNING**: Recoverable issues (validation failures)
- **ERROR**: Error conditions (failed operations)
- **CRITICAL**: Critical failures (shutdown required)

### Log Format

```
%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s
```

### Example Output

```
2025-10-01 12:00:00 - EmotivEpocX - INFO - emotiv_epoc_x.py:55 - Found matching device: Brain Computer Interface USB Receiver/Dongle
```

---

## Testing Strategy

### Test Structure

```
tests/
├── test_config.py      # Configuration tests
├── test_logger.py      # Logging tests
├── test_json_export.py # Export functionality
└── test_emotiv_*.py    # Device-specific tests (future)
```

### Testing Approach

1. **Unit Tests**: Individual functions and methods
2. **Integration Tests**: End-to-end workflows
3. **Mock Tests**: HID device simulation
4. **Fixture-based**: Reusable test data

### Coverage Goals

- **Current**: 40% (manual testing)
- **Target**: 80%+ (automated testing)

---

## Security Architecture

### Security Layers

1. **Device Access**:
   - Requires elevated permissions (macOS sudo)
   - HID device access control
   - Serial number-based encryption key

2. **Data Encryption**:
   - AES-ECB cipher
   - XOR preprocessing
   - Device-specific keys

3. **Credential Management**:
   - Environment variables only
   - No hardcoded passwords
   - .env file gitignored

4. **Network Security**:
   - LSL streams on localhost by default
   - No external network required

### Threat Model

| Threat | Mitigation |
|--------|------------|
| Credential exposure | .gitignore, security warnings |
| Device access abuse | Sudo for specific commands only |
| Data interception | LSL on localhost |
| Dependency vulnerabilities | Regular updates, safety checks |

---

## Performance Considerations

### Optimization Strategies

1. **Data Processing**:
   - Minimal processing in main loop
   - Pre-compiled cipher objects
   - Efficient list operations

2. **Memory Management**:
   - Stream data, don't buffer
   - Fixed-size packet reads
   - Automatic garbage collection

3. **I/O Performance**:
   - Non-blocking HID reads
   - Buffered file writes
   - LSL zero-copy push

### Performance Metrics

- **Latency**: <10ms (device → LSL)
- **CPU Usage**: <1% on modern hardware
- **Memory**: ~50 MB resident
- **Throughput**: 256 samples/sec × 14 channels

---

## Future Extensibility

### Planned Extensions

1. **Additional Devices**:
   - EmotivInsight class
   - EmotivEpocPlus class
   - Common interface maintained

2. **Processing Pipeline**:
   - Real-time filtering
   - Feature extraction
   - Event detection

3. **Storage Backend**:
   - Database support
   - Cloud storage
   - Compressed formats

4. **Network Streaming**:
   - Remote LSL access
   - Web sockets
   - REST API

### Extension Points

```python
# New device implementation
class EmotivInsight(EmotivBase):
    def get_hid_device(self) -> dict[str, Any]:
        # Insight-specific detection
        pass
    
    def decode_data(self, data: bytes) -> list[float]:
        # Insight-specific decoding
        pass
```

---

## Dependencies Graph

```
emotiv-lsl
├── hidapi (USB HID access)
├── pycryptodome (Encryption)
├── pylsl (LSL protocol)
├── numpy (Numerical operations) [optional]
├── mne (EEG analysis) [optional]
├── streamlit (Web UI) [optional]
├── matplotlib (Plotting) [optional]
└── scipy (Signal processing) [optional]
```

---

## Build and Deployment

### Build Process

```
Source Code → setuptools → Wheel Package → PyPI/GitHub
```

### Deployment Targets

1. **Local Installation**: `pip install -e .`
2. **Virtual Environment**: `venv + requirements.txt`
3. **Container**: Docker (future)
4. **Cloud**: Streamlit Cloud (UI only)

---

## Maintenance and Support

### Code Quality Metrics

- **Type Hints**: 98%+ coverage
- **Docstrings**: 95%+ coverage
- **Test Coverage**: Target 80%+
- **Lint Score**: 9+/10

### Maintenance Tasks

- Dependency updates (monthly)
- Security scans (weekly via CI)
- Documentation updates (per release)
- Performance profiling (quarterly)

---

## References

- [Lab Streaming Layer Documentation](https://labstreaminglayer.readthedocs.io/)
- [Emotiv SDK Documentation](https://emotiv.gitbook.io/cortex-api/)
- [hidapi Documentation](https://github.com/libusb/hidapi)
- [MNE-Python Documentation](https://mne.tools/stable/index.html)

---

**Document Status**: Complete  
**Review Date**: October 1, 2025  
**Next Review**: January 1, 2026

