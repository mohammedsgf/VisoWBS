"""
Tree builder for constructing WBS tree structure from records.
"""

from typing import List
from wbsviz.core.model import Record, Node, Tree
from wbsviz.core.common import valid_code, parent_code


class TreeBuilder:
    """Builds tree structure from WBS records."""
    
    def __init__(self, strict: bool = True):
        """
        Initialize tree builder.
        
        Args:
            strict: If True, raise error on missing parents.
                   If False, auto-create missing parent nodes.
        """
        self.strict = strict
    
    def build(self, records: List[Record]) -> Tree:
        """
        Build tree from records.
        
        Args:
            records: List of WBS records
            
        Returns:
            Tree structure
            
        Raises:
            ValueError: If codes are invalid or duplicates found (or missing parents in strict mode)
        """
        tree = Tree()
        
        # Create nodes and validate
        for record in records:
            if not valid_code(record.code):
                raise ValueError(f"Invalid code: {record.code}")
            
            if record.code in tree.store:
                raise ValueError(f"Duplicate code: {record.code}")
            
            node = Node()
            node.code = record.code
            node.title = record.title
            node.description = record.description
            node.primaryResp = record.primaryResp
            node.seconderyResp = record.seconderyResp
            node.estimateDuration = record.estimateDuration
            
            tree.store[record.code] = node
        
        # Ensure parents exist (auto-create if !strict)
        def ensure_parent(code: str):
            if not code:
                return
            
            if code not in tree.store:
                if self.strict:
                    raise ValueError(f"Missing parent: {code}")
                
                # Auto-create parent
                parent = Node()
                parent.code = code
                parent.title = f"[Auto] {code}"
                tree.store[code] = parent
                
                # Recursively ensure grandparent
                ensure_parent(parent_code(code))
        
        for code in list(tree.store.keys()):
            ensure_parent(parent_code(code))
        
        # Link children and roots
        for node in tree.store.values():
            parent_code_str = parent_code(node.code)
            if not parent_code_str:
                tree.roots.append(node)
            else:
                parent = tree.store[parent_code_str]
                parent.children.append(node)
        
        # Sort by numeric code segments
        def code_less(a: Node, b: Node) -> bool:
            def split_code(s: str) -> List[int]:
                return [int(x) for x in s.split('.')]
            
            a_parts = split_code(a.code)
            b_parts = split_code(b.code)
            
            min_len = min(len(a_parts), len(b_parts))
            for i in range(min_len):
                if a_parts[i] != b_parts[i]:
                    return a_parts[i] < b_parts[i]
            
            return len(a_parts) < len(b_parts)
        
        # Sort children for each node
        for node in tree.store.values():
            node.children.sort(key=lambda n: tuple(int(x) for x in n.code.split('.')))
        
        # Sort roots
        tree.roots.sort(key=lambda n: tuple(int(x) for x in n.code.split('.')))
        
        return tree

