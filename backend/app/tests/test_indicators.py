from app.services.indicators import sma, ema, macd


def test_sma_basic():
    values = [1, 2, 3, 4]
    result = sma(values, 2)
    assert result == [float("nan"), 1.5, 2.5, 3.5]


def test_ema_monotonic():
    values = [1, 1, 1]
    result = ema(values, 2)
    assert len(result) == len(values)
    assert all(abs(v - 1) < 1e-6 for v in result)


def test_macd_above_zero():
    values = [i for i in range(1, 60)]
    macd_result = macd(values)
    assert len(macd_result["macd_line"]) == len(values)
    assert macd_result["macd_line"][-1] > 0
