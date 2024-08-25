from enum import Enum
from .common import BaseDef


class RelationshipType(str, Enum):
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_ONE = "MANY_TO_ONE"
    MANY_TO_MANY = "MANY_TO_MANY"


class RelationshipDef(BaseDef):
    relationship_type: RelationshipType
    from_table: str
    from_column: str
    to_table: str
    to_column: str
