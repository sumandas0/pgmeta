import os
import json
from typing import List
from defs.defs import Defs
from parsers.generate_ddl import generate_create_table_statement, generate_relation_statement

def read_definitions(directory: str) -> List[Defs]:
    all_definitions = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r") as file:
                data = json.load(file)
                defs = Defs(**data)
                all_definitions[filename[:-5]] = defs
                
    return all_definitions

def generate_sql_statements(all_defs: dict[str, Defs]) -> dict[str, str]:
    statements = {}
    
    for defs in all_defs:
        for table_def in defs.tableDefs:
            statements[table_def.name] = generate_create_table_statement(table_def)

        for relationship_def in defs.relationshipDefs:
            statements[relationship_def.name] = generate_relation_statement(relationship_def)
            
    return statements
        

