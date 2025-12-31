import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from app.core.config import get_settings
from app.services.cache.cache import TTLCache
from app.services.data_providers.base import MarketDataProvider


class MockMarketDataProvider(MarketDataProvider):
    def __init__(self) -> None:
        settings = get_settings()
        self.data_file = Path(settings.mock_data_file)
        self.snapshot_cache = TTLCache(settings.cache_ttl_seconds)
        self.history_cache = TTLCache(settings.cache_ttl_seconds)
        self._data = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        if not self.data_file.exists():
            raise FileNotFoundError(f"Mock data file missing: {self.data_file}")
        with self.data_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def list_symbols(self) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": item["symbol"],
                "company_name": item["company_name"],
                "last_price": item["last_price"],
                "volume": item["volume"],
                "trade_value": item["trade_value"],
                "percent_change": item["percent_change"],
                "last_updated": datetime.fromisoformat(item["last_updated"]),
            }
            for item in self._data
        ]

    def get_snapshot(self, symbol: str) -> Dict[str, Any]:
        cached = self.snapshot_cache.get(symbol)
        if cached:
            return cached
        match = next((item for item in self._data if item["symbol"] == symbol), None)
        if not match:
            raise ValueError(f"Symbol not found: {symbol}")
        snapshot = {
            "symbol": match["symbol"],
            "company_name": match["company_name"],
            "last_price": match["last_price"],
            "volume": match["volume"],
            "trade_value": match["trade_value"],
            "percent_change": match["percent_change"],
            "last_updated": datetime.fromisoformat(match["last_updated"]),
        }
        self.snapshot_cache.set(symbol, snapshot)
        return snapshot

    def get_history(self, symbol: str, lookback: int = 60) -> List[Dict[str, Any]]:
        cache_key = f"{symbol}:{lookback}"
        cached = self.history_cache.get(cache_key)
        if cached:
            return cached
        match = next((item for item in self._data if item["symbol"] == symbol), None)
        if not match:
            raise ValueError(f"Symbol not found: {symbol}")
        history = match.get("history", [])[-lookback:]
        self.history_cache.set(cache_key, history)
        return history
