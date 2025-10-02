# Emotiv LSL

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Stream EEG data from Emotiv EPOC X via Lab Streaming Layer**

Clean, simple, and ready to use in 60 seconds.

---

## Quick Start

```bash
git clone https://github.com/yawningbrain/project_mindgames.git
cd project_mindgames
./QUICK_START.sh
```

That's it! ✓

---

## Usage

### Run LSL Server
```bash
./scripts/start_server.sh
```

### Run Streamlit App
```bash
./run_app.sh
```

### Record Data
```bash
source venv/bin/activate
python examples/export_to_json.py
```

---

## Requirements

- **Python 3.9+**
- **Emotiv EPOC X** headset with USB dongle
- **macOS**: `brew install labstreaminglayer/tap/lsl`

---

## Documentation

- **[INSTALL.md](INSTALL.md)** - Installation guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[SECURITY.md](SECURITY.md)** - Security policy
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[docs/](docs/)** - Detailed technical docs

**New to the project?** See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

---

## Features

✓ Real-time EEG streaming via LSL  
✓ 14-channel support (EPOC X)  
✓ JSON export with metadata  
✓ Data analysis and visualization  
✓ Streamlit web interface  
✓ One-command setup  

---

## Project Structure

```
emotiv-lsl/
├── emotiv_lsl/          # Core package
├── examples/            # Usage examples
├── scripts/             # Helper scripts
├── data/               # Data storage
└── docs/               # Documentation
```

---

## Troubleshooting

**Device not found?**
- Plug in USB dongle
- Turn on headset
- Close Emotiv App

**Permission denied? (macOS)**
- Run with: `sudo ./scripts/start_server.sh`

**More help?** See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Credits

Original code adapted from [CyKit](https://github.com/CymatiCorp/CyKit)

**Made for the neuroscience community** 🧠
