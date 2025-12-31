from app.services.filters.volume_spike import VolumeAboveAverageFilter


def test_volume_filter_pass():
    history = [{"volume": 1000} for _ in range(20)]
    symbol_data = {"volume": 2000, "history": history}
    f = VolumeAboveAverageFilter(multiplier=1.5, lookback=20)
    result = f.evaluate(symbol_data)
    assert result["passed"] is True


def test_volume_filter_fail_on_data():
    history = [{"volume": 1000} for _ in range(10)]
    symbol_data = {"volume": 2000, "history": history}
    f = VolumeAboveAverageFilter(multiplier=1.5, lookback=20)
    result = f.evaluate(symbol_data)
    assert result["passed"] is False
