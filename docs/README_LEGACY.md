# WBS Visualizer - Python GUI Application

A desktop GUI application for visualizing Work Breakdown Structures (WBS) from CSV files using Graphviz.

## Features

- **Two-tab interface:**
  - **Data Entry tab**: Enter WBS data directly or load from CSV
  - **Visualization tab**: Configure options and generate diagrams

- **Flexible input**: Load from CSV file or enter data directly in the GUI
- **Multiple output formats**: SVG, PDF, PNG, or DOT format
- **Configurable options**: 
  - Rank direction (Top-Bottom or Left-Right)
  - Strict mode (error on missing parents) vs auto-create mode
- **Visual feedback**: Status bar and error dialogs

## Requirements

1. **Python 3.7 or higher**

2. **Graphviz system binaries** - Must be installed on your system:
   - **Linux**: `sudo apt-get install graphviz` (or equivalent)
   - **macOS**: `brew install graphviz`
   - **Windows**: Download from [Graphviz website](https://graphviz.org/download/)

3. **Python package dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Installation

1. Install Graphviz binaries on your system (see Requirements above)

2. Install Python dependencies:
   ```bash
   cd python
   pip install -r requirements.txt
   ```

## Usage

### Running the GUI

```bash
cd python
python gui.py
```

### Using the Application

1. **Data Entry Tab**:
   - Option 1: Click "Load from CSV..." to load an existing CSV file
   - Option 2: Enter data directly in the text area (tab-separated columns)
   - Click "Parse Data" to validate the entered data
   - Click "Save to CSV..." to save your data

2. **Visualization Tab**:
   - Select input CSV file (or use parsed data from Data Entry tab)
   - Choose output file path
   - Select output format (SVG, PDF, PNG, or DOT)
   - Choose rank direction (Top-Bottom or Left-Right)
   - Toggle strict mode if desired
   - Click "Generate Diagram" to create the visualization
   - Click "Open Output File" to view the generated diagram

### CSV Format

The CSV file should have the following columns (case-insensitive headers):

- **code** (required): Hierarchical code like "1", "1.1", "1.2.3", etc.
- **title** (required): Node title
- **description** (optional): Detailed description
- **primaryResp** (optional): Primary responsible person
- **seconderyResp** (optional): Secondary responsible person  
- **estimateDuration** (optional): Duration estimate

Example:
```csv
code,title,description,primaryResp,seconderyResp,estimateDuration
1,Project,Overall project scope and goals,PM,,30d
1.1,Initiation,Decide scope and stakeholders,PM,,2d
1.1.1,Project Charter,Create and approve the charter,PM,,1d
```

## Command Line Alternative

You can also use the Python package from command line:

```python
from wbsviz import CsvReader, TreeBuilder, DotBuilder
import graphviz

# Read CSV
reader = CsvReader("example.csv")
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

## Differences from C++ Version

The Python version provides:
- GUI interface for easier use
- Data entry tab for creating/editing WBS data
- Cross-platform compatibility (Linux, macOS, Windows)
- Easier to extend and modify

The core functionality (CSV parsing, tree building, DOT generation) matches the C++ version.

## Troubleshooting

**"graphviz not found" error:**
- Ensure Graphviz binaries are installed and in your system PATH
- Verify with: `dot -V` (should show version)

**Import errors:**
- Make sure you've run: `pip install -r requirements.txt`
- Check that you're using Python 3.7+

**Rendering fails:**
- Check that the output directory is writable
- Verify Graphviz is properly installed
- Try generating DOT format first to debug

## License

Same as the main project.

