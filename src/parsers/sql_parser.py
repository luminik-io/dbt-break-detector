from dataclasses import dataclass
from typing import Set, Dict
import sqlparse
from sqlparse.sql import Token, TokenList
from sqlparse.tokens import Keyword, Name, Whitespace, Punctuation

@dataclass
class SQLModel:
    columns: Set[str]
    column_types: Dict[str, str]
    dependencies: Set[str]

class SQLParser:
    def parse(self, content: str) -> SQLModel:
        """Parse SQL content and extract relevant information"""
        if not content:
            return SQLModel(set(), {}, set())
        
        # Parse SQL using sqlparse
        parsed = sqlparse.parse(content)[0]
        
        columns = set()
        column_types = {}
        dependencies = set()
        
        # Extract columns from SELECT statement
        select_found = False
        current_column = ""
        
        for token in parsed.flatten():
            if token.is_whitespace:
                continue
                
            if token.ttype is Keyword and token.value.upper() == 'SELECT':
                select_found = True
                continue
                
            if select_found and token.ttype is Keyword and token.value.upper() == 'FROM':
                select_found = False
                continue
                
            if select_found:
                if token.ttype is Name:
                    current_column = token.value
                    columns.add(current_column)
                elif token.ttype is Punctuation and token.value == ',':
                    current_column = ""
        
        return SQLModel(columns, column_types, dependencies)