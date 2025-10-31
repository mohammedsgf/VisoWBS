"""
DOT format builder for Graphviz visualization.
"""

from typing import List
from io import StringIO
from wbsviz.core.model import Tree, Node
from wbsviz.core.common import esc


class DotBuilder:
    """Builds Graphviz DOT format strings from tree structures."""
    
    # Color palette matching C++ version
    LEVEL_PALETTE = [
        "#E3F2FD",  # L1  blue-50
        "#E8F5E9",  # L2  green-50
        "#FFF3E0",  # L3  orange-50
        "#F3E5F5",  # L4  purple-50
        "#FCE4EC",  # L5  pink-50
        "#E0F2F1",  # L6  teal-50
        "#FFFDE7",  # L7  yellow-50
        "#ECEFF1"   # L8  blue-grey-50
    ]
    
    def __init__(self, rankdir: str = "TB"):
        """
        Initialize DOT builder.
        
        Args:
            rankdir: Graph direction - "TB" (top-bottom) or "LR" (left-right)
        """
        self.rankdir = rankdir
    
    @staticmethod
    def level_of(code: str) -> int:
        """
        Calculate hierarchy level from code.
        
        Args:
            code: Hierarchical code string
            
        Returns:
            Level number (1 for "1", 2 for "1.1", etc.)
        """
        if not code:
            return 0
        return code.count('.') + 1
    
    @staticmethod
    def fill_by_level(code: str) -> str:
        """
        Get fill color based on hierarchy level.
        
        Args:
            code: Node code
            
        Returns:
            Hex color code
        """
        level = DotBuilder.level_of(code)
        if level <= 0:
            return "#FFFFFF"
        
        idx = (level - 1) % len(DotBuilder.LEVEL_PALETTE)
        return DotBuilder.LEVEL_PALETTE[idx]
    
    def emit_node(self, output: StringIO, node: Node) -> None:
        """
        Emit DOT node definition and recursively emit children.
        
        Args:
            output: StringIO stream to write to
            node: Node to emit
        """
        # Build label: first line is code + title
        label_parts = [f"{esc(node.code)}  {esc(node.title)}"]
        
        # Second line: metadata (if present)
        meta_parts = []
        if node.primaryResp:
            meta_parts.append(f"PR: {esc(node.primaryResp)}")
        if node.seconderyResp:
            meta_parts.append(f"SR: {esc(node.seconderyResp)}")
        if node.estimateDuration:
            meta_parts.append(f"Est: {esc(node.estimateDuration)}")
        
        if meta_parts:
            label_parts.append("\\n(" + " | ".join(meta_parts) + ")")
        
        label = "".join(label_parts)
        fill_color = self.fill_by_level(node.code)
        tooltip = esc(node.description) if node.description else ""
        
        # Emit node
        output.write(f'  "{esc(node.code)}"')
        output.write(f' [label="{label}",')
        output.write(' style="filled", shape=box, fontsize=10, margin="0.06,0.04",')
        output.write(f' penwidth=1.0, fillcolor="{fill_color}",')
        output.write(f' tooltip="{tooltip}",')
        output.write(' URL="#", target="_top"')
        output.write('];\n')
        
        # Emit edges to children
        for child in node.children:
            output.write(f'  "{esc(node.code)}" -> "{esc(child.code)}" [arrowhead=none];\n')
            self.emit_node(output, child)
    
    def build(self, tree: Tree) -> str:
        """
        Build complete DOT format string from tree.
        
        Args:
            tree: Tree structure
            
        Returns:
            DOT format string
        """
        output = StringIO()
        
        # Graph header
        rankdir_value = "LR" if self.rankdir == "LR" else "TB"
        output.write("digraph WBS {\n")
        output.write(
            f'  graph [rankdir={rankdir_value}, nodesep=0.6, ranksep=0.9, '
            f'splines=ortho, ordering=out, outputorder=edgesfirst];\n'
        )
        output.write(
            '  edge  [arrowhead=none, weight=3, tailport=s, headport=n, minlen=1];\n'
        )
        output.write('  node  [shape=box, style=rounded, fontsize=10];\n')
        
        # Emit all root nodes and their subtrees
        for root in tree.roots:
            self.emit_node(output, root)
        
        output.write("}\n")
        
        return output.getvalue()

