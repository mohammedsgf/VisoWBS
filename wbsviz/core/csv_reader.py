"""
CSV reader for WBS data files.
"""

from typing import List
from pathlib import Path
from wbsviz.core.model import Record
from wbsviz.core.common import split_csv_line, to_lower


class CsvReader:
    """Reads and parses CSV files containing WBS data."""
    
    def __init__(self, path: str):
        """
        Initialize CSV reader.
        
        Args:
            path: Path to CSV file
        """
        self.path = Path(path)
    
    def read(self) -> List[Record]:
        """
        Read and parse CSV file.
        
        Returns:
            List of Record objects
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If CSV is invalid or missing required fields
        """
        if not self.path.exists():
            raise FileNotFoundError(f"Failed to open CSV: {self.path}")
        
        with open(self.path, 'r', encoding='utf-8') as f:
            # Read header
            header_line = f.readline()
            if not header_line.strip():
                raise ValueError("Empty CSV")
            
            headers = split_csv_line(header_line.strip())
            headers_lower = [to_lower(h) for h in headers]
            
            # Find column indices
            def find_index(key: str) -> int:
                key_lower = to_lower(key)
                for i, h in enumerate(headers_lower):
                    if h == key_lower:
                        return i
                return -1
            
            # Required headers
            code_idx = find_index("code")
            title_idx = find_index("title")
            
            if code_idx < 0 or title_idx < 0:
                raise ValueError("CSV missing required headers: code, title")
            
            # Optional headers
            desc_idx = find_index("description")
            pr_idx = find_index("primaryresp")
            sr_idx = find_index("seconderyresp")
            est_idx = find_index("estimateduration")
            
            # Read data rows
            records = []
            line_num = 1  # Header is line 1
            
            for line in f:
                line_num += 1
                line = line.strip()
                if not line:
                    continue
                
                row = split_csv_line(line)
                
                def get_field(idx: int) -> str:
                    if 0 <= idx < len(row):
                        return row[idx]
                    return ""
                
                code = get_field(code_idx)
                title = get_field(title_idx)
                
                if not code or not title:
                    raise ValueError(f"Missing code/title at line {line_num}")
                
                record = Record(
                    code=code,
                    title=title,
                    description=get_field(desc_idx),
                    primaryResp=get_field(pr_idx),
                    seconderyResp=get_field(sr_idx),
                    estimateDuration=get_field(est_idx)
                )
                
                records.append(record)
            
            return records

