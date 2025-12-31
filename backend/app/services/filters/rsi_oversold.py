from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase
from app.services.indicators import rsi


class RsiOversoldFilter(FilterBase):
    id = "rsi_oversold"
    name = "اشباع فروش RSI"
    description = "RSI پایین‌تر از آستانه باشد"
    parameters = {
        "window": FilterParameter(
            name="window",
            type="int",
            description="دوره RSI",
            default=14,
        ),
        "threshold": FilterParameter(
            name="threshold",
            type="float",
            description="آستانه RSI",
            default=30,
        ),
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        window = int(self.params.get("window", 14))
        threshold = float(self.params.get("threshold", 30))
        closes = [item["close"] for item in symbol_data.get("history", [])]
        if len(closes) < window + 1:
            return {"passed": False, "reason": "داده کافی برای RSI موجود نیست"}
        rsi_values = rsi(closes, window=window)
        last_rsi = rsi_values[-1]
        passed = last_rsi <= threshold
        reason = f"RSI آخرین کندل {last_rsi:.2f} و آستانه {threshold:.2f}"
        return {"passed": passed, "reason": reason}
