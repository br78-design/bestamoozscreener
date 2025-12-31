from typing import List

from fastapi import APIRouter, Depends, Query

from app.deps import get_provider
from app.schemas.symbol import SymbolResponse
from app.services.data_providers.base import MarketDataProvider

router = APIRouter(prefix="/api/symbols", tags=["symbols"])


@router.get("", response_model=List[SymbolResponse])
def list_symbols(
    search: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    provider: MarketDataProvider = Depends(get_provider),
):
    items = provider.list_symbols()
    if search:
        search_lower = search.lower()
        items = [
            item
            for item in items
            if search_lower in item["symbol"].lower()
            or search_lower in item.get("company_name", "").lower()
        ]
    offset = (page - 1) * page_size
    return items[offset : offset + page_size]
