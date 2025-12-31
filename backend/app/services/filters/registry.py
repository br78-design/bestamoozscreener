from typing import Any, Dict, List, Type

from app.schemas.filters import FilterDefinition
from app.services.filters.base import FilterBase
from app.services.filters.macd_positive import MacdAboveZeroFilter
from app.services.filters.smart_money import SmartMoneyInflowFilter
from app.services.filters.volume_spike import VolumeAboveAverageFilter

AVAILABLE_FILTERS: Dict[str, Type[FilterBase]] = {
    SmartMoneyInflowFilter.id: SmartMoneyInflowFilter,
    MacdAboveZeroFilter.id: MacdAboveZeroFilter,
    VolumeAboveAverageFilter.id: VolumeAboveAverageFilter,
}


def get_filter_definitions() -> List[FilterDefinition]:
    return [cls.definition() for cls in AVAILABLE_FILTERS.values()]


def instantiate_filter(filter_id: str, params: Dict[str, Any]) -> FilterBase:
    if filter_id not in AVAILABLE_FILTERS:
        raise ValueError(f"Unknown filter id: {filter_id}")
    return AVAILABLE_FILTERS[filter_id](**params)
