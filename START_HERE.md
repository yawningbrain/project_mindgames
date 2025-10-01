# 👋 START HERE - Emotiv LSL

**Welcome! This is your entry point to the Emotiv LSL project.**

---

## ✨ What is This?

A production-ready Python package for streaming **real-time EEG data** from your **Emotiv EPOC X headset** via Lab Streaming Layer (LSL), with:

- 🔴 **Live data streaming** at 256 Hz
- 💾 **JSON export** with full metadata
- 📊 **Automatic analysis** with 5 types of visualizations
- 🛠️ **Helper scripts** for easy management
- 📚 **4000+ lines of documentation**

---

## 🎯 What Do You Want To Do?

### 🆕 I'm New - Set Everything Up

**→ Read: [GETTING_STARTED.md](GETTING_STARTED.md)**

Complete step-by-step guide from zero to streaming data.

**Quick version:**
```bash
# 1. Setup (one-time, ~5 minutes)
./scripts/setup_env.sh

# 2. Configure headset (see GETTING_STARTED.md)

# 3. Start streaming!
./scripts/start_server.sh
```

---

### ⚡ I Just Want to Run It

**→ Read: [QUICKSTART.md](QUICKSTART.md)**

Minimal steps to get running in 5 minutes.

```bash
./scripts/start_server.sh                    # Terminal 1
python examples/export_to_json.py            # Terminal 2
python examples/analyze_json.py --latest     # Terminal 2
./scripts/stop_server.sh                     # Terminal 1
```

---

### 📖 I Want Complete Documentation

**→ Read: [README.md](README.md)**

Comprehensive 650+ line guide covering everything.

Also available:
- [REQUIREMENTS.md](REQUIREMENTS.md) - System & software requirements
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Visual project guide

---

### 🔧 I'm Having Problems

**→ Read: README.md [Troubleshooting Section](README.md#troubleshooting)**

Covers 15+ common issues including:
- Device not found
- Permission denied
- LSL library issues
- macOS-specific problems
- Server won't stop

**Quick fixes:**
```bash
# Device not found
→ Check dongle plugged in, headset on

# Permission denied (macOS)  
→ Use: ./scripts/start_server.sh (runs with sudo)

# Can't stop server
→ Use: ./scripts/stop_server.sh
```

---

### 👨‍💻 I Want to Contribute

**→ Read: [CONTRIBUTING.md](CONTRIBUTING.md)**

Development guidelines, coding standards, and contribution process.

```bash
# Setup for development
pip install -e ".[dev]"
```

---

## 📁 What's In This Project?

### Essential Files

```
emotiv-lsl-main/
├── 📚 Documentation/          # 9 comprehensive guides
├── 🔧 emotiv_lsl/            # Core package (5 modules)
├── 📝 examples/              # 5 usage examples
├── 🚀 scripts/               # 5 helper scripts
├── 📊 data/                  # Your recordings & plots
│   ├── json/                 # JSON recordings
│   ├── fif/                  # MNE format
│   └── plots/                # Visualizations
└── ⚙️ Configuration files
```

### Quick Command Reference

```bash
# Setup
./scripts/setup_env.sh              # One-time setup

# Server Management
./scripts/start_server.sh           # Start LSL server
./scripts/stop_server.sh            # Stop LSL server

# Data Operations
python examples/export_to_json.py   # Record data
python examples/analyze_json.py --latest  # Analyze

# Utilities
./scripts/cleanup_data.sh           # Clean up data files
python examples/read_data.py        # View real-time data
```

---

## ⚠️ Platform-Specific Notes

### macOS Users (IMPORTANT)

1. **Requires Homebrew** for LSL library:
   ```bash
   brew install labstreaminglayer/tap/lsl
   ```

2. **Requires sudo** to access USB devices:
   - Use `./scripts/start_server.sh` (handles this)
   - You'll be prompted for password

3. **Close Emotiv App** before starting server
   - Apps cannot run simultaneously

### Linux Users

- May need udev rules (see GETTING_STARTED.md)
- No sudo required (after udev rules)

### Windows Users

- No special requirements!
- No admin privileges needed

---

## 🎓 Learning Path

```
1. START HERE               (this file)
   ↓
2. GETTING_STARTED.md       (detailed setup)
   ↓
3. Try the Quick Reference  (in README)
   ↓
4. Record & Analyze Data    (examples/)
   ↓
5. Explore README.md        (deep dive)
   ↓
6. Customize for your needs (modify scripts)
```

---

## ✅ Success Looks Like

After setup, you should be able to:

1. ✅ Start server with one command
2. ✅ See device connection confirmed
3. ✅ Record data to JSON files
4. ✅ Generate analysis plots automatically
5. ✅ Stop server cleanly
6. ✅ Find all your data organized in `data/`

### Verification

```bash
# 1. Test imports
python -c "from emotiv_lsl import EmotivEpocX; print('✓ OK')"

# 2. Check scripts
./scripts/start_server.sh --help 2>&1 | head -5

# 3. Check data directories
ls -d data/*/
```

---

## 🆘 Getting Help

**In Order of Speed:**

1. **Check README Troubleshooting** - Most issues covered
2. **Review GETTING_STARTED.md** - Step-by-step guidance
3. **Check examples/** - Working code samples
4. **Open GitHub Issue** - For bugs or questions
5. **Read REQUIREMENTS.md** - For dependency issues

---

## 🎯 Next Steps

### Option A: Quick Test (5 min)
```bash
./scripts/start_server.sh
# (new terminal) python examples/read_data.py
```

### Option B: Full Workflow (10 min)
Follow [QUICKSTART.md](QUICKSTART.md)

### Option C: Deep Dive (30 min)
Read [GETTING_STARTED.md](GETTING_STARTED.md) then [README.md](README.md)

---

## 📊 Project Stats

- **Documentation:** 4,300+ lines across 10 files
- **Code:** 1,500+ lines with full type hints
- **Examples:** 5 working scripts
- **Helper Scripts:** 5 automation scripts
- **Supported Platforms:** macOS, Linux, Windows
- **Export Formats:** JSON, FIF, PNG, CSV-ready
- **Analysis Types:** 5 visualization + 11 statistics per channel

---

## 🎊 You're Ready!

Pick your path above and start exploring. The project is:
- ✅ Fully documented
- ✅ Well organized
- ✅ Production tested
- ✅ Easy to use

**Choose your next step from the options above!**

---

*Happy brain-hacking! 🧠✨*

**Last updated:** October 1, 2025

