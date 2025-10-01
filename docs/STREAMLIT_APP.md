# 🧠 Emotiv LSL Streamlit Application

A modern, user-friendly web interface for controlling your Emotiv EPOC X EEG headset and recording data.

## ✨ Features

- 🎮 **Easy Server Control** - Start/stop the LSL server with one click
- 📹 **Simple Recording** - Record EEG data with customizable duration
- 📊 **Real-time Visualization** - View your recorded data with interactive plots
- 💾 **Data Management** - Browse, view, and download recordings
- 🎨 **Modern UI** - Clean, intuitive interface built with Streamlit

## 🚀 Quick Start

### Prerequisites

1. **Emotiv EPOC X headset** with USB dongle
2. **Python 3.9+** installed
3. **Virtual environment** set up (see main README.md)

### Launch the App

```bash
./run_app.sh
```

The application will automatically open in your browser at `http://localhost:8501`

### Alternative Launch

```bash
# Activate virtual environment
source venv/bin/activate

# Set library path (macOS only)
export DYLD_LIBRARY_PATH=/opt/homebrew/lib

# Run Streamlit
streamlit run streamlit_app.py
```

## 📖 Using the Application

### 1. Start the Server

- Click the **▶️ Start** button in the sidebar
- Wait for the status to show **🟢 Server Running**
- You may need to enter your password (macOS sudo requirement)

### 2. Record Data

- Go to the **📹 Record** tab
- Adjust the recording duration with the slider (1-60 seconds)
- Click **🔴 Start Recording**
- Wait for the recording to complete
- See your new recording appear in the list

### 3. View Your Data

- Switch to the **📈 View Data** tab
- Select a recording from the dropdown
- View metadata (duration, sample count, etc.)
- Explore the interactive channel plots
- Download the JSON file if needed

### 4. Stop the Server

- Click the **⏹️ Stop** button in the sidebar when done
- This saves battery on your headset

## 🎯 Use Cases

### Research & Data Collection

```
1. Start server
2. Record baseline (eyes closed, 60 seconds)
3. Record task data (eyes open, various durations)
4. Stop server
5. Export data for analysis
```

### Real-time Monitoring

```
1. Start server
2. Record short sessions (5-10 seconds)
3. Immediately view data in interactive plots
4. Iterate and adjust experimental protocol
```

### Teaching & Demos

```
1. Launch Streamlit app for audience
2. Show live recording process
3. Display EEG channels in real-time
4. Discuss signal quality and artifacts
```

## 🔧 Configuration

### Recording Duration

Adjust in the sidebar (1-60 seconds). Longer recordings create larger files:

| Duration | File Size | Use Case |
|----------|-----------|----------|
| 5 sec | ~0.5 MB | Quick tests |
| 30 sec | ~3 MB | Short experiments |
| 60 sec | ~6 MB | Full data collection |

### Port Configuration

Default: `http://localhost:8501`

To change:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 🐛 Troubleshooting

### App Won't Start

```bash
# Install Streamlit dependencies
pip install streamlit plotly pandas

# Try launching again
./run_app.sh
```

### Server Won't Start

**Error: "Permission denied"**
- macOS requires sudo for HID device access
- This is normal and expected

**Error: "Device not found"**
- Check USB dongle is plugged in
- Ensure headset is turned on
- Close Emotiv App if running

### Recording Fails

**Error: "No EEG stream found"**
- Make sure server is running (green status in sidebar)
- Check server terminal for errors
- Try stopping and restarting the server

### Plots Not Showing

- Ensure you have `plotly` installed: `pip install plotly`
- Try refreshing the browser
- Check browser console for JavaScript errors

## 🔒 Security & Permissions

### Sudo Requirements (macOS)

The app requires sudo to access the USB HID device. Two options:

**Option 1: Enter password each time** (recommended for shared machines)
- You'll be prompted when starting the server

**Option 2: Passwordless sudo** (convenient for personal machines)
```bash
sudo visudo
# Add: YOUR_USERNAME ALL=(ALL) NOPASSWD: ALL
```
⚠️ **Security Warning**: Only use passwordless sudo on trusted personal machines

### Network Access

- App runs locally only (localhost)
- No external network connections required
- Data stays on your machine

## 📊 Data Files

### Location

All recordings are saved to:
```
data/json/eeg_data_YYYYMMDD_HHMMSS.json
```

### Format

Each file contains:
- **Metadata**: Device info, channels, sample rate, duration
- **Samples**: Array of timestamped channel values
- **Full timestamps**: Both relative and absolute LSL timestamps

### Loading Data

```python
import json

with open('data/json/eeg_data_20251001_120000.json', 'r') as f:
    data = json.load(f)

# Access metadata
metadata = data['metadata']
print(f"Duration: {metadata['duration_sec']} seconds")

# Access samples
samples = data['samples']
first_sample = samples[0]
print(f"AF3 value: {first_sample['AF3']}")
```

## 🎨 Customization

### Modify Recording Duration Range

Edit `streamlit_app.py`:
```python
# Line ~170
duration = st.slider("Duration (seconds)", 
                     min_value=1, 
                     max_value=120,  # Change max
                     value=10)        # Change default
```

### Add Custom Visualizations

```python
# Add after line ~220 in plot_eeg_channels()
def plot_custom_view(data):
    # Your custom plotting code
    return fig
```

### Change Theme

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"
```

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Deploy from `streamlit-app` branch
5. Select `streamlit_app.py` as main file

**Note**: The Streamlit Cloud deployment won't have access to hardware, so it's mainly for demonstration of the UI.

### Run on Remote Server

```bash
# SSH into server
ssh user@server

# Clone and setup
git clone https://github.com/yourusername/emotiv-lsl.git
cd emotiv-lsl
./scripts/setup_env.sh

# Run with external access
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

Access from other devices: `http://SERVER_IP:8501`

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Graph Reference](https://plotly.com/python/)
- [Main Project README](README.md)
- [GitHub Setup Guide](GITHUB_SETUP.md)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

---

**Made with ❤️ for the neuroscience community**

