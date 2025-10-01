#!/usr/bin/env python3
"""
Example script to read and analyze JSON exported EEG data.

This demonstrates how to load and work with JSON-formatted EEG data
exported from the Emotiv EPOC X.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_json_data(filename: str) -> Dict[str, Any]:
    """
    Load JSON EEG data file.
    
    Args:
        filename: Path to JSON file
        
    Returns:
        Dictionary with metadata and samples
    """
    print(f"📂 Loading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✓ Loaded successfully!\n")
    return data


def print_metadata(data: Dict[str, Any]):
    """Print recording metadata."""
    metadata = data['metadata']
    
    print("=" * 60)
    print("METADATA")
    print("=" * 60)
    print(f"Device:           {metadata['device']}")
    print(f"Recording ID:     {metadata['recording_id']}")
    print(f"Start Time:       {metadata['start_time_iso']}")
    print(f"Duration:         {metadata['duration_sec']} seconds")
    print(f"Sample Rate:      {metadata['sample_rate_hz']} Hz")
    print(f"Samples:          {metadata['num_samples']}")
    print(f"Channels:         {metadata['channel_count']}")
    print(f"Units:            {metadata['units']}")
    print(f"Channels:         {', '.join(metadata['channels'])}")
    print()


def analyze_samples(data: Dict[str, Any]):
    """Analyze and print sample statistics."""
    samples = data['samples']
    channels = data['metadata']['channels']
    
    print("=" * 60)
    print("DATA ANALYSIS")
    print("=" * 60)
    
    # First sample
    print("\n📍 First Sample:")
    first = samples[0]
    print(f"  Time: {first['time_sec']} sec")
    print(f"  LSL Timestamp: {first['lsl_timestamp']}")
    for ch in channels[:3]:  # Show first 3 channels
        print(f"  {ch}: {first[ch]}")
    print("  ...")
    
    # Last sample
    print("\n📍 Last Sample:")
    last = samples[-1]
    print(f"  Time: {last['time_sec']} sec")
    print(f"  LSL Timestamp: {last['lsl_timestamp']}")
    for ch in channels[:3]:
        print(f"  {ch}: {last[ch]}")
    print("  ...")
    
    # Channel statistics
    print("\n📊 Channel Statistics:")
    print(f"{'Channel':<8} {'Min':>12} {'Max':>12} {'Mean':>12} {'Std':>12}")
    print("-" * 60)
    
    for ch in channels:
        values = [s[ch] for s in samples]
        ch_min = min(values)
        ch_max = max(values)
        ch_mean = sum(values) / len(values)
        ch_std = (sum((x - ch_mean) ** 2 for x in values) / len(values)) ** 0.5
        
        print(f"{ch:<8} {ch_min:>12.2f} {ch_max:>12.2f} {ch_mean:>12.2f} {ch_std:>12.2f}")
    
    print()


def extract_channel_data(data: Dict[str, Any], channel_name: str) -> List[float]:
    """
    Extract all values for a specific channel.
    
    Args:
        data: JSON data dictionary
        channel_name: Name of channel to extract
        
    Returns:
        List of values for that channel
    """
    samples = data['samples']
    return [s[channel_name] for s in samples]


def extract_timestamps(data: Dict[str, Any], relative: bool = True) -> List[float]:
    """
    Extract timestamps.
    
    Args:
        data: JSON data dictionary
        relative: If True, return relative times; if False, return LSL timestamps
        
    Returns:
        List of timestamps
    """
    samples = data['samples']
    key = 'time_sec' if relative else 'lsl_timestamp'
    return [s[key] for s in samples]


def convert_to_numpy_array(data: Dict[str, Any]):
    """
    Convert to numpy array (if numpy is available).
    
    Returns:
        2D numpy array (samples x channels)
    """
    try:
        import numpy as np
    except ImportError:
        print("⚠️  NumPy not installed. Cannot convert to array.")
        return None
    
    samples = data['samples']
    channels = data['metadata']['channels']
    
    # Build 2D array
    array = np.zeros((len(samples), len(channels)))
    
    for i, sample in enumerate(samples):
        for j, ch in enumerate(channels):
            array[i, j] = sample[ch]
    
    return array


def example_usage():
    """Show example usage patterns."""
    print("=" * 60)
    print("EXAMPLE USAGE")
    print("=" * 60)
    
    print("""
# Load JSON file
import json
with open('eeg_data.json', 'r') as f:
    data = json.load(f)

# Access metadata
metadata = data['metadata']
channels = metadata['channels']
sample_rate = metadata['sample_rate_hz']

# Access samples
samples = data['samples']
first_sample = samples[0]

# Get specific channel data for all samples
af3_values = [s['AF3'] for s in samples]

# Get timestamps
timestamps = [s['time_sec'] for s in samples]

# Iterate through samples
for sample in samples:
    time = sample['time_sec']
    af3 = sample['AF3']
    f7 = sample['F7']
    print(f"Time: {time}, AF3: {af3}, F7: {f7}")

# Convert to numpy for analysis (if numpy installed)
import numpy as np
channels = metadata['channels']
array = np.array([[s[ch] for ch in channels] for s in samples])
# array shape: (num_samples, num_channels)
""")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python read_json.py <json_file>")
        print("\nExample:")
        print("  python read_json.py eeg_data_20251001_000258.json")
        print()
        example_usage()
        return
    
    filename = sys.argv[1]
    
    if not Path(filename).exists():
        print(f"❌ File not found: {filename}")
        return
    
    # Load data
    data = load_json_data(filename)
    
    # Print metadata
    print_metadata(data)
    
    # Analyze samples
    analyze_samples(data)
    
    # Try numpy conversion
    print("=" * 60)
    print("NUMPY CONVERSION")
    print("=" * 60)
    array = convert_to_numpy_array(data)
    if array is not None:
        print(f"✓ Converted to NumPy array")
        print(f"  Shape: {array.shape} (samples x channels)")
        print(f"  Dtype: {array.dtype}")
        print(f"  Size: {array.nbytes / 1024:.2f} KB in memory")
    print()
    
    # Show usage examples
    example_usage()


if __name__ == '__main__':
    main()

