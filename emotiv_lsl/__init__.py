"""Emotiv LSL - Lab Streaming Layer server for Emotiv EPOC X."""

__version__ = "1.0.0"
__author__ = "Emotiv LSL Contributors"

from emotiv_lsl.emotiv_base import EmotivBase
from emotiv_lsl.emotiv_epoc_x import EmotivEpocX

__all__ = ['EmotivBase', 'EmotivEpocX', '__version__']

