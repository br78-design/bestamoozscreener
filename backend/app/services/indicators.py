from typing import List


def sma(values: List[float], window: int) -> List[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    result = []
    for i in range(len(values)):
        if i + 1 < window:
            result.append(float("nan"))
        else:
            window_values = values[i + 1 - window : i + 1]
            result.append(sum(window_values) / window)
    return result


def ema(values: List[float], window: int) -> List[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    result = []
    multiplier = 2 / (window + 1)
    ema_prev = None
    for price in values:
        if ema_prev is None:
            ema_prev = price
        else:
            ema_prev = (price - ema_prev) * multiplier + ema_prev
        result.append(ema_prev)
    return result


def macd(values: List[float], fast: int = 12, slow: int = 26, signal: int = 9):
    if len(values) < slow:
        raise ValueError("Not enough data for MACD calculation")
    slow_ema = ema(values, slow)
    fast_ema = ema(values, fast)
    macd_line = [f - s for f, s in zip(fast_ema, slow_ema)]
    signal_line = ema(macd_line, signal)
    histogram = [m - s for m, s in zip(macd_line, signal_line)]
    return {
        "macd_line": macd_line,
        "signal_line": signal_line,
        "histogram": histogram,
    }
