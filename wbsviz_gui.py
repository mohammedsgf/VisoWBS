#!/usr/bin/env python3
"""
Main entry point for WBS Visualizer GUI application.
"""

from wbsviz.gui.main import WBSVisualizerGUI
import tkinter as tk


def main():
    """Main entry point."""
    root = tk.Tk()
    app = WBSVisualizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
