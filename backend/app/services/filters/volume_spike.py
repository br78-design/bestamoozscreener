from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase


class VolumeAboveAverageFilter(FilterBase):
    id = "volume_above_average"
    name = "حجم بالاتر از میانگین"
    description = "حجم امروز بزرگ‌تر از میانگین دوره انتخابی باشد"
    parameters = {
        "lookback": FilterParameter(
            name="lookback",
            type="int",
            description="تعداد روز برای میانگین حجم",
            default=20,
        ),
        "multiplier": FilterParameter(
            name="multiplier",
            type="float",
            description="ضریب مقایسه حجم امروز با میانگین",
            default=1.5,
        ),
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        lookback = int(self.params.get("lookback", 20))
        multiplier = float(self.params.get("multiplier", 1.5))
        history = symbol_data.get("history", [])
        if len(history) < lookback:
            return {"passed": False, "reason": "تعداد کندل کافی نیست"}

        volumes = [h.get("volume", 0) for h in history[-lookback:]]
        avg_volume = sum(volumes) / lookback if volumes else 0
        today_volume = symbol_data.get("volume", 0)
        if avg_volume == 0:
            return {"passed": False, "reason": "میانگین حجم صفر است"}

        passed = today_volume > avg_volume * multiplier
        reason = (
            f"حجم امروز {today_volume:.0f} در مقابل میانگین {avg_volume:.0f} با ضریب {multiplier}"
        )
        return {"passed": passed, "reason": reason}
