from typing import List, Optional
from .column_def import ColumnDef
from .relation_def import RelationshipDef
from .common import BaseDef


class TableDef(BaseDef):
    parent_table: Optional[str] = None
    parents: Optional[List[str]] = []
    columnDefs: Optional[List[ColumnDef]] = []
    relationshipDefs: Optional[List[RelationshipDef]] = []

    def add_attribute(self, attribute: ColumnDef):
        self.columns.append(attribute)

    def add_relationship(self, relationship: RelationshipDef):
        self.relationships.append(relationship)
    
    class Config:
        arbitrary_types_allowed = True
