from pydantic import BaseModel
from typing import List
from defs.table_def import TableDef
from defs.column_def import ColumnDef
from defs.relation_def import RelationshipDef

class Defs(BaseModel):
    tableDefs: List[TableDef]
    columnDefs: List[ColumnDef]
    relationshipDefs: List[RelationshipDef] = []