import time
from typing import Any, Dict, Tuple


class TTLCache:
    def __init__(self, ttl_seconds: int = 60):
        self.ttl_seconds = ttl_seconds
        self.store: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str) -> Any:
        record = self.store.get(key)
        if not record:
            return None
        timestamp, value = record
        if time.time() - timestamp > self.ttl_seconds:
            self.store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self.store[key] = (time.time(), value)

    def clear(self) -> None:
        self.store.clear()
