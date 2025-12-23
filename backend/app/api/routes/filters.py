from fastapi import APIRouter

from app.schemas.filters import FilterDefinition
from app.services.filters.registry import get_filter_definitions

router = APIRouter(prefix="/api/filters", tags=["filters"])


@router.get("", response_model=list[FilterDefinition])
def list_filters():
    return get_filter_definitions()
