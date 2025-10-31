"""
Main GUI application for WBS Visualizer.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import subprocess
import sys
import os

from wbsviz.core.csv_reader import CsvReader
from wbsviz.core.tree_builder import TreeBuilder
from wbsviz.core.dot_builder import DotBuilder
from wbsviz.core.model import Record


class WBSVisualizerGUI:
    """Main GUI application window."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("WBS Visualizer")
        self.root.geometry("900x700")
        
        # Default values
        self.input_file = tk.StringVar(value="")
        self.output_file = tk.StringVar(value="")
        self.format_var = tk.StringVar(value="svg")
        self.rankdir_var = tk.StringVar(value="TB")
        self.strict_var = tk.BooleanVar(value=True)
        
        # Data storage
        self.records = []
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Data Entry
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="Data Entry")
        self.create_data_tab(data_frame)
        
        # Tab 2: Visualization
        viz_frame = ttk.Frame(notebook)
        notebook.add(viz_frame, text="Visualization")
        self.create_viz_tab(viz_frame)
        
        # Status bar at bottom
        self.status_bar = tk.Label(
            self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_data_tab(self, parent):
        """Create the data entry tab."""
        # Instructions
        instructions = tk.Label(
            parent,
            text="Enter WBS data below or load from CSV file. Columns: code, title, description, primaryResp, seconderyResp, estimateDuration",
            wraplength=800,
            justify=tk.LEFT
        )
        instructions.pack(pady=5, padx=10, anchor=tk.W)
        
        # Load CSV button
        load_frame = ttk.Frame(parent)
        load_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            load_frame,
            text="Load from CSV...",
            command=self.load_csv
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            load_frame,
            text="Save to CSV...",
            command=self.save_csv
        ).pack(side=tk.LEFT, padx=5)
        
        # Data entry table (simplified - using Text widget with column headers)
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Headers
        headers = ["Code", "Title", "Description", "Primary Resp", "Secondary Resp", "Estimate Duration"]
        header_frame = ttk.Frame(table_frame)
        header_frame.pack(fill=tk.X)
        
        col_widths = [80, 150, 200, 120, 120, 120]
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            label = ttk.Label(header_frame, text=header, font=("Arial", 9, "bold"))
            label.grid(row=0, column=i, padx=2, pady=2, sticky=tk.W)
        
        # Scrollable text area for data entry
        text_frame = ttk.Frame(table_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.data_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.NONE,
            font=("Courier", 9),
            width=100,
            height=20
        )
        self.data_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert header row
        header_row = "\t".join(headers) + "\n"
        self.data_text.insert(tk.END, header_row)
        
        # Add some example data
        example = "\t".join(["1", "Project", "Overall project", "PM", "", "30d"]) + "\n"
        self.data_text.insert(tk.END, example)
        
        # Button to parse data
        ttk.Button(
            parent,
            text="Parse Data",
            command=self.parse_data
        ).pack(pady=5)
    
    def create_viz_tab(self, parent):
        """Create the visualization tab."""
        # Input file section
        input_frame = ttk.LabelFrame(parent, text="Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="CSV File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E
        )
        ttk.Button(input_frame, text="Browse...", command=self.browse_input).grid(
            row=0, column=2, padx=5, pady=5
        )
        input_frame.columnconfigure(1, weight=1)
        
        # Output file section
        output_frame = ttk.LabelFrame(parent, text="Output", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_file, width=50).grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E
        )
        ttk.Button(output_frame, text="Browse...", command=self.browse_output).grid(
            row=0, column=2, padx=5, pady=5
        )
        output_frame.columnconfigure(1, weight=1)
        
        # Options section
        options_frame = ttk.LabelFrame(parent, text="Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Format
        ttk.Label(options_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        format_combo = ttk.Combobox(
            options_frame,
            textvariable=self.format_var,
            values=["svg", "pdf", "png", "dot"],
            state="readonly",
            width=10
        )
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Rank direction
        ttk.Label(options_frame, text="Rank Direction:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        rank_frame = ttk.Frame(options_frame)
        rank_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(
            rank_frame, text="Top-Bottom", variable=self.rankdir_var, value="TB"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            rank_frame, text="Left-Right", variable=self.rankdir_var, value="LR"
        ).pack(side=tk.LEFT, padx=5)
        
        # Strict mode
        ttk.Checkbutton(
            options_frame,
            text="Strict mode (error on missing parents)",
            variable=self.strict_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Generate button
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Generate Diagram",
            command=self.generate_diagram,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Open Output File",
            command=self.open_output
        ).pack(side=tk.LEFT, padx=10)
    
    def load_csv(self):
        """Load CSV file into data entry text area."""
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.data_text.delete(1.0, tk.END)
                    self.data_text.insert(1.0, content)
                    self.input_file.set(filename)
                    self.update_status(f"Loaded CSV: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {e}")
    
    def save_csv(self):
        """Save data entry content to CSV file."""
        filename = filedialog.asksaveasfilename(
            title="Save CSV file",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                content = self.data_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.update_status(f"Saved CSV: {filename}")
                messagebox.showinfo("Success", f"Saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save CSV: {e}")
    
    def parse_data(self):
        """Parse data from text area and validate."""
        content = self.data_text.get(1.0, tk.END).strip()
        lines = content.split('\n')
        if not lines:
            messagebox.showwarning("Warning", "No data to parse")
            return
        
        # Skip header if present
        start_idx = 0
        if len(lines) > 0:
            first_line_lower = lines[0].lower()
            if 'code' in first_line_lower and 'title' in first_line_lower:
                start_idx = 1
        
        self.records = []
        errors = []
        
        for i, line in enumerate(lines[start_idx:], start=start_idx + 1):
            line = line.strip()
            if not line:
                continue
            
            # Simple tab-separated parsing
            parts = line.split('\t')
            if len(parts) < 2:
                errors.append(f"Line {i}: Needs at least code and title")
                continue
            
            record = Record(
                code=parts[0].strip(),
                title=parts[1].strip() if len(parts) > 1 else "",
                description=parts[2].strip() if len(parts) > 2 else "",
                primaryResp=parts[3].strip() if len(parts) > 3 else "",
                seconderyResp=parts[4].strip() if len(parts) > 4 else "",
                estimateDuration=parts[5].strip() if len(parts) > 5 else ""
            )
            
            if not record.code or not record.title:
                errors.append(f"Line {i}: Missing code or title")
                continue
            
            self.records.append(record)
        
        if errors:
            messagebox.showwarning("Parsing Warnings", "\n".join(errors))
        
        if self.records:
            self.update_status(f"Parsed {len(self.records)} records")
            messagebox.showinfo("Success", f"Parsed {len(self.records)} records")
        else:
            messagebox.showwarning("Warning", "No valid records found")
    
    def browse_input(self):
        """Browse for input CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-set output file if not set
            if not self.output_file.get():
                base = Path(filename).stem
                output_dir = Path(filename).parent
                format_ext = self.format_var.get()
                output_path = output_dir / f"{base}_diagram.{format_ext}"
                self.output_file.set(str(output_path))
    
    def browse_output(self):
        """Browse for output file."""
        format_ext = self.format_var.get()
        filename = filedialog.asksaveasfilename(
            title="Save diagram as",
            defaultextension=f".{format_ext}",
            filetypes=[(f"{format_ext.upper()} files", f"*.{format_ext}"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def generate_diagram(self):
        """Generate the WBS diagram."""
        # Determine input source
        input_path = self.input_file.get()
        records_to_use = []
        
        if input_path and Path(input_path).exists():
            # Use CSV file
            try:
                reader = CsvReader(input_path)
                records_to_use = reader.read()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV: {e}")
                return
        elif self.records:
            # Use parsed records from data tab
            records_to_use = self.records
        else:
            messagebox.showwarning("Warning", "Please load a CSV file or parse data first")
            return
        
        if not records_to_use:
            messagebox.showwarning("Warning", "No data to visualize")
            return
        
        output_path = self.output_file.get()
        if not output_path:
            # Auto-generate output path
            if input_path:
                base = Path(input_path).stem
                output_dir = Path(input_path).parent
            else:
                base = "diagram"
                output_dir = Path.cwd()
            
            format_ext = self.format_var.get()
            output_path = output_dir / f"{base}_diagram.{format_ext}"
            self.output_file.set(str(output_path))
        
        try:
            self.update_status("Building tree...")
            self.root.update()
            
            # Build tree
            builder = TreeBuilder(strict=self.strict_var.get())
            tree = builder.build(records_to_use)
            
            self.update_status("Generating DOT...")
            self.root.update()
            
            # Generate DOT
            dot_builder = DotBuilder(rankdir=self.rankdir_var.get())
            dot_content = dot_builder.build(tree)
            
            format_type = self.format_var.get()
            
            if format_type == "dot":
                # Just save DOT file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(dot_content)
                self.update_status(f"Saved DOT to {output_path}")
            else:
                # Render using graphviz
                self.update_status("Rendering diagram...")
                self.root.update()
                
                try:
                    import graphviz
                    source = graphviz.Source(dot_content)
                    source.render(
                        filename=str(Path(output_path).with_suffix('')),
                        format=format_type,
                        cleanup=True
                    )
                    self.update_status(f"Generated {format_type.upper()} to {output_path}")
                    messagebox.showinfo("Success", f"Diagram generated successfully!\n{output_path}")
                except ImportError:
                    messagebox.showerror(
                        "Error",
                        "graphviz Python package not found.\n"
                        "Install it with: pip install graphviz\n"
                        "Also ensure Graphviz binaries are installed on your system."
                    )
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to render diagram: {e}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate diagram: {e}")
            self.update_status(f"Error: {e}")
    
    def open_output(self):
        """Open the output file with system default application."""
        output_path = self.output_file.get()
        if not output_path or not Path(output_path).exists():
            messagebox.showwarning("Warning", "Output file does not exist")
            return
        
        try:
            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_path])
            else:
                subprocess.run(["xdg-open", output_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
    
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_bar.config(text=message)
        self.root.update_idletasks()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = WBSVisualizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

