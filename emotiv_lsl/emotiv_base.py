"""Base class for Emotiv EEG devices."""

from __future__ import annotations

import logging
from typing import Any

import hid
from pylsl import StreamInfo, StreamOutlet

from emotiv_lsl.logger import setup_logger
from config import LOG_LEVEL, LOG_FILE


class EmotivBase:
    """Base class for Emotiv EEG devices with LSL streaming."""
    
    READ_SIZE = 32

    def __init__(self):
        """Initialize the Emotiv base class."""
        self.logger = setup_logger(
            name=self.__class__.__name__,
            level=LOG_LEVEL,
            log_file=LOG_FILE if LOG_FILE else None
        )

    def get_hid_device(self) -> dict[str, Any]:
        """
        Get the HID device information.
        
        Returns:
            Dictionary containing device information
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement get_hid_device()")

    def get_stream_info(self) -> StreamInfo:
        """
        Get the LSL stream information.
        
        Returns:
            StreamInfo object for LSL streaming
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement get_stream_info()")

    def decode_data(self, data: bytes) -> list[float]:
        """
        Decode raw data from the device.
        
        Args:
            data: Raw bytes from the device
            
        Returns:
            List of decoded channel values
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement decode_data()")

    def validate_data(self, data: bytes) -> bool:
        """
        Validate the received data.
        
        Args:
            data: Raw bytes from the device
            
        Returns:
            True if data is valid, False otherwise
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement validate_data()")

    def main_loop(self):
        """
        Main loop for reading data from device and streaming via LSL.
        
        Raises:
            Exception: If device connection fails or other errors occur
        """
        packet_count = 0
        error_count = 0
        
        try:
            self.logger.info("Initializing LSL stream...")
            stream_info = self.get_stream_info()
            outlet = StreamOutlet(stream_info)
            self.logger.info(f"LSL stream '{stream_info.name()}' created successfully")

            self.logger.info("Connecting to HID device...")
            device = self.get_hid_device()
            hid_device = hid.device()
            hid_device.open_path(device['path'])
            self.logger.info(f"Connected to device: {device.get('product_string', 'Unknown')}")

            self.logger.info("Starting data acquisition...")
            
            while True:
                try:
                    data = hid_device.read(self.READ_SIZE)
                    
                    if self.validate_data(data):
                        decoded = self.decode_data(data)
                        outlet.push_sample(decoded)
                        packet_count += 1
                        
                        if packet_count % 1000 == 0:
                            self.logger.debug(f"Processed {packet_count} packets")
                    else:
                        error_count += 1
                        if error_count % 100 == 0:
                            self.logger.warning(
                                f"Data validation failed {error_count} times. "
                                f"Last data length: {len(data)}"
                            )
                            
                except KeyboardInterrupt:
                    self.logger.info("Keyboard interrupt received, shutting down...")
                    raise
                except Exception as e:
                    self.logger.error(f"Error processing data: {e}", exc_info=True)
                    error_count += 1
                    if error_count > 1000:
                        self.logger.critical("Too many errors, shutting down...")
                        raise
                        
        except Exception as e:
            self.logger.error(f"Fatal error in main loop: {e}", exc_info=True)
            raise
        finally:
            self.logger.info(f"Session completed. Packets processed: {packet_count}, Errors: {error_count}")
