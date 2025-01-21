#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from indexer import FileIndexer
from query_parser import QueryParser
from search_engine import SearchEngine

def main():
    parser = argparse.ArgumentParser(description='In-memory file search engine')
    parser.add_argument('--dir', required=True, help='Directory to search in')
    args = parser.parse_args()
    
    search_dir = Path(args.dir)
    if not search_dir.is_dir():
        print(f"Error: {args.dir} is not a valid directory", file=sys.stderr)
        sys.exit(1)
    
    # Initialize components
    indexer = FileIndexer()
    search_engine = SearchEngine()
    query_parser = QueryParser()
    
    # Build index
    print(f"Indexing files in {search_dir}...")
    index = indexer.build_index(search_dir)
    search_engine.set_index(index)
    print("Indexing complete. Ready for queries.")
    print("Enter queries in the format: word +required +(either or) optional")
    
    # Query loop
    while True:
        try:
            query = input("> ").strip()
            if not query:
                continue
                
            if query.lower() == 'exit':
                break
                
            parsed_query = query_parser.parse(query)
            results = search_engine.search(parsed_query)
            
            if not results:
                print("No matches found.")
                continue
                
            for result in results:
                print(f"{result['file']} {result['line_number']} \"{result['line_text']}\"")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
    
    print("\nGoodbye!")

if __name__ == '__main__':
    main() 