#!/usr/bin/env python3
"""
Comprehensive analysis and visualization of JSON-exported EEG data.

This script performs multiple analyses on EEG data and generates
publication-quality visualizations.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy import signal, stats

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class EEGAnalyzer:
    """Comprehensive EEG data analyzer."""
    
    def __init__(self, json_file: str):
        """
        Initialize analyzer with JSON data file.
        
        Args:
            json_file: Path to JSON EEG data file
        """
        self.json_file = Path(json_file)
        self.data = None
        self.metadata = None
        self.samples = None
        self.channel_names = None
        self.sample_rate = None
        self.data_array = None
        self.timestamps = None
        
        self._load_data()
        self._prepare_arrays()
    
    def _load_data(self):
        """Load JSON data file."""
        print(f"📂 Loading {self.json_file.name}...")
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.metadata = self.data['metadata']
        self.samples = self.data['samples']
        self.channel_names = self.metadata['channels']
        self.sample_rate = self.metadata['sample_rate_hz']
        
        print(f"✓ Loaded {len(self.samples)} samples from {len(self.channel_names)} channels")
    
    def _prepare_arrays(self):
        """Convert samples to numpy arrays."""
        print("📊 Preparing data arrays...")
        
        # Build 2D array: (num_samples, num_channels)
        self.data_array = np.zeros((len(self.samples), len(self.channel_names)))
        self.timestamps = np.zeros(len(self.samples))
        
        for i, sample in enumerate(self.samples):
            self.timestamps[i] = sample['time_sec']
            for j, ch in enumerate(self.channel_names):
                self.data_array[i, j] = sample[ch]
        
        print(f"✓ Array shape: {self.data_array.shape} (samples × channels)")
    
    def compute_statistics(self) -> Dict[str, Any]:
        """Compute comprehensive statistics for all channels."""
        print("\n📈 Computing statistics...")
        
        stats_dict = {}
        
        for i, ch in enumerate(self.channel_names):
            ch_data = self.data_array[:, i]
            
            stats_dict[ch] = {
                'mean': float(np.mean(ch_data)),
                'std': float(np.std(ch_data)),
                'min': float(np.min(ch_data)),
                'max': float(np.max(ch_data)),
                'median': float(np.median(ch_data)),
                'q25': float(np.percentile(ch_data, 25)),
                'q75': float(np.percentile(ch_data, 75)),
                'range': float(np.ptp(ch_data)),
                'variance': float(np.var(ch_data)),
                'skewness': float(stats.skew(ch_data)),
                'kurtosis': float(stats.kurtosis(ch_data)),
            }
        
        print("✓ Statistics computed for all channels")
        return stats_dict
    
    def print_statistics(self, stats_dict: Dict[str, Any]):
        """Print statistics table."""
        print("\n" + "=" * 90)
        print("CHANNEL STATISTICS")
        print("=" * 90)
        print(f"{'Channel':<8} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10} {'Median':>10} {'Range':>10}")
        print("-" * 90)
        
        for ch in self.channel_names:
            s = stats_dict[ch]
            print(f"{ch:<8} {s['mean']:>10.2f} {s['std']:>10.2f} {s['min']:>10.2f} "
                  f"{s['max']:>10.2f} {s['median']:>10.2f} {s['range']:>10.2f}")
        
        print()
    
    def compute_frequency_analysis(self, channel_idx: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute power spectral density for a channel.
        
        Args:
            channel_idx: Index of channel to analyze
            
        Returns:
            Tuple of (frequencies, power_spectrum)
        """
        ch_data = self.data_array[:, channel_idx]
        
        # Compute PSD using Welch's method
        freqs, psd = signal.welch(
            ch_data,
            fs=self.sample_rate,
            nperseg=min(256, len(ch_data))
        )
        
        return freqs, psd
    
    def plot_time_series(self, output_path: Path):
        """
        Plot time series for all channels.
        
        Args:
            output_path: Path to save the plot
        """
        print("📉 Generating time series plot...")
        
        fig, axes = plt.subplots(7, 2, figsize=(15, 14))
        fig.suptitle(f'EEG Time Series - {self.metadata["device"]}\n'
                     f'Recording: {self.metadata["start_time_iso"][:19]}',
                     fontsize=14, fontweight='bold')
        
        axes = axes.flatten()
        
        for i, ch in enumerate(self.channel_names):
            ax = axes[i]
            ch_data = self.data_array[:, i]
            
            ax.plot(self.timestamps, ch_data, linewidth=0.5, color='steelblue')
            ax.set_title(ch, fontweight='bold', fontsize=10)
            ax.set_xlabel('Time (s)', fontsize=8)
            ax.set_ylabel('Amplitude', fontsize=8)
            ax.grid(True, alpha=0.3)
            ax.tick_params(labelsize=7)
            
            # Add statistics
            mean = np.mean(ch_data)
            std = np.std(ch_data)
            ax.axhline(mean, color='red', linestyle='--', linewidth=0.8, alpha=0.7, label=f'Mean: {mean:.1f}')
            ax.fill_between(self.timestamps, mean - std, mean + std, alpha=0.2, color='red', label=f'±1 SD')
            ax.legend(fontsize=6, loc='upper right')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved: {output_path.name}")
    
    def plot_frequency_spectrum(self, output_path: Path):
        """
        Plot frequency spectrum for all channels.
        
        Args:
            output_path: Path to save the plot
        """
        print("📊 Generating frequency spectrum plot...")
        
        fig, axes = plt.subplots(7, 2, figsize=(15, 14))
        fig.suptitle(f'Power Spectral Density - {self.metadata["device"]}\n'
                     f'Sampling Rate: {self.sample_rate} Hz',
                     fontsize=14, fontweight='bold')
        
        axes = axes.flatten()
        
        for i, ch in enumerate(self.channel_names):
            ax = axes[i]
            ch_data = self.data_array[:, i]
            
            # Compute PSD
            freqs, psd = signal.welch(
                ch_data,
                fs=self.sample_rate,
                nperseg=min(256, len(ch_data))
            )
            
            # Plot up to 60 Hz
            mask = freqs <= 60
            ax.semilogy(freqs[mask], psd[mask], linewidth=1.5, color='darkgreen')
            ax.set_title(ch, fontweight='bold', fontsize=10)
            ax.set_xlabel('Frequency (Hz)', fontsize=8)
            ax.set_ylabel('Power', fontsize=8)
            ax.grid(True, alpha=0.3, which='both')
            ax.tick_params(labelsize=7)
            
            # Mark common bands
            ax.axvspan(0.5, 4, alpha=0.1, color='purple', label='Delta')
            ax.axvspan(4, 8, alpha=0.1, color='blue', label='Theta')
            ax.axvspan(8, 13, alpha=0.1, color='green', label='Alpha')
            ax.axvspan(13, 30, alpha=0.1, color='orange', label='Beta')
            ax.legend(fontsize=5, loc='upper right')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved: {output_path.name}")
    
    def plot_channel_heatmap(self, output_path: Path):
        """
        Plot heatmap showing all channels over time.
        
        Args:
            output_path: Path to save the plot
        """
        print("🗺️  Generating channel heatmap...")
        
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Normalize each channel for better visualization
        data_normalized = (self.data_array - self.data_array.mean(axis=0)) / self.data_array.std(axis=0)
        
        im = ax.imshow(
            data_normalized.T,
            aspect='auto',
            cmap='RdBu_r',
            interpolation='bilinear',
            extent=[self.timestamps[0], self.timestamps[-1], 0, len(self.channel_names)]
        )
        
        ax.set_yticks(np.arange(len(self.channel_names)) + 0.5)
        ax.set_yticklabels(self.channel_names)
        ax.set_xlabel('Time (seconds)', fontsize=12)
        ax.set_ylabel('Channel', fontsize=12)
        ax.set_title(f'EEG Channel Activity Heatmap (Normalized)\n'
                     f'{self.metadata["device"]} - {len(self.samples)} samples',
                     fontsize=14, fontweight='bold')
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Normalized Amplitude (σ)', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved: {output_path.name}")
    
    def plot_correlation_matrix(self, output_path: Path):
        """
        Plot correlation matrix between channels.
        
        Args:
            output_path: Path to save the plot
        """
        print("🔗 Generating correlation matrix...")
        
        # Compute correlation matrix
        corr_matrix = np.corrcoef(self.data_array.T)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
        
        ax.set_xticks(np.arange(len(self.channel_names)))
        ax.set_yticks(np.arange(len(self.channel_names)))
        ax.set_xticklabels(self.channel_names, rotation=45, ha='right')
        ax.set_yticklabels(self.channel_names)
        
        # Add correlation values
        for i in range(len(self.channel_names)):
            for j in range(len(self.channel_names)):
                text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                             ha="center", va="center", color="black", fontsize=7)
        
        ax.set_title('Channel Correlation Matrix\n'
                     f'{self.metadata["device"]}',
                     fontsize=14, fontweight='bold', pad=20)
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Correlation Coefficient', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved: {output_path.name}")
    
    def plot_band_power(self, output_path: Path):
        """
        Plot relative band power for each channel.
        
        Args:
            output_path: Path to save the plot
        """
        print("🎵 Generating band power analysis...")
        
        # Define frequency bands
        bands = {
            'Delta (0.5-4 Hz)': (0.5, 4),
            'Theta (4-8 Hz)': (4, 8),
            'Alpha (8-13 Hz)': (8, 13),
            'Beta (13-30 Hz)': (13, 30),
            'Gamma (30-50 Hz)': (30, 50)
        }
        
        # Compute band power for each channel
        band_powers = {band: [] for band in bands.keys()}
        
        for i, ch in enumerate(self.channel_names):
            ch_data = self.data_array[:, i]
            
            # Compute PSD
            freqs, psd = signal.welch(
                ch_data,
                fs=self.sample_rate,
                nperseg=min(256, len(ch_data))
            )
            
            # Calculate power in each band
            for band_name, (low, high) in bands.items():
                idx = np.logical_and(freqs >= low, freqs <= high)
                band_power = np.trapz(psd[idx], freqs[idx])
                band_powers[band_name].append(band_power)
        
        # Create grouped bar plot
        fig, ax = plt.subplots(figsize=(15, 8))
        
        x = np.arange(len(self.channel_names))
        width = 0.15
        colors = ['purple', 'blue', 'green', 'orange', 'red']
        
        for i, (band_name, color) in enumerate(zip(bands.keys(), colors)):
            offset = width * (i - 2)
            powers = band_powers[band_name]
            ax.bar(x + offset, powers, width, label=band_name, color=color, alpha=0.8)
        
        ax.set_xlabel('Channel', fontsize=12, fontweight='bold')
        ax.set_ylabel('Relative Power', fontsize=12, fontweight='bold')
        ax.set_title(f'Frequency Band Power by Channel\n{self.metadata["device"]}',
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(self.channel_names, rotation=45, ha='right')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved: {output_path.name}")
        
        return band_powers
    
    def plot_statistical_summary(self, stats_dict: Dict[str, Any], output_path: Path):
        """
        Plot statistical summary visualization.
        
        Args:
            stats_dict: Statistics dictionary
            output_path: Path to save the plot
        """
        print("📊 Generating statistical summary plot...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Statistical Summary - {self.metadata["device"]}\n'
                     f'Duration: {self.metadata["duration_sec"]:.1f}s, '
                     f'Samples: {self.metadata["num_samples"]}',
                     fontsize=14, fontweight='bold')
        
        channels = self.channel_names
        
        # 1. Mean values by channel
        ax = axes[0, 0]
        means = [stats_dict[ch]['mean'] for ch in channels]
        stds = [stats_dict[ch]['std'] for ch in channels]
        ax.bar(channels, means, color='steelblue', alpha=0.7)
        ax.errorbar(channels, means, yerr=stds, fmt='none', color='black', capsize=3)
        ax.set_title('Mean Amplitude by Channel', fontweight='bold')
        ax.set_ylabel('Mean Amplitude')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        # 2. Range (min-max) by channel
        ax = axes[0, 1]
        ranges = [stats_dict[ch]['range'] for ch in channels]
        ax.bar(channels, ranges, color='coral', alpha=0.7)
        ax.set_title('Signal Range by Channel', fontweight='bold')
        ax.set_ylabel('Range (Max - Min)')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        # 3. Box plot of all channels
        ax = axes[1, 0]
        data_for_box = [self.data_array[:, i] for i in range(len(channels))]
        bp = ax.boxplot(data_for_box, labels=channels, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightgreen')
            patch.set_alpha(0.7)
        ax.set_title('Distribution by Channel (Box Plot)', fontweight='bold')
        ax.set_ylabel('Amplitude')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        # 4. Variance by channel
        ax = axes[1, 1]
        variances = [stats_dict[ch]['variance'] for ch in channels]
        ax.bar(channels, variances, color='mediumpurple', alpha=0.7)
        ax.set_title('Variance by Channel', fontweight='bold')
        ax.set_ylabel('Variance')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Saved: {output_path.name}")
    
    def save_statistics_json(self, stats_dict: Dict[str, Any], output_path: Path):
        """Save statistics as JSON."""
        print("💾 Saving statistics to JSON...")
        
        stats_output = {
            "source_file": self.json_file.name,
            "analysis_timestamp": datetime.now().isoformat(),
            "metadata": self.metadata,
            "channel_statistics": stats_dict
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats_output, f, indent=2, ensure_ascii=False)
        
        file_size = output_path.stat().st_size / 1024
        print(f"✓ Saved: {output_path.name} ({file_size:.1f} KB)")
    
    def generate_report(self, output_dir: Path):
        """
        Generate comprehensive analysis report.
        
        Args:
            output_dir: Directory to save all outputs
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Base name for outputs
        base_name = self.json_file.stem
        
        print("\n" + "=" * 70)
        print("COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 70)
        print(f"\nSource: {self.json_file.name}")
        print(f"Output Directory: {output_dir}\n")
        
        # Compute statistics
        stats_dict = self.compute_statistics()
        self.print_statistics(stats_dict)
        
        # Generate all visualizations
        print("\n🎨 Generating visualizations...\n")
        
        self.plot_time_series(output_dir / f"{base_name}_timeseries.png")
        self.plot_frequency_spectrum(output_dir / f"{base_name}_frequency.png")
        self.plot_channel_heatmap(output_dir / f"{base_name}_heatmap.png")
        self.plot_correlation_matrix(output_dir / f"{base_name}_correlation.png")
        self.plot_band_power(output_dir / f"{base_name}_bandpower.png")
        
        # Save statistics
        self.save_statistics_json(stats_dict, output_dir / f"{base_name}_statistics.json")
        
        print("\n" + "=" * 70)
        print("✨ ANALYSIS COMPLETE!")
        print("=" * 70)
        print(f"\nGenerated files in {output_dir}:")
        print(f"  • {base_name}_timeseries.png    - Time series for all channels")
        print(f"  • {base_name}_frequency.png     - Power spectral density")
        print(f"  • {base_name}_heatmap.png       - Activity heatmap")
        print(f"  • {base_name}_correlation.png   - Channel correlations")
        print(f"  • {base_name}_bandpower.png     - Frequency band analysis")
        print(f"  • {base_name}_statistics.json   - Numerical statistics")
        print()


def main():
    """Main execution function."""
    print("=" * 70)
    print("  Emotiv EPOC X - EEG Data Analyzer")
    print("=" * 70)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\nUsage: python analyze_json.py <json_file>")
        print("\nExample:")
        print("  python analyze_json.py data/json/eeg_data_20251001_001535.json")
        print("\nOr analyze the most recent file:")
        print("  python analyze_json.py --latest")
        print()
        return
    
    # Handle --latest flag
    if sys.argv[1] == '--latest':
        data_dir = Path(__file__).parent.parent / "data" / "json"
        json_files = sorted(data_dir.glob("eeg_data_*.json"))
        
        if not json_files:
            print("❌ No JSON files found in data/json/")
            return
        
        json_file = json_files[-1]
        print(f"\n📂 Using most recent file: {json_file.name}\n")
    else:
        json_file = Path(sys.argv[1])
        
        if not json_file.exists():
            print(f"❌ File not found: {json_file}")
            return
    
    # Create analyzer
    try:
        analyzer = EEGAnalyzer(json_file)
        
        # Generate report
        output_dir = Path(__file__).parent.parent / "data" / "plots"
        analyzer.generate_report(output_dir)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis cancelled by user")
        sys.exit(0)

