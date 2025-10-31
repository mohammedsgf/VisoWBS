"""
Common utility functions for WBS visualizer.
"""

import re
from typing import List


def split_csv_line(line: str) -> List[str]:
    """
    Split a CSV line, handling quoted fields properly.
    
    Args:
        line: CSV line string
        
    Returns:
        List of field values
    """
    fields = []
    current = ""
    in_quotes = False
    
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # Escaped quote
                current += '"'
                i += 1
            else:
                # Toggle quote state
                in_quotes = not in_quotes
        elif c == ',' and not in_quotes:
            # End of field
            fields.append(current)
            current = ""
        else:
            current += c
        i += 1
    
    # Add last field
    fields.append(current)
    return fields


def valid_code(code: str) -> bool:
    """
    Validate that a code matches the hierarchical pattern (e.g., "1.2.3").
    
    Args:
        code: Code string to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = re.compile(r'^\d+(\.\d+)*$')
    return bool(pattern.match(code))


def parent_code(code: str) -> str:
    """
    Extract parent code from a hierarchical code.
    
    Examples:
        "1.2.3" -> "1.2"
        "1.2" -> "1"
        "1" -> ""
        
    Args:
        code: Hierarchical code string
        
    Returns:
        Parent code, or empty string if root
    """
    pos = code.rfind('.')
    if pos == -1:
        return ""
    return code[:pos]


def to_lower(s: str) -> str:
    """
    Convert string to lowercase.
    
    Args:
        s: Input string
        
    Returns:
        Lowercase string
    """
    return s.lower()


def esc(s: str) -> str:
    """
    Escape special characters for DOT format.
    
    Args:
        s: String to escape
        
    Returns:
        Escaped string
    """
    result = []
    for c in s:
        if c in ('\\', '"'):
            result.append('\\')
        result.append(c)
    return ''.join(result)

