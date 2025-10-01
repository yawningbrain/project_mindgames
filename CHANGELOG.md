# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-01

### Added

- Initial release of emotiv-lsl
- Support for Emotiv EPOC X EEG headset
- Real-time LSL streaming of 14 EEG channels
- Automatic device detection and connection
- AES encryption/decryption of device data
- Configurable sampling rates (128Hz, 256Hz)
- Comprehensive logging system with configurable levels
- Environment-based configuration via .env files
- Command-line arguments for runtime configuration
- Examples for reading and exporting data with MNE
- Complete documentation with troubleshooting guide
- Setup.py for package installation
- Support for Python 3.9+

### Features

- **Core Functionality**
  - EmotivBase abstract base class for device implementations
  - EmotivEpocX implementation for EPOC X headset
  - LSL stream creation with proper metadata
  - Real-time data decryption and decoding
  - Data validation and error handling

- **Configuration**
  - Environment variable support
  - config.py for default settings
  - Runtime configuration via CLI arguments

- **Logging**
  - Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Console and file logging support
  - Detailed error messages and stack traces
  - Packet count and error tracking

- **Documentation**
  - Comprehensive README with installation instructions
  - Quick start guide
  - Usage examples
  - Troubleshooting section
  - Contributing guidelines
  - API documentation

- **Development**
  - Type hints throughout codebase
  - Docstrings for all public methods
  - Clean project structure
  - Development dependencies specified

### Changed

- Improved error messages with actionable solutions
- Enhanced data validation with detailed logging
- Better separation of concerns in code architecture

### Fixed

- Channel order now correctly matches 10-20 system
- Proper exception handling for device not found
- Thread-safe logging configuration

## [Unreleased]

### Planned

- Support for Emotiv EPOC+ headset
- Support for Emotiv Insight headset
- Unit tests with pytest
- Continuous Integration setup
- Online documentation with Read the Docs
- Additional examples for common use cases
- Performance optimizations
- Windows installer

---

[1.0.0]: https://github.com/your-repo/emotiv-lsl/releases/tag/v1.0.0

