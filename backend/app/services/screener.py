from typing import Any, Dict, List

from app.services.data_providers.base import MarketDataProvider
from app.services.filters.registry import instantiate_filter


def run_screener(
    provider: MarketDataProvider, filters: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    symbols = provider.list_symbols()
    results = []

    for symbol in symbols:
        symbol_id = symbol["symbol"]
        try:
            snapshot = provider.get_snapshot(symbol_id)
            history = provider.get_history(symbol_id, lookback=120)
        except Exception:
            continue
        symbol_data = {**snapshot, "history": history}

        passed_all = True
        reasons = []
        score = None

        for f in filters:
            instance = instantiate_filter(f["id"], f.get("params", {}))
            evaluation = instance.evaluate(symbol_data)
            if not evaluation.get("passed"):
                passed_all = False
                reasons.append(evaluation.get("reason") or "رد شده")
                break
            reasons.append(evaluation.get("reason") or "قبول")
            if evaluation.get("score") is not None:
                score = evaluation.get("score")

        if passed_all:
            results.append(
                {
                    **snapshot,
                    "reason": " و ".join(reasons),
                    "score": score,
                }
            )

    return results
