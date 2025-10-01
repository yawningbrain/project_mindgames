"""
Emotiv LSL - Lab Streaming Layer server for Emotiv EPOC X EEG headset.

This package provides a Python interface for streaming EEG data from Emotiv
EPOC X headsets via the Lab Streaming Layer (LSL) protocol.
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Emotiv LSL Contributors"
__license__ = "MIT"

# Public API
from emotiv_lsl.emotiv_base import EmotivBase
from emotiv_lsl.emotiv_epoc_x import EmotivEpocX
from emotiv_lsl.logger import setup_logger

__all__ = [
    "EmotivBase",
    "EmotivEpocX",
    "setup_logger",
    "__version__",
]
