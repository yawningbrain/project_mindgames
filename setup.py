"""Setup script for emotiv-lsl package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="emotiv-lsl",
    version="1.0.0",
    author="Emotiv LSL Contributors",
    description="LSL server for Emotiv EPOC X EEG headset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/emotiv-lsl",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "hidapi>=0.14.0",
        "pycryptodome>=3.19.0",
        "pylsl>=1.16.1",
    ],
    extras_require={
        "dev": [
            "mne>=1.5.1",
            "numpy>=1.26.0",
            "scipy>=1.11.3",
            "matplotlib>=3.8.0",
            "pyshark>=0.6",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "analysis": [
            "mne>=1.5.1",
            "numpy>=1.26.0",
            "scipy>=1.11.3",
            "matplotlib>=3.8.0",
        ],
        "pyshark": [
            "pyshark>=0.6",
        ],
    },
    entry_points={
        "console_scripts": [
            "emotiv-lsl=main:main",
        ],
    },
)

