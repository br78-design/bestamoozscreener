from functools import lru_cache

from app.services.data_providers.base import MarketDataProvider
from app.services.data_providers.mock_provider import MockMarketDataProvider


@lru_cache()
def get_provider() -> MarketDataProvider:
    return MockMarketDataProvider()
