from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase
from app.services.indicators import sma


class PriceAboveSmaFilter(FilterBase):
    id = "price_above_sma"
    name = "قیمت بالای میانگین ساده"
    description = "قیمت پایانی بالاتر از SMA باشد"
    parameters = {
        "window": FilterParameter(
            name="window",
            type="int",
            description="دوره میانگین ساده",
            default=20,
        )
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        window = int(self.params.get("window", 20))
        closes = [item["close"] for item in symbol_data.get("history", [])]
        if len(closes) < window:
            return {"passed": False, "reason": "داده کافی برای SMA موجود نیست"}
        last_close = closes[-1]
        sma_values = sma(closes, window=window)
        last_sma = sma_values[-1]
        passed = last_close > last_sma
        reason = f"قیمت {last_close:.2f} و SMA{window} برابر {last_sma:.2f}"
        return {"passed": passed, "reason": reason}
