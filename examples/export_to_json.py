#!/usr/bin/env python3
"""
Export Emotiv EPOC X EEG data to JSON format.

This script records EEG data from the LSL stream and exports it in a 
sample-by-sample JSON format with full metadata and timestamps.
"""

import json
import sys
import uuid
import signal
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pylsl import StreamInlet, resolve_byprop

from config import SRATE

# Global flag for interrupt handling
_interrupted = False


def signal_handler(sig, frame):
    """Handle interrupt signal."""
    global _interrupted
    _interrupted = True


# Register signal handler
signal.signal(signal.SIGINT, signal_handler)


def estimate_file_size(duration_sec: int, num_channels: int, sample_rate: int) -> tuple:
    """
    Estimate JSON file size.
    
    Args:
        duration_sec: Recording duration in seconds
        num_channels: Number of EEG channels
        sample_rate: Sampling rate in Hz
        
    Returns:
        Tuple of (size_bytes, size_mb)
    """
    num_samples = duration_sec * sample_rate
    # Rough estimate: ~200 bytes per sample object in JSON
    bytes_per_sample = 200 + (num_channels * 15)  # 15 bytes per channel value
    total_bytes = num_samples * bytes_per_sample + 1000  # +1000 for metadata
    return total_bytes, total_bytes / (1024 * 1024)


def collect_samples(inlet: StreamInlet, duration_sec: int, sample_rate: int) -> tuple:
    """
    Collect EEG samples from LSL stream.
    
    Args:
        inlet: LSL StreamInlet object
        duration_sec: Duration to record in seconds
        sample_rate: Expected sample rate
        
    Returns:
        Tuple of (samples_list, start_lsl_timestamp, channel_names)
    """
    global _interrupted
    
    num_samples_expected = duration_sec * sample_rate
    samples = []
    start_lsl_time = None
    
    print(f"\n📊 Recording {duration_sec} seconds ({num_samples_expected} samples)...")
    print("Press Ctrl+C to stop early\n")
    
    # Get stream info to extract channel names
    stream_info = inlet.info()
    ch_count = stream_info.channel_count()
    
    # Extract channel names from stream metadata
    ch_names = []
    ch = stream_info.desc().child("channels").child("channel")
    for _ in range(ch_count):
        ch_names.append(ch.child_value("label"))
        ch = ch.next_sibling()
    
    # If no metadata, use default channel names
    if not ch_names:
        ch_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 
                   'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
    
    print(f"✓ Channels: {', '.join(ch_names)}\n")
    
    progress_interval = max(1, num_samples_expected // 20)  # Update every 5%
    
    for i in range(num_samples_expected):
        # Check for interrupt
        if _interrupted:
            print(f"\n\n⚠️  Recording interrupted by user")
            print(f"✓ Collected {len(samples)} samples before interruption\n")
            break
        
        # Pull sample with timeout
        sample, timestamp = inlet.pull_sample(timeout=1.0)
        
        if sample is None:
            print(f"\n⚠️  Timeout waiting for sample {i+1}")
            continue
        
        if start_lsl_time is None:
            start_lsl_time = timestamp
            print(f"🎬 Recording started at LSL time: {timestamp:.6f}\n")
        
        samples.append((sample, timestamp))
        
        # Progress indicator
        if (i + 1) % progress_interval == 0:
            progress = ((i + 1) / num_samples_expected) * 100
            elapsed = timestamp - start_lsl_time if start_lsl_time else 0
            print(f"Progress: {progress:.0f}% ({i + 1}/{num_samples_expected} samples, {elapsed:.1f}s)", end='\r')
    
    if not _interrupted and len(samples) == num_samples_expected:
        print(f"\n✓ Recording complete! Collected {len(samples)} samples\n")
    
    return samples, start_lsl_time, ch_names


def create_json_structure(
    samples: List[tuple],
    start_lsl_time: float,
    ch_names: List[str],
    sample_rate: int,
    apply_conversion: bool = False
) -> Dict[str, Any]:
    """
    Create JSON structure from collected samples.
    
    Args:
        samples: List of (sample_data, timestamp) tuples
        start_lsl_time: First LSL timestamp
        ch_names: Channel names
        sample_rate: Sampling rate
        apply_conversion: If True, convert to microvolts (divide by 1e6)
        
    Returns:
        Dictionary ready for JSON serialization
    """
    print("📝 Building JSON structure...")
    
    # Calculate metadata
    duration_sec = len(samples) / sample_rate
    start_datetime = datetime.now(timezone.utc)
    recording_id = str(uuid.uuid4())
    
    # Create metadata
    metadata = {
        "device": "Emotiv EPOC X",
        "recording_id": recording_id,
        "start_time_iso": start_datetime.isoformat(),
        "start_time_lsl": round(start_lsl_time, 6),
        "channels": ch_names,
        "channel_count": len(ch_names),
        "sample_rate_hz": sample_rate,
        "num_samples": len(samples),
        "duration_sec": round(duration_sec, 3),
        "units": "microvolts" if apply_conversion else "emotiv_raw",
        "conversion_factor": 1e-6 if apply_conversion else 1.0,
        "note": "time_sec is relative to start of recording, lsl_timestamp is absolute"
    }
    
    # Build sample array
    sample_objects = []
    conversion = 1e-6 if apply_conversion else 1.0
    
    for i, (sample_data, lsl_timestamp) in enumerate(samples):
        # Calculate relative time from start
        relative_time = (lsl_timestamp - start_lsl_time)
        
        # Create sample object
        sample_obj = {
            "time_sec": round(relative_time, 3),
            "lsl_timestamp": round(lsl_timestamp, 6)
        }
        
        # Add channel data with reasonable precision
        for ch_name, value in zip(ch_names, sample_data):
            sample_obj[ch_name] = round(value * conversion, 6)
        
        sample_objects.append(sample_obj)
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(samples)} samples...", end='\r')
    
    print(f"✓ Processed all {len(samples)} samples          \n")
    
    # Combine into final structure
    json_data = {
        "metadata": metadata,
        "samples": sample_objects
    }
    
    return json_data


