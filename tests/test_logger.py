"""Tests for logger module."""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from emotiv_lsl.logger import setup_logger  # noqa: E402


def test_logger_creation():
    """Test logger can be created."""
    logger = setup_logger("test_logger", level="INFO")
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_logger_levels():
    """Test different logging levels."""
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        logger = setup_logger(f"test_{level}", level=level)
        assert logger.level == getattr(logging, level)


def test_logger_output(caplog):
    """Test logger output."""
    logger = setup_logger("test_output", level="INFO")

    with caplog.at_level(logging.INFO):
        logger.info("Test message")

    assert "Test message" in caplog.text
