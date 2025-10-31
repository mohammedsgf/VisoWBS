"""
WBS Visualizer - A Work Breakdown Structure visualization tool.
"""

__version__ = "1.0.0"
__author__ = "WBS Visualizer Team"

from wbsviz.core.model import Record, Node, Tree
from wbsviz.core.csv_reader import CsvReader
from wbsviz.core.tree_builder import TreeBuilder
from wbsviz.core.dot_builder import DotBuilder

__all__ = [
    'Record',
    'Node',
    'Tree',
    'CsvReader',
    'TreeBuilder',
    'DotBuilder',
    '__version__',
]

