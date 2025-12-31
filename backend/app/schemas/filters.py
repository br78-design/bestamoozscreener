from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FilterParameter(BaseModel):
    name: str
    type: str
    description: str
    default: Optional[Any] = None


class FilterDefinition(BaseModel):
    id: str
    name: str
    description: str
    parameters: List[FilterParameter] = Field(default_factory=list)


class SelectedFilter(BaseModel):
    id: str
    params: Dict[str, Any] = Field(default_factory=dict)