def save_json(data: Dict[str, Any], filename: str, pretty: bool = True):
    """
    Save data to JSON file.
    
    Args:
        data: Dictionary to save
        filename: Output filename
        pretty: If True, use indentation for readability
    """
    print(f"💾 Writing to {filename}...")
    
    indent = 2 if pretty else None
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        # Get actual file size
        file_size = Path(filename).stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✓ Successfully saved!")
        print(f"  File: {filename}")
        print(f"  Size: {file_size_mb:.2f} MB ({file_size:,} bytes)")
        print(f"  Samples: {len(data['samples'])}")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        raise


def validate_json(filename: str) -> bool:
    """
    Validate that the JSON file can be loaded.
    
    Args:
        filename: Path to JSON file
        
    Returns:
        True if valid, False otherwise
    """
    print(f"\n🔍 Validating JSON file...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check structure
        assert "metadata" in data, "Missing metadata"
        assert "samples" in data, "Missing samples"
        assert len(data["samples"]) > 0, "No samples in file"
        assert "channels" in data["metadata"], "Missing channel names"
        
        print(f"✓ JSON file is valid!")
        print(f"  Metadata keys: {list(data['metadata'].keys())}")
        print(f"  Sample count: {len(data['samples'])}")
        print(f"  First sample keys: {list(data['samples'][0].keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 70)
    print("  Emotiv EPOC X → JSON Exporter")
    print("=" * 70)
    
    # Configuration
    DURATION_SEC = 5  # Default: 5 seconds
    APPLY_CONVERSION = False  # Keep raw values by default
    PRETTY_PRINT = True  # Readable JSON
    
    # Estimate file size
    est_bytes, est_mb = estimate_file_size(DURATION_SEC, 14, SRATE)
    
    print(f"\n⚙️  Configuration:")
    print(f"  Duration: {DURATION_SEC} seconds")
    print(f"  Sample Rate: {SRATE} Hz")
    print(f"  Expected Samples: {DURATION_SEC * SRATE}")
    print(f"  Estimated File Size: ~{est_mb:.2f} MB")
    print(f"  Units: {'microvolts' if APPLY_CONVERSION else 'emotiv_raw'}")
    
    if est_mb > 10:
        print(f"\n⚠️  WARNING: Large file size estimated (> 10 MB)")
        try:
            response = input("  Continue? (y/N): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        except KeyboardInterrupt:
            print("\nCancelled.")
            return
    
    # Find LSL stream
    print(f"\n🔍 Looking for EEG stream (timeout: 5 seconds)...")
    try:
        streams = resolve_byprop('type', 'EEG', timeout=5.0)
        if not streams:
            print("❌ No EEG stream found!")
            print("   Make sure the LSL server is running.")
            return
        
        print(f"✓ Found stream: {streams[0].name()}")
        
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        return
    except Exception as e:
        print(f"❌ Error finding stream: {e}")
        return
    
    # Create inlet
    print("📡 Creating stream inlet...")
    inlet = StreamInlet(streams[0])
    print("✓ Inlet created")
    
    # Collect samples
    try:
        samples, start_lsl_time, ch_names = collect_samples(inlet, DURATION_SEC, SRATE)
        
        if not samples:
            print("❌ No samples collected!")
            return
        
        # Create JSON structure
        json_data = create_json_structure(
            samples, 
            start_lsl_time, 
            ch_names, 
            SRATE,
            apply_conversion=APPLY_CONVERSION
        )
        
        # Generate filename and ensure data directory exists
        data_dir = Path(__file__).parent.parent / "data" / "json"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = str(data_dir / f"eeg_data_{timestamp_str}.json")
        
        # Save to file
        save_json(json_data, filename, pretty=PRETTY_PRINT)
        
        # Validate
        validate_json(filename)
        
        print("\n" + "=" * 70)
        print("✨ Export complete!")
        print("=" * 70)
        print(f"\nTo load this data in Python:")
        print(f"  import json")
        print(f"  with open('{filename}', 'r') as f:")
        print(f"      data = json.load(f)")
        print(f"  samples = data['samples']")
        print(f"  metadata = data['metadata']")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Export cancelled by user")
        print("✓ No files were saved")
        return


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

