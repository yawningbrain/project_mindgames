from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from mne import Info, create_info
from mne.io.array import RawArray
from pylsl import StreamInlet, resolve_byprop

from config import SRATE


def get_info() -> Info:
    ch_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7',
                'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

    info = create_info(
        sfreq=SRATE,
        ch_names=ch_names,
        ch_types=['eeg'] * len(ch_names)
    )

    return info


def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG', timeout=5.0)

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    buffer = []
    while True:
        if len(buffer) == 128 * 5:  # wait 5 seconds
            break

        sample, _ = inlet.pull_sample()
        sample = [el / 1000000 for el in sample]  # convert to microvolts

        buffer.append(sample)

    info = get_info()
    raw = RawArray(np.array(buffer).T, info)

    # Save to data/fif directory
    data_dir = Path(__file__).parent.parent / "data" / "fif"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    filename = str(data_dir / "data_{}_raw.fif".format(datetime.now().strftime("%Y%m%d_%H%M%S")))
    raw.save(filename)
    print(f"Data saved to {filename}")


if __name__ == '__main__':
    main()
