import re
from pathlib import Path
from typing import Dict, List, Set

class FileIndexer:
    def __init__(self):
        self.index: Dict[str, List[dict]] = {}
        self.file_extensions: Set[str] = {'.txt', '.md', '.py', '.java', '.cpp', '.c', '.h', '.js', '.html', '.css'}
    
    def tokenize(self, text: str) -> List[str]:
        """Convert text to lowercase and split into tokens."""
        # Replace non-alphanumeric chars with spaces and split
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        return text.split()
    
    def is_text_file(self, file_path: Path) -> bool:
        """Check if file is a text file based on extension."""
        return file_path.suffix.lower() in self.file_extensions
    
    def index_file(self, file_path: Path) -> None:
        """Index a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                        
                    tokens = self.tokenize(line)
                    location = {
                        'directory': str(file_path.parent),
                        'file': str(file_path),
                        'line_number': line_number,
                        'line_text': line
                    }
                    
                    for token in tokens:
                        if token not in self.index:
                            self.index[token] = []
                        self.index[token].append(location)
                        
        except Exception as e:
            print(f"Warning: Could not read file {file_path}: {e}")
    
    def build_index(self, directory: Path) -> Dict[str, List[dict]]:
        """Build index from all text files in directory and subdirectories."""
        self.index.clear()
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and self.is_text_file(file_path):
                self.index_file(file_path)
        
        return self.index 