from typing import Optional, Dict
from enum import Enum
from .common import BaseDef


class ColumnDef(BaseDef):
    data_type: str
    is_nullable: bool
    is_primary_key: bool
    is_unique: bool
    default_value: Optional = None
    index: bool = False
    index_name: Optional[str] = None
    index_type: Optional[str] = None
    # Check constraints
    check: bool = True
    # Constraints are a dictionary of constraints based on types, e.g. for int min or max.
    constraints: Optional[Dict[str, str]] = {}
    text_search_configs: Optional[Dict[str, str]] = {}  # Postgres specific text search configs

    is_vector_index: bool = False
    vector_index_dimension: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True
