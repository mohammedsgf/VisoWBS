"""
Setup script for WBS Visualizer.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="wbsviz",
    version="1.0.0",
    description="A Work Breakdown Structure visualizer that generates Graphviz diagrams from CSV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="WBS Visualizer Team",
    url="https://github.com/yourusername/wbsviz",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "graphviz>=0.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wbsviz-gui=wbsviz_gui:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

