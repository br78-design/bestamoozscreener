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


def rsi(values: List[float], window: int = 14) -> List[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    if len(values) < window + 1:
        raise ValueError("Not enough data for RSI calculation")
    gains = []
    losses = []
    for i in range(1, len(values)):
        delta = values[i] - values[i - 1]
        gains.append(max(delta, 0))
        losses.append(abs(min(delta, 0)))
    avg_gain = sum(gains[:window]) / window
    avg_loss = sum(losses[:window]) / window
    rs_values = []
    rsi_values = [float("nan")] * window
    for i in range(window, len(gains)):
        if i > window:
            avg_gain = (avg_gain * (window - 1) + gains[i]) / window
            avg_loss = (avg_loss * (window - 1) + losses[i]) / window
        rs = avg_gain / avg_loss if avg_loss != 0 else float("inf")
        rs_values.append(rs)
        rsi_values.append(100 - (100 / (1 + rs)))
    return rsi_values
