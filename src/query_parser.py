from typing import Dict, List, Set
import re

class QueryParser:
    def __init__(self):
        self.or_group_pattern = re.compile(r'\+\((.*?)\)')
    
    def parse(self, query: str) -> Dict:
        """Parse a query string into required, optional, and OR-group terms."""
        terms = query.strip().split()
        required = []
        optional = []
        or_groups = []
        
        i = 0
        while i < len(terms):
            term = terms[i]
            
            # Handle OR groups: +(word1 word2)
            if term.startswith('+('):
                # Find the closing parenthesis
                group_text = ''
                while i < len(terms) and ')' not in terms[i]:
                    group_text += ' ' + terms[i]
                    i += 1
                if i < len(terms):
                    group_text += ' ' + terms[i]
                
                match = self.or_group_pattern.match(group_text.strip())
                if match:
                    or_terms = match.group(1).split()
                    or_groups.append(or_terms)
            
            # Handle required terms: +word
            elif term.startswith('+'):
                required.append(term[1:].lower())
            
            # Handle optional terms
            else:
                optional.append(term.lower())
            
            i += 1
        
        return {
            'required': required,
            'optional': optional,
            'or_groups': or_groups
        } 