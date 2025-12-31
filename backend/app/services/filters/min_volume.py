from typing import Any, Dict, Optional

from app.schemas.filters import FilterParameter
from app.services.filters.base import FilterBase


class MinimumVolumeFilter(FilterBase):
    id = "min_volume"
    name = "حداقل حجم معاملات"
    description = "حجم معاملات بالاتر از مقدار حداقل باشد"
    parameters = {
        "min_volume": FilterParameter(
            name="min_volume",
            type="int",
            description="حداقل حجم",
            default=1_000_000,
        )
    }

    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        min_volume = int(self.params.get("min_volume", 1_000_000))
        volume = int(symbol_data.get("volume", 0))
        passed = volume >= min_volume
        reason = f"حجم {volume:,} و حداقل {min_volume:,}"
        return {"passed": passed, "reason": reason}
