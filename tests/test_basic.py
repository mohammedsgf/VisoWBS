"""
Basic tests for WBS Visualizer core functionality.
"""

import pytest
from pathlib import Path

from wbsviz.core.model import Record
from wbsviz.core.csv_reader import CsvReader
from wbsviz.core.tree_builder import TreeBuilder
from wbsviz.core.dot_builder import DotBuilder
from wbsviz.core.common import valid_code, parent_code


def test_valid_code():
    """Test code validation."""
    assert valid_code("1") is True
    assert valid_code("1.2") is True
    assert valid_code("1.2.3") is True
    assert valid_code("a") is False
    assert valid_code("1.a") is False
    assert valid_code("") is False


def test_parent_code():
    """Test parent code extraction."""
    assert parent_code("1.2.3") == "1.2"
    assert parent_code("1.2") == "1"
    assert parent_code("1") == ""


def test_record_creation():
    """Test Record creation."""
    record = Record(
        code="1.1",
        title="Test",
        description="Test description"
    )
    assert record.code == "1.1"
    assert record.title == "Test"
    assert record.description == "Test description"


def test_tree_builder():
    """Test tree building."""
    records = [
        Record(code="1", title="Root"),
        Record(code="1.1", title="Child 1"),
        Record(code="1.2", title="Child 2"),
    ]
    
    builder = TreeBuilder(strict=True)
    tree = builder.build(records)
    
    assert len(tree.roots) == 1
    assert tree.roots[0].code == "1"
    assert len(tree.roots[0].children) == 2


def test_dot_builder():
    """Test DOT generation."""
    records = [
        Record(code="1", title="Root"),
        Record(code="1.1", title="Child"),
    ]
    
    builder = TreeBuilder(strict=True)
    tree = builder.build(records)
    
    dot_builder = DotBuilder(rankdir="TB")
    dot = dot_builder.build(tree)
    
    assert "digraph WBS" in dot
    assert '"1"' in dot
    assert '"1.1"' in dot
    assert "Rank Direction: TB" not in dot  # Should not appear in DOT


def test_csv_reader_example():
    """Test reading example CSV if available."""
    example_csv = Path(__file__).parent.parent / "examples" / "example.csv"
    if example_csv.exists():
        reader = CsvReader(str(example_csv))
        records = reader.read()
        assert len(records) > 0
        assert all(record.code and record.title for record in records)

