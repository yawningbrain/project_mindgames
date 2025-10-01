"""
Emotiv LSL Streamlit Application
==================================
A modern web interface for controlling the Emotiv EPOC X LSL server
and recording EEG data.
"""

import streamlit as st
import subprocess
import time
import json
import os
import signal
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure page
st.set_page_config(
    page_title="Emotiv LSL Controller",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data" / "json"
VENV_PYTHON = PROJECT_ROOT / "venv" / "bin" / "python"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Initialize session state
if 'server_process' not in st.session_state:
    st.session_state.server_process = None
if 'server_running' not in st.session_state:
    st.session_state.server_running = False
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'last_recording' not in st.session_state:
    st.session_state.last_recording = None


def check_server_running():
    """Check if the server process is running."""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'python main.py'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False


def start_server():
    """Start the LSL server."""
    try:
        # Stop any conflicting Emotiv services
        subprocess.run(
            ['sudo', 'killall', '-9', 'CortexService', 'CortexSync'],
            capture_output=True,
            stderr=subprocess.DEVNULL
        )
        
        # Start server in background
        env = os.environ.copy()
        env['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
        
        process = subprocess.Popen(
            ['sudo', '-n', str(VENV_PYTHON), 'main.py'],
            cwd=str(PROJECT_ROOT),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment to check if it started
        time.sleep(2)
        
        if process.poll() is None:
            st.session_state.server_process = process
            st.session_state.server_running = True
            return True, "Server started successfully!"
        else:
            _, stderr = process.communicate()
            return False, f"Server failed to start: {stderr}"
            
    except Exception as e:
        return False, f"Error starting server: {str(e)}"


def stop_server():
    """Stop the LSL server."""
    try:
        # Kill the process
        subprocess.run(
            ['sudo', '-n', 'pkill', '-f', 'python main.py'],
            capture_output=True
        )
        
        time.sleep(1)
        
        if st.session_state.server_process:
            try:
                st.session_state.server_process.terminate()
                st.session_state.server_process.wait(timeout=3)
            except:
                pass
        
        st.session_state.server_process = None
        st.session_state.server_running = False
        
        return True, "Server stopped successfully!"
        
    except Exception as e:
        return False, f"Error stopping server: {str(e)}"


def record_data(duration_sec=5):
    """Record EEG data to JSON."""
    try:
        env = os.environ.copy()
        env['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
        
        # Modify the export script temporarily to use specified duration
        result = subprocess.run(
            [str(VENV_PYTHON), 'examples/export_to_json.py'],
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=duration_sec + 30
        )
        
        if result.returncode == 0:
            # Find the most recent JSON file
            json_files = list(DATA_DIR.glob("eeg_data_*.json"))
            if json_files:
                latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                st.session_state.last_recording = str(latest_file)
                return True, f"Recording saved: {latest_file.name}"
            else:
                return False, "Recording completed but file not found"
        else:
            return False, f"Recording failed: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return False, "Recording timed out"
    except Exception as e:
        return False, f"Error recording data: {str(e)}"


def load_json_data(filepath):
    """Load JSON recording data."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def plot_eeg_channels(data):
    """Create an interactive plot of EEG channels."""
    samples = data['samples']
    metadata = data['metadata']
    channels = metadata['channels']
    
    # Extract data
    times = [s['time_sec'] for s in samples]
    
    # Create subplots
    fig = make_subplots(
        rows=len(channels),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=channels
    )
    
    # Add traces for each channel
    for idx, channel in enumerate(channels, 1):
        values = [s[channel] for s in samples]
        
        fig.add_trace(
            go.Scatter(
                x=times,
                y=values,
                mode='lines',
                name=channel,
                line=dict(width=1)
            ),
            row=idx,
            col=1
        )
    
    # Update layout
    fig.update_layout(
        height=200 * len(channels),
        showlegend=False,
        title_text="EEG Channel Data",
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Time (seconds)", row=len(channels), col=1)
    
    return fig


# ============================================================================
# Main UI
# ============================================================================

# Header
st.title("🧠 Emotiv LSL Controller")
st.markdown("Control your Emotiv EPOC X EEG headset and record data")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Check actual server status
    actual_status = check_server_running()
    if actual_status != st.session_state.server_running:
        st.session_state.server_running = actual_status
    
    # Server status
    if st.session_state.server_running:
        st.success("🟢 Server Running")
    else:
        st.error("🔴 Server Stopped")
    
    st.divider()
    
    # Server controls
    st.subheader("Server Control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Start", disabled=st.session_state.server_running, use_container_width=True):
            with st.spinner("Starting server..."):
                success, message = start_server()
                if success:
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)
    
    with col2:
        if st.button("⏹️ Stop", disabled=not st.session_state.server_running, use_container_width=True):
            with st.spinner("Stopping server..."):
                success, message = stop_server()
                if success:
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)
    
    st.divider()
    
    # Recording settings
    st.subheader("Recording Settings")
    duration = st.slider("Duration (seconds)", min_value=1, max_value=60, value=5)
    
    st.divider()
    
    # System info
    st.subheader("📊 System Info")
    st.caption(f"Data Directory: `data/json/`")
    json_files = list(DATA_DIR.glob("eeg_data_*.json"))
    st.caption(f"Recordings: {len(json_files)}")

# Main content area
tab1, tab2, tab3 = st.tabs(["📹 Record", "📈 View Data", "ℹ️ About"])

# ============================================================================
# Tab 1: Record
# ============================================================================
with tab1:
    st.header("Record EEG Data")
    
    if not st.session_state.server_running:
        st.warning("⚠️ Server is not running. Please start the server first.")
    else:
        st.info(f"Ready to record {duration} seconds of EEG data")
        
        if st.button("🔴 Start Recording", use_container_width=True, type="primary", disabled=not st.session_state.server_running):
            with st.spinner(f"Recording {duration} seconds..."):
                success, message = record_data(duration)
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)
        
        # Show recent recordings
        st.subheader("Recent Recordings")
        json_files = sorted(
            DATA_DIR.glob("eeg_data_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:10]
        
        if json_files:
            for filepath in json_files:
                stat = filepath.stat()
                size_mb = stat.st_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(stat.st_mtime)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.text(filepath.name)
                with col2:
                    st.text(f"{size_mb:.2f} MB")
                with col3:
                    st.text(mod_time.strftime("%H:%M:%S"))
        else:
            st.info("No recordings yet")

# ============================================================================
# Tab 2: View Data
# ============================================================================
with tab2:
    st.header("View Recorded Data")
    
    # File selector
    json_files = sorted(
        DATA_DIR.glob("eeg_data_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if json_files:
        # Select file
        selected_file = st.selectbox(
            "Select Recording",
            options=json_files,
            format_func=lambda p: f"{p.name} ({datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')})"
        )
        
        if selected_file:
            # Load and display data
            data = load_json_data(selected_file)
            
            if data:
                metadata = data['metadata']
                
                # Display metadata
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Duration", f"{metadata['duration_sec']:.1f}s")
                with col2:
                    st.metric("Samples", metadata['num_samples'])
                with col3:
                    st.metric("Sample Rate", f"{metadata['sample_rate_hz']} Hz")
                with col4:
                    st.metric("Channels", metadata['channel_count'])
                
                # Plot data
                st.subheader("Channel Data")
                with st.spinner("Generating plot..."):
                    fig = plot_eeg_channels(data)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Show sample data
                with st.expander("View Sample Data"):
                    samples_df = pd.DataFrame(data['samples'][:100])  # First 100 samples
                    st.dataframe(samples_df, use_container_width=True)
                
                # Download button
                st.download_button(
                    label="📥 Download JSON",
                    data=json.dumps(data, indent=2),
                    file_name=selected_file.name,
                    mime="application/json"
                )
    else:
        st.info("No recordings available. Record some data first!")

# ============================================================================
# Tab 3: About
# ============================================================================
with tab3:
    st.header("About Emotiv LSL")
    
    st.markdown("""
    ### 🧠 Emotiv EPOC X LSL Controller
    
    This application provides a user-friendly interface for:
    - **Starting/Stopping** the LSL server
    - **Recording** EEG data from your Emotiv EPOC X headset
    - **Viewing** and analyzing recorded data
    - **Exporting** data in JSON format
    
    ### 📋 Quick Start
    
    1. **Start the Server**: Click the "▶️ Start" button in the sidebar
    2. **Record Data**: Go to the "Record" tab and click "Start Recording"
    3. **View Results**: Switch to the "View Data" tab to see your recordings
    
    ### 🔧 Technical Details
    
    - **Device**: Emotiv EPOC X (14 channels)
    - **Protocol**: Lab Streaming Layer (LSL)
    - **Sample Rate**: 256 Hz
    - **Data Format**: JSON with full metadata
    
    ### 📂 File Locations
    
    - **Recordings**: `data/json/eeg_data_*.json`
    - **Plots**: `data/plots/*.png`
    
    ### ⚠️ Important Notes
    
    - Make sure the Emotiv USB dongle is plugged in
    - Ensure the headset is turned on and connected
    - Close the Emotiv App before starting the server
    - On macOS, sudo access is required (passwordless sudo recommended)
    
    ### 🛠️ Setup Passwordless Sudo (Optional)
    
    To avoid entering your password every time:
    
    ```bash
    sudo visudo
    # Add this line (replace USERNAME with your username):
    USERNAME ALL=(ALL) NOPASSWD: ALL
    ```
    
    **⚠️ Security Warning**: Only do this on a personal machine you trust.
    """)
    
    st.divider()
    
    st.caption("Made with ❤️ for the neuroscience community")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🧠 Emotiv LSL v1.0")
with col2:
    st.caption(f"📁 Data: {len(list(DATA_DIR.glob('*.json')))} files")
with col3:
    st.caption(f"⏰ {datetime.now().strftime('%H:%M:%S')}")

