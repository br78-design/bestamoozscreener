from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase


class MinimumTradeValueFilter(FilterBase):
    id = "min_trade_value"
    name = "حداقل ارزش معاملات"
    description = "ارزش معاملات بالاتر از مقدار حداقل باشد"
    parameters = {
        "min_value": FilterParameter(
            name="min_value",
            type="int",
            description="حداقل ارزش معاملات",
            default=50_000_000_000,
        )
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        min_value = int(self.params.get("min_value", 50_000_000_000))
        trade_value = int(symbol_data.get("trade_value", 0))
        passed = trade_value >= min_value
        reason = f"ارزش {trade_value:,} و حداقل {min_value:,}"
        return {"passed": passed, "reason": reason}
