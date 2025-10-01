"""Emotiv EPOC X EEG headset implementation."""

from __future__ import annotations

from typing import Any

import hid
from Crypto.Cipher import AES
from pylsl import StreamInfo

from emotiv_lsl.emotiv_base import EmotivBase
from config import SRATE, STREAM_NAME, DEVICE_MANUFACTURER


class EmotivEpocX(EmotivBase):
    """Emotiv EPOC X implementation with LSL streaming."""
    
    READ_SIZE = 32

    def __init__(self) -> None:
        """Initialize the Emotiv EPOC X device."""
        super().__init__()
        self.delimiter = ','
        
        self.logger.info("Initializing Emotiv EPOC X...")
        
        try:
            crypto_key = self.get_crypto_key()
            self.cipher = AES.new(crypto_key, AES.MODE_ECB)
            self.logger.info("Encryption cipher initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize cipher: {e}")
            raise

    def get_hid_device(self) -> dict[str, Any]:
        """
        Find and return the Emotiv EPOC X HID device.
        
        Returns:
            Dictionary containing device information
            
        Raises:
            RuntimeError: If device is not found
        """
        self.logger.info(f"Searching for {DEVICE_MANUFACTURER} device...")
        
        devices = list(hid.enumerate())
        self.logger.debug(f"Found {len(devices)} HID devices")
        
        for device in devices:
            manufacturer = device.get('manufacturer_string', '')
            usage = device.get('usage', 0)
            product = device.get('product_string', 'Unknown')
            
            if manufacturer == DEVICE_MANUFACTURER and usage == 2:
                self.logger.info(
                    f"Found matching device: {product} "
                    f"(Serial: {device.get('serial_number', 'N/A')})"
                )
                return device

        error_msg = (
            f"{DEVICE_MANUFACTURER} EPOC X not found. "
            "Please ensure the device is connected and dongle is plugged in."
        )
        self.logger.error(error_msg)
        raise RuntimeError(error_msg)

    def get_crypto_key(self) -> bytearray:
        """
        Generate encryption key from device serial number.
        
        Returns:
            Encryption key as bytearray
            
        Raises:
            RuntimeError: If device is not found or serial number is invalid
        """
        try:
            device = self.get_hid_device()
            serial = device.get('serial_number', '')
            
            if not serial:
                raise ValueError("Device serial number is empty")
            
            self.logger.debug(f"Generating crypto key from serial number")
            
            # Convert serial number to bytearray
            sn = bytearray()
            for char in serial:
                sn += bytearray([ord(char)])
            
            if len(sn) < 4:
                raise ValueError(f"Serial number too short: {len(sn)} bytes")

            # Generate key using specific algorithm
            key = bytearray([
                sn[-1], sn[-2], sn[-4], sn[-4], sn[-2], sn[-1], sn[-2], sn[-4],
                sn[-1], sn[-4], sn[-3], sn[-2], sn[-1], sn[-2], sn[-2], sn[-3]
            ])
            
            return key
            
        except Exception as e:
            self.logger.error(f"Failed to generate crypto key: {e}")
            raise RuntimeError(f"Crypto key generation failed: {e}") from e

    def get_stream_info(self) -> StreamInfo:
        """
        Create LSL stream information for EPOC X.
        
        Returns:
            StreamInfo object configured for EPOC X
        """
        # EPOC X channel names in 10-20 system
        ch_names = [
            'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7',
            'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'
        ]
        n_channels = len(ch_names)

        self.logger.info(
            f"Creating LSL stream: {STREAM_NAME} "
            f"({n_channels} channels @ {SRATE}Hz)"
        )

        info = StreamInfo(STREAM_NAME, 'EEG', n_channels, SRATE, 'float32')
        
        # Add channel metadata
        chns = info.desc().append_child("channels")
        for label in ch_names:
            ch = chns.append_child("channel")
            ch.append_child_value("label", label)
            ch.append_child_value("unit", "microvolts")
            ch.append_child_value("type", "EEG")
            ch.append_child_value("scaling_factor", "1")

        # Add cap metadata
        cap = info.desc().append_child("cap")
        cap.append_child_value("name", "easycap-M1")
        cap.append_child_value("labelscheme", "10-20")

        return info

    def decode_data(self, data: bytes) -> list[float]:
        """
        Decode encrypted data from EPOC X device.
        
        Args:
            data: Raw encrypted data from device
            
        Returns:
            List of 14 channel values in microvolts
        """
        try:
            # XOR decryption step
            data = [el ^ 0x55 for el in data]
            
            # AES decryption
            data = self.cipher.decrypt(bytearray(data))

            # Extract channel values
            packet_data = ""
            for i in range(2, 16, 2):
                packet_data += str(self._convert_value(
                    str(data[i]), str(data[i+1]))) + self.delimiter

            for i in range(18, len(data), 2):
                packet_data += str(self._convert_value(
                    str(data[i]), str(data[i+1]))) + self.delimiter

            # Parse values
            packet_data = packet_data[:-len(self.delimiter)]
            packet_data = packet_data.split(self.delimiter)
            packet_data = [float(i) for i in packet_data]

            # Rearrange channels to match 10-20 system order
            # Original device order needs correction
            
            # Swap AF3 and F3
            packet_data[0], packet_data[2] = packet_data[2], packet_data[0]

            # Swap AF4 and F4
            packet_data[13], packet_data[11] = packet_data[11], packet_data[13]

            # Swap F7 and FC5
            packet_data[1], packet_data[3] = packet_data[3], packet_data[1]

            # Swap FC6 and F8
            packet_data[10], packet_data[12] = packet_data[12], packet_data[10]

            # Final order: ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
            return packet_data
            
        except Exception as e:
            self.logger.error(f"Error decoding data: {e}")
            raise

    def _convert_value(self, value_1: str, value_2: str) -> str:
        """
        Convert raw sensor values to microvolts.
        
        Args:
            value_1: First byte value as string
            value_2: Second byte value as string
            
        Returns:
            Converted value as formatted string
        """
        edk_value = "%.8f" % (
            ((int(value_1) * 0.128205128205129) + 4201.02564096001) + 
            ((int(value_2) - 128) * 32.82051289)
        )
        return edk_value

    def validate_data(self, data: bytes) -> bool:
        """
        Validate that data packet has correct size.
        
        Args:
            data: Raw data from device
            
        Returns:
            True if data size is valid
        """
        return len(data) == 32
