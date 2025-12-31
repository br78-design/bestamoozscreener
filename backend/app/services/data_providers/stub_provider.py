from typing import Any, Dict, List

from app.services.data_providers.base import MarketDataProvider


class RealMarketDataAdapter(MarketDataProvider):
    """
    Skeleton adapter for integrating with real Tehran Stock Exchange data providers.

    Implementations could leverage REST endpoints or vendor SDKs. Replace the method
    bodies with concrete calls to your provider of choice, then wire the dependency
    in app.main where the provider is instantiated.
    """

    def list_symbols(self) -> List[Dict[str, Any]]:
        # TODO: Replace with live provider implementation
        raise NotImplementedError("Real data provider not implemented yet")

    def get_snapshot(self, symbol: str) -> Dict[str, Any]:
        # TODO: Replace with live provider implementation
        raise NotImplementedError("Real data provider not implemented yet")

    def get_history(self, symbol: str, lookback: int = 60) -> List[Dict[str, Any]]:
        # TODO: Replace with live provider implementation
        raise NotImplementedError("Real data provider not implemented yet")
