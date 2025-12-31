from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase


class PercentChangeBelowFilter(FilterBase):
    id = "percent_change_below"
    name = "درصد تغییر منفی"
    description = "درصد تغییر نماد پایین‌تر از آستانه باشد"
    parameters = {
        "threshold": FilterParameter(
            name="threshold",
            type="float",
            description="حداکثر درصد تغییر",
            default=-2.5,
        )
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        threshold = float(self.params.get("threshold", -2.5))
        percent_change = float(symbol_data.get("percent_change", 0))
        passed = percent_change <= threshold
        reason = f"درصد تغییر {percent_change:.2f}% کمتر/برابر {threshold:.2f}%"
        return {"passed": passed, "reason": reason}
