from abc import ABC, abstractmethod
from typing import Any, Dict, List


class MarketDataProvider(ABC):
    @abstractmethod
    def list_symbols(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_snapshot(self, symbol: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_history(self, symbol: str, lookback: int = 60) -> List[Dict[str, Any]]:
        ...
