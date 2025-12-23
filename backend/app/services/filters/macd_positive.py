from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase
from app.services.indicators import macd


class MacdAboveZeroFilter(FilterBase):
    id = "macd_above_zero"
    name = "MACD بالای صفر"
    description = "آخرین مقدار MACD خط اصلی بالای صفر باشد"
    parameters = {
        "fast": FilterParameter(
            name="fast",
            type="int",
            description="دوره EMA سریع",
            default=12,
        ),
        "slow": FilterParameter(
            name="slow",
            type="int",
            description="دوره EMA کند",
            default=26,
        ),
        "signal": FilterParameter(
            name="signal",
            type="int",
            description="دوره خط سیگنال",
            default=9,
        ),
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        fast = int(self.params.get("fast", 12))
        slow = int(self.params.get("slow", 26))
        signal = int(self.params.get("signal", 9))
        closes = [item["close"] for item in symbol_data.get("history", [])]
        if len(closes) < slow:
            return {"passed": False, "reason": "داده کافی برای MACD موجود نیست"}

        macd_values = macd(closes, fast=fast, slow=slow, signal=signal)
        last_macd = macd_values["macd_line"][-1]
        passed = last_macd > 0
        reason = f"MACD آخرین کندل {last_macd:.2f} است"
        return {"passed": passed, "reason": reason}
