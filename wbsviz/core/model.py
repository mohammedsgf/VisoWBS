"""
Data model classes for WBS visualizer.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import OrderedDict


@dataclass
class Record:
    """CSV record representing a WBS item."""
    code: str
    title: str
    description: str = ""
    primaryResp: str = ""
    seconderyResp: str = ""
    estimateDuration: str = ""


class Node:
    """Tree node representing a WBS item."""
    
    def __init__(self):
        self.code: str = ""
        self.title: str = ""
        self.description: str = ""
        self.primaryResp: str = ""
        self.seconderyResp: str = ""
        self.estimateDuration: str = ""
        self.children: List['Node'] = []


class Tree:
    """Tree structure containing WBS nodes."""
    
    def __init__(self):
        self.store: Dict[str, Node] = {}
        self.roots: List[Node] = []

