# Project Structure

This document describes the professional structure of the WBS Visualizer project.

## Directory Layout

```
TestGraphivz/
├── wbsviz/                    # Main Python package
│   ├── __init__.py           # Package initialization and exports
│   ├── core/                 # Core functionality
│   │   ├── __init__.py       # Core module exports
│   │   ├── model.py          # Data models (Record, Node, Tree)
│   │   ├── common.py         # Utility functions
│   │   ├── csv_reader.py     # CSV file reading
│   │   ├── tree_builder.py   # Tree construction logic
│   │   └── dot_builder.py    # DOT format generation
│   └── gui/                  # GUI components
│       ├── __init__.py
│       └── main.py           # Tkinter GUI implementation
│
├── wbsviz_gui.py             # Main GUI entry point (executable)
├── setup.py                   # Package setup and installation
├── requirements.txt           # Python dependencies
├── README.md                  # Main project documentation
├── .gitignore                # Git ignore patterns
│
├── examples/                 # Example files
│   └── example.csv           # Sample WBS CSV file
│
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_basic.py         # Basic functionality tests
│
├── docs/                      # Documentation
│   └── README_LEGACY.md      # Legacy C++ documentation
│
└── legacy/                    # Legacy C++ implementation
    ├── src/                  # C++ source files
    ├── include/              # C++ headers
    ├── CMakeLists.txt        # CMake configuration
    └── build/                # Build artifacts (kept for reference)
```

## Key Files

### Entry Points

- **`wbsviz_gui.py`**: Main entry point for the GUI application. Run with `python wbsviz_gui.py`
- **`setup.py`**: Package installation script. Install with `pip install -e .`

### Core Package (`wbsviz/core/`)

- **`model.py`**: Defines data structures:
  - `Record`: Represents a CSV row
  - `Node`: Tree node with hierarchical relationships
  - `Tree`: Container for the entire tree structure

- **`common.py`**: Utility functions:
  - CSV line parsing with quote handling
  - Code validation (hierarchical format)
  - Parent code extraction
  - String escaping for DOT format

- **`csv_reader.py`**: Reads and parses CSV files with:
  - Case-insensitive headers
  - Required field validation
  - Optional field support

- **`tree_builder.py`**: Constructs tree structure:
  - Validates hierarchical codes
  - Handles strict/non-strict modes
  - Auto-creates missing parents (non-strict)
  - Sorts nodes numerically

- **`dot_builder.py`**: Generates Graphviz DOT format:
  - Level-based color coding
  - Configurable rank direction
  - Metadata display in labels

### GUI Package (`wbsviz/gui/`)

- **`main.py`**: Tkinter-based GUI with:
  - Two-tab interface (Data Entry + Visualization)
  - File dialogs for CSV input/output
  - Format selection (SVG, PDF, PNG, DOT)
  - Configuration options

## Development Workflow

1. **Install in development mode**: `pip install -e ".[dev]"`
2. **Run GUI**: `python wbsviz_gui.py`
3. **Run tests**: `pytest tests/`
4. **Build package**: `python setup.py sdist bdist_wheel`

## Legacy Code

The original C++ implementation has been moved to `legacy/` directory for reference purposes. It is no longer actively maintained but can be used as a reference for algorithm details.

