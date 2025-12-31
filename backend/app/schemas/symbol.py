from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SymbolResponse(BaseModel):
    symbol: str
    company_name: str


class ScreenerResult(BaseModel):
    symbol: str
    company_name: str
    last_price: float
    volume: float
    trade_value: float
    percent_change: float
    last_updated: datetime
    reason: str
    score: Optional[float] = None
