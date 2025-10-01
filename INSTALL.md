# Installation - 60 Seconds

## For Everyone (macOS, Linux, Windows)

```bash
# 1. Clone
git clone https://github.com/yawningbrain/project_mindgames.git
cd project_mindgames

# 2. Setup (one command)
./QUICK_START.sh
```

**That's it!** ✓

---

## What You Can Run

### Option 1: LSL Server (for data streaming)
```bash
./scripts/start_server.sh
```

### Option 2: Streamlit App (for GUI)
```bash
./run_app.sh
```

### Option 3: Record Data
```bash
source venv/bin/activate
python examples/export_to_json.py
```

---

## Requirements

- **Python 3.9+**
- **Emotiv EPOC X** headset with USB dongle
- **macOS users**: `brew install labstreaminglayer/tap/lsl`

---

## Troubleshooting

**"Permission denied"?**
```bash
chmod +x QUICK_START.sh
```

**"Python not found"?**
- Install Python from https://python.org

**Need more help?**
- See [README.md](README.md) for full documentation

---

**That's all you need to know to get started!** 🚀
