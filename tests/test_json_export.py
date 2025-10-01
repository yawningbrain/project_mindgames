"""Tests for JSON export functionality."""

import pytest
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_json_file_structure():
    """Test that JSON files have the correct structure."""
    # Find most recent JSON file
    data_dir = Path(__file__).parent.parent / "data" / "json"
    
    if not data_dir.exists():
        pytest.skip("No data directory found")
    
    json_files = list(data_dir.glob("eeg_data_*.json"))
    
    if not json_files:
        pytest.skip("No JSON files found")
    
    # Test the most recent file
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    # Check top-level structure
    assert 'metadata' in data
    assert 'samples' in data
    
    # Check metadata
    metadata = data['metadata']
    assert 'device' in metadata
    assert 'channels' in metadata
    assert 'sample_rate_hz' in metadata
    assert 'duration_sec' in metadata
    
    # Check samples
    samples = data['samples']
    assert isinstance(samples, list)
    assert len(samples) > 0
    
    # Check first sample
    first_sample = samples[0]
    assert 'time_sec' in first_sample
    assert 'lsl_timestamp' in first_sample
    
    # Check that all channels are present
    for channel in metadata['channels']:
        assert channel in first_sample


def test_channel_count():
    """Test that the channel count matches expected value."""
    data_dir = Path(__file__).parent.parent / "data" / "json"
    
    if not data_dir.exists():
        pytest.skip("No data directory found")
    
    json_files = list(data_dir.glob("eeg_data_*.json"))
    
    if not json_files:
        pytest.skip("No JSON files found")
    
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    # EPOC X should have 14 channels
    assert data['metadata']['channel_count'] == 14
    assert len(data['metadata']['channels']) == 14

