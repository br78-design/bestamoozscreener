from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase


class SmartMoneyInflowFilter(FilterBase):
    id = "smart_money_inflow"
    name = "ورود پول هوشمند"
    description = (
        "حجم و ارزش معاملات امروز نسبت به میانگین دوره اخیر رشد معنادار داشته باشد."
    )
    parameters = {
        "lookback_days": FilterParameter(
            name="lookback_days",
            type="int",
            description="تعداد روز برای محاسبه میانگین ارزش معاملات",
            default=20,
        ),
        "threshold": FilterParameter(
            name="threshold",
            type="float",
            description="حداقل نسبت ارزش معاملات امروز به میانگین",
            default=2.0,
        ),
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        lookback = int(self.params.get("lookback_days", 20))
        threshold = float(self.params.get("threshold", 2.0))
        history = symbol_data.get("history", [])
        if len(history) < lookback:
            return {"passed": False, "reason": "داده تاریخی کافی نیست"}

        values = [h["close"] * h.get("volume", 0) for h in history[-lookback:]]
        avg_value = sum(values) / lookback if values else 0
        today_value = symbol_data.get("trade_value") or (
            symbol_data.get("last_price", 0) * symbol_data.get("volume", 0)
        )
        if avg_value == 0:
            return {"passed": False, "reason": "میانگین ارزش معاملات صفر است"}

        ratio = today_value / avg_value
        passed = ratio >= threshold
        reason = (
            f"نسبت ارزش معاملات امروز به میانگین {ratio:.2f} است (حداقل {threshold})"
        )
        return {"passed": passed, "reason": reason}
