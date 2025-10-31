# WBS Visualizer

A professional desktop application for visualizing Work Breakdown Structures (WBS) from CSV files using Graphviz. Create beautiful hierarchical diagrams with automatic layout, color coding, and flexible configuration options.

## Features

- 🎨 **Interactive GUI**: Two-tab interface for data entry and visualization
- 📊 **Flexible Input**: Load from CSV files or enter data directly in the GUI
- 🎯 **Multiple Formats**: Export to SVG, PDF, PNG, or DOT format
- 🌳 **Hierarchical Visualization**: Automatic tree layout with level-based color coding
- ⚙️ **Configurable Options**: 
  - Rank direction (Top-Bottom or Left-Right)
  - Strict mode (error on missing parents) vs auto-create mode
- 📝 **Rich Metadata**: Display responsibilities, estimates, and descriptions

## Installation

### Prerequisites

1. **Python 3.7 or higher**

2. **Graphviz system binaries** - Must be installed on your system:
   - **Linux (Ubuntu/Debian)**: `sudo apt-get install graphviz python3-tk`
   - **Linux (Fedora/RHEL)**: `sudo dnf install graphviz python3-tkinter`
   - **macOS**: `brew install graphviz`
   - **Windows**: Download from [Graphviz website](https://graphviz.org/download/)

### Install from Source

```bash
# Clone or download the repository
cd TestGraphivz

# Install the package
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

## Quick Start

### Running the GUI

```bash
python wbsviz_gui.py
```

Or if installed as a package:
```bash
wbsviz-gui
```

### Using the Application

1. **Data Entry Tab**:
   - Load a CSV file using "Load from CSV..." button
   - Or enter data directly in the text area (tab-separated columns)
   - Click "Parse Data" to validate
   - Save your work with "Save to CSV..."

2. **Visualization Tab**:
   - Select input CSV file
   - Choose output location and format
   - Configure options (format, rank direction, strict mode)
   - Click "Generate Diagram"
   - View with "Open Output File"

## CSV Format

Your CSV file should have these columns (headers are case-insensitive):

| Column | Required | Description |
|--------|----------|-------------|
| `code` | ✅ | Hierarchical code (e.g., "1", "1.1", "1.2.3") |
| `title` | ✅ | Node title/name |
| `description` | | Detailed description |
| `primaryResp` | | Primary responsible person |
| `seconderyResp` | | Secondary responsible person |
| `estimateDuration` | | Duration estimate (e.g., "30d", "2 weeks") |

### Example CSV

```csv
code,title,description,primaryResp,seconderyResp,estimateDuration
1,Project,Overall project scope and goals,PM,,30d
1.1,Initiation,Decide scope and stakeholders,PM,,2d
1.1.1,Project Charter,Create and approve the charter,PM,,1d
1.1.2,Stakeholder Register,List and analyze stakeholders,PM,,1d
1.2,Planning,Plan requirements and architecture,SE,PM,6d
```

## Project Structure

```
wbsviz/
├── wbsviz/              # Main package
│   ├── core/           # Core functionality
│   │   ├── model.py
│   │   ├── common.py
│   │   ├── csv_reader.py
│   │   ├── tree_builder.py
│   │   └── dot_builder.py
│   └── gui/            # GUI components
│       └── main.py
├── wbsviz_gui.py       # Main GUI entry point
├── setup.py            # Package setup
├── requirements.txt    # Python dependencies
├── examples/           # Example CSV files
└── tests/              # Test suite (future)
```

## Programmatic Usage

You can also use the core functionality programmatically:

```python
from wbsviz.core.csv_reader import CsvReader
from wbsviz.core.tree_builder import TreeBuilder
from wbsviz.core.dot_builder import DotBuilder
import graphviz

# Read CSV
reader = CsvReader("examples/example.csv")
records = reader.read()

# Build tree
builder = TreeBuilder(strict=True)
tree = builder.build(records)

# Generate DOT
dot_builder = DotBuilder(rankdir="TB")
dot = dot_builder.build(tree)

# Render
source = graphviz.Source(dot)
source.render("diagram", format="svg")
```

## Development

### Setup Development Environment

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

## Troubleshooting

### "tkinter not found"
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora/RHEL**: `sudo dnf install python3-tkinter`
- **macOS**: Usually included with Python
- **Windows**: Usually included with Python

### "graphviz not found"
- Ensure Graphviz binaries are installed (see Prerequisites)
- Verify installation: `dot -V` should show version
- Check that Graphviz is in your system PATH

### Rendering fails
- Verify Graphviz is properly installed
- Check output directory permissions
- Try generating DOT format first for debugging

## License

[Specify your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Legacy C++ Version

The original C++ implementation has been moved to the `legacy/` directory for reference.
