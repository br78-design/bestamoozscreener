import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from app.core.config import get_settings
from app.services.cache.cache import TTLCache
from app.services.data_providers.base import MarketDataProvider


class TsetmcMarketDataProvider(MarketDataProvider):
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.tsetmc_base_url.rstrip("/")
        self.api_prefix = settings.tsetmc_api_prefix.rstrip("/")
        self.max_symbols = settings.tsetmc_max_symbols
        self.instrument_cache = TTLCache(settings.cache_ttl_seconds)
        self.snapshot_cache = TTLCache(settings.cache_ttl_seconds)
        self.history_cache = TTLCache(settings.cache_ttl_seconds)

    def _build_url(self, path: str, with_prefix: bool) -> str:
        path = path.lstrip("/")
        if with_prefix and self.api_prefix:
            if self.base_url.endswith(self.api_prefix):
                return f"{self.base_url}/{path}"
            return f"{self.base_url}{self.api_prefix}/{path}"
        return f"{self.base_url}/{path}"

    def _fetch_json(self, path: str) -> Any:
        urls = [
            self._build_url(path, with_prefix=True),
            self._build_url(path, with_prefix=False),
        ]
        seen = set()
        for url in urls:
            if url in seen:
                continue
            seen.add(url)
            request = Request(
                url,
                headers={
                    "User-Agent": "bestamoozscreener/1.0",
                    "Accept": "application/json",
                },
            )
            try:
                with urlopen(request, timeout=15) as response:
                    payload = response.read().decode("utf-8")
                return json.loads(payload)
            except HTTPError as exc:
                if exc.code != 404:
                    raise
        raise HTTPError(urls[-1], 404, "Not Found", hdrs=None, fp=None)

    def _extract_list(self, data: Any) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in (
                "instrumentList",
                "instrumentlist",
                "closingPriceDaily",
                "closingPriceDailyList",
                "data",
                "result",
            ):
                value = data.get(key)
                if isinstance(value, list):
                    return value
            for value in data.values():
                if isinstance(value, list) and value and isinstance(value[0], dict):
                    return value
        return []

    def _parse_symbol_entry(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        ins_code = item.get("insCode") or item.get("instrumentId") or item.get("ins_code")
        symbol = item.get("symbol") or item.get("lVal18AFC") or item.get("lVal18aFC")
        company_name = item.get("company_name") or item.get("lVal30") or item.get("lVal30Name")
        if not ins_code or not symbol:
            return None
        return {
            "ins_code": str(ins_code),
            "symbol": str(symbol).strip(),
            "company_name": str(company_name or symbol).strip(),
        }

    def _get_instruments(self) -> List[Dict[str, Any]]:
        cached = self.instrument_cache.get("instruments")
        if cached:
            return cached
        data = None
        for path in (
            "Instrument/GetInstrumentList/0",
            "Instrument/GetInstrumentList",
            "Instrument/GetInstrumentList/1",
        ):
            try:
                data = self._fetch_json(path)
                break
            except HTTPError:
                continue
        if data is None:
            raise HTTPError("Instrument/GetInstrumentList/0", 404, "Not Found", hdrs=None, fp=None)
        items = self._extract_list(data)
        instruments = []
        for item in items:
            parsed = self._parse_symbol_entry(item)
            if parsed:
                instruments.append(parsed)
            if len(instruments) >= self.max_symbols:
                break
        self.instrument_cache.set("instruments", instruments)
        return instruments

    def _parse_date(self, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, int):
            text = str(value)
        elif isinstance(value, str):
            text = value.strip()
        else:
            return datetime.utcnow()
        if len(text) == 8 and text.isdigit():
            return datetime.strptime(text, "%Y%m%d")
        try:
            return datetime.fromisoformat(text)
        except ValueError:
            return datetime.utcnow()

    def _parse_history(self, items: List[Dict[str, Any]], lookback: int) -> List[Dict[str, Any]]:
        history = []
        for item in items[-lookback:]:
            close = (
                item.get("pClosing")
                or item.get("close")
                or item.get("closingPrice")
                or item.get("pDrCotVal")
            )
            if close is None:
                continue
            volume = item.get("qTotTran5J") or item.get("volume") or 0
            trade_value = item.get("qTotCap") or item.get("trade_value")
            trade_value = trade_value if trade_value is not None else float(close) * float(volume)
            history.append(
                {
                    "date": self._parse_date(item.get("dEven") or item.get("date")).isoformat(),
                    "close": float(close),
                    "volume": float(volume),
                    "trade_value": float(trade_value),
                }
            )
        return history

    def list_symbols(self) -> List[Dict[str, Any]]:
        try:
            instruments = self._get_instruments()
        except Exception:
            return []
        return [
            {
                "symbol": item["symbol"],
                "company_name": item["company_name"],
            }
            for item in instruments
        ]

    def _resolve_ins_code(self, symbol: str) -> Optional[str]:
        instruments = self._get_instruments()
        for item in instruments:
            if item["symbol"] == symbol:
                return item["ins_code"]
        return None

    def get_snapshot(self, symbol: str) -> Dict[str, Any]:
        cached = self.snapshot_cache.get(symbol)
        if cached:
            return cached
        ins_code = self._resolve_ins_code(symbol)
        if not ins_code:
            raise ValueError(f"Symbol not found: {symbol}")
        history = self.get_history(symbol, lookback=5)
        if not history:
            raise ValueError(f"No history for symbol: {symbol}")
        last = history[-1]
        prev = history[-2] if len(history) > 1 else last
        percent_change = (
            (last["close"] - prev["close"]) / prev["close"] * 100
            if prev["close"]
            else 0
        )
        snapshot = {
            "symbol": symbol,
            "company_name": next(
                (item["company_name"] for item in self._get_instruments() if item["symbol"] == symbol),
                symbol,
            ),
            "last_price": last["close"],
            "volume": last["volume"],
            "trade_value": last["trade_value"],
            "percent_change": round(percent_change, 2),
            "last_updated": datetime.fromisoformat(last["date"]),
            "ins_code": ins_code,
        }
        self.snapshot_cache.set(symbol, snapshot)
        return snapshot

    def get_history(self, symbol: str, lookback: int = 60) -> List[Dict[str, Any]]:
        cache_key = f"{symbol}:{lookback}"
        cached = self.history_cache.get(cache_key)
        if cached:
            return cached
        ins_code = self._resolve_ins_code(symbol)
        if not ins_code:
            raise ValueError(f"Symbol not found: {symbol}")
        data = self._fetch_json(f"ClosingPrice/GetClosingPriceDailyList/{ins_code}/0")
        items = self._extract_list(data)
        history = self._parse_history(items, lookback)
        self.history_cache.set(cache_key, history)
        return history
