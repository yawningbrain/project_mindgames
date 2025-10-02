"""Tests for configuration module."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config  # noqa: E402


def test_config_values():
    """Test that configuration values are set."""
    assert hasattr(config, "SRATE")
    assert isinstance(config.SRATE, int)
    assert config.SRATE in [128, 256]


def test_log_level():
    """Test logging configuration."""
    assert hasattr(config, "LOG_LEVEL")
    assert config.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def test_stream_configuration():
    """Test LSL stream configuration."""
    assert hasattr(config, "STREAM_NAME")
    assert hasattr(config, "STREAM_TYPE")
    assert isinstance(config.STREAM_NAME, str)
    assert isinstance(config.STREAM_TYPE, str)
