from typing import Dict, List, Set
from collections import defaultdict

class SearchEngine:
    def __init__(self):
        self.index = {}
    
    def set_index(self, index: Dict[str, List[dict]]):
        """Set the search index."""
        self.index = index
    
    def _location_to_tuple(self, location: dict) -> tuple:
        """Convert location dict to tuple for set operations."""
        return (
            location['directory'],
            location['file'],
            location['line_number'],
            location['line_text']
        )
    
    def _tuple_to_location(self, location_tuple: tuple) -> dict:
        """Convert location tuple back to dict."""
        return {
            'directory': location_tuple[0],
            'file': location_tuple[1],
            'line_number': location_tuple[2],
            'line_text': location_tuple[3]
        }
    
    def find_matches(self, terms: List[str], locations: Set[tuple]) -> Set[tuple]:
        """Find locations that contain all given terms."""
        if not terms:
            return locations
        
        matches = set()
        for term in terms:
            if term not in self.index:
                return set()  # If any required term is missing, no matches
            term_locations = {self._location_to_tuple(loc) for loc in self.index[term]}
            
            if not matches:
                matches = term_locations
            else:
                matches &= term_locations
        
        return matches
    
    def find_or_group_matches(self, or_group: List[str], locations: Set[tuple]) -> Set[tuple]:
        """Find locations that contain any of the OR group terms."""
        if not or_group:
            return locations
        
        matches = set()
        for term in or_group:
            if term in self.index:
                matches.update(self._location_to_tuple(loc) for loc in self.index[term])
        
        if locations:
            matches &= locations
        return matches
    
    def count_optional_matches(self, location_tuple: tuple, optional_terms: List[str]) -> int:
        """Count how many optional terms match for a given location."""
        count = 0
        line_text = location_tuple[3].lower()  # line_text is at index 3
        for term in optional_terms:
            if term in line_text:
                count += 1
        return count
    
    def count_or_group_matches(self, location_tuple: tuple, or_groups: List[List[str]]) -> List[int]:
        """Count how many terms match in each OR group."""
        line_text = location_tuple[3].lower()
        counts = []
        for group in or_groups:
            count = sum(1 for term in group if term in line_text)
            counts.append(count)
        return counts
    
    def search(self, query: Dict) -> List[dict]:
        """Search the index using the parsed query."""
        matches: Set[tuple] = set()
        
        # Start with required terms
        if query['required']:
            matches = self.find_matches(query['required'], matches)
            if not matches:
                return []
        
        # Apply OR groups
        for or_group in query['or_groups']:
            matches = self.find_or_group_matches(or_group, matches)
            if not matches:
                return []
        
        # If no required terms or OR groups, start with all locations that have any optional term
        if not matches and query['optional']:
            for term in query['optional']:
                if term in self.index:
                    matches.update(self._location_to_tuple(loc) for loc in self.index[term])
        
        # Convert matches to list for sorting
        results = list(matches)
        
        # Sort results by both optional matches and OR group matches
        scored_results = []
        for loc in results:
            # Count optional matches
            opt_count = self.count_optional_matches(loc, query['optional'])
            # Count OR group matches
            or_counts = self.count_or_group_matches(loc, query['or_groups'])
            # Create a tuple for sorting: (location, optional_count, or_group_counts)
            scored_results.append((loc, opt_count, or_counts))
        
        # Sort by optional matches and then by OR group matches
        scored_results.sort(key=lambda x: (x[1], sum(x[2])), reverse=True)
        
        # Extract just the location tuples in sorted order
        results = [loc for loc, _, _ in scored_results]
        
        # Convert back to dictionaries for output
        return [self._tuple_to_location(loc_tuple) for loc_tuple in results]