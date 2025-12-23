from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from app.schemas.filters import FilterDefinition, FilterParameter


class FilterBase(ABC):
    id: str
    name: str
    description: str
    parameters: Dict[str, FilterParameter]

    def __init__(self, **params: Any) -> None:
        self.params = params

    @classmethod
    def definition(cls) -> FilterDefinition:
        return FilterDefinition(
            id=cls.id,
            name=cls.name,
            description=cls.description,
            parameters=list(cls.parameters.values()),
        )

    @abstractmethod
    def evaluate(self, symbol_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """
        Evaluate the filter against symbol data.

        Returns a dict with keys: passed (bool), reason (str), score (optional float)
        """
        raise NotImplementedError
