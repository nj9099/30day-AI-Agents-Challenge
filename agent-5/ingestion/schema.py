from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

class DocumemtModel(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid4()))
    document_name: str
    content: str
    metadata: dict[str, Any] = Field(default=dict)
