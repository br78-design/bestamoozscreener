from functools import lru_cache

from app.core.config import get_settings
from app.services.data_providers.base import MarketDataProvider
from app.services.data_providers.mock_provider import MockMarketDataProvider
from app.services.data_providers.tsetmc_provider import TsetmcMarketDataProvider


@lru_cache()
def get_provider() -> MarketDataProvider:
    settings = get_settings()
    provider_name = settings.data_provider.lower()
    if provider_name == "mock":
        return MockMarketDataProvider()
    if provider_name == "tsetmc":
        return TsetmcMarketDataProvider()
    raise ValueError(f"Unknown data provider: {settings.data_provider}")
