from pydantic import BaseModel
from typing import List, Optional


class BaseDef(BaseModel):
    name: str
    version: int = 0
    description: Optional[str] = ""
    tags: Optional[List[str]] = []

    created_by: Optional[str] = ""
    created_at: Optional[str] = ""

    updated_by: Optional[str] = ""
    updated_at: Optional[str] = ""

