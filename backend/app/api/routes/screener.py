from fastapi import APIRouter, Depends

from app.deps import get_provider
from app.schemas.screener import ScreenerRunRequest
from app.services.data_providers.base import MarketDataProvider
from app.services.screener import run_screener

router = APIRouter(prefix="/api/screener", tags=["screener"])


@router.post("/run")
def run_screen(
    payload: ScreenerRunRequest,
    provider: MarketDataProvider = Depends(get_provider),
):
    filters = [{"id": f.id, "params": f.params} for f in payload.filters]
    return run_screener(provider, filters)
