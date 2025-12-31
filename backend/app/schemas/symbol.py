from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SymbolBase(BaseModel):
    symbol: str
    company_name: str
    last_price: float
    volume: float
    trade_value: float
    percent_change: float
    last_updated: datetime


class SymbolResponse(SymbolBase):
    id: int

    class Config:
        from_attributes = True


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
