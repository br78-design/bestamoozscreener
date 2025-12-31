from typing import List
from pydantic import BaseModel, Field

from app.schemas.filters import SelectedFilter


class ScreenerRunRequest(BaseModel):
    filters: List[SelectedFilter] = Field(default_factory=list)
