"""Configuration for emotiv-lsl."""

import os
from typing import Optional


def get_env_int(key: str, default: int) -> int:
    """Get integer value from environment variable."""
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def get_env_str(key: str, default: str) -> str:
    """Get string value from environment variable."""
    return os.getenv(key, default)


def get_env_bool(key: str, default: bool) -> bool:
    """Get boolean value from environment variable."""
    value = os.getenv(key, str(default))
    return value.lower() in ('true', '1', 'yes', 'on')


# Device sampling rate (must match Emotiv app settings)
# Common values: 128, 256
SRATE = get_env_int('SRATE', 256)

# Logging configuration
LOG_LEVEL = get_env_str('LOG_LEVEL', 'INFO')
LOG_FILE = get_env_str('LOG_FILE', '')

# LSL Stream configuration
STREAM_NAME = get_env_str('STREAM_NAME', 'Epoc X')
STREAM_TYPE = get_env_str('STREAM_TYPE', 'EEG')

# Device configuration
DEVICE_MANUFACTURER = get_env_str('DEVICE_MANUFACTURER', 'Emotiv')

# PyShark configuration (only needed for EmotivEpocXPyShark)
PYSHARK_INTERFACE = get_env_str('PYSHARK_INTERFACE', 'XHC20')