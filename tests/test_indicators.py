"""Unit tests for technical indicators."""

import pandas as pd
import pytest

from stock_checker.indicators import (
    calculate_macd,
    calculate_mas,
    calculate_rsi,
    calculate_volume_metrics,
    determine_signal,
)


@pytest.fixture
def sample_ohlcv():
    """Generate sample OHLCV data for testing."""
    dates = pd.date_range("2026-01-01", periods=60, freq="D")
    close = [100 + i * 0.5 for i in range(60)]
    return pd.DataFrame(
        {
            "Open": [c - 0.5 for c in close],
            "High": [c + 1.0 for c in close],
            "Low": [c - 1.0 for c in close],
            "Close": close,
            "Volume": [1_000_000] * 60,
        },
        index=dates,
    )


def test_calculate_mas_default(sample_ohlcv):
    mas = calculate_mas(sample_ohlcv, interval="1d")
    assert "MA5" in mas
    assert "MA9" in mas
    assert "MA20" in mas
    assert "MA50" in mas
    assert all(isinstance(v, float) for v in mas.values())


def test_calculate_mas_custom_periods(sample_ohlcv):
    mas = calculate_mas(sample_ohlcv, custom_periods=[5, 20, 50])
    assert "MA5" in mas
    assert "MA20" in mas
    assert "MA50" in mas
    assert len(mas) == 3


def test_calculate_mas_insufficient_data():
    short_data = pd.DataFrame({"Close": [100, 101, 102]})
    mas = calculate_mas(short_data, interval="1d")
    assert "MA5" not in mas
    assert "MA50" not in mas


def test_calculate_rsi(sample_ohlcv):
    rsi = calculate_rsi(sample_ohlcv)
    assert rsi is not None
    assert 0 <= rsi <= 100


def test_calculate_rsi_insufficient_data():
    short_data = pd.DataFrame({"Close": [100, 101]})
    rsi = calculate_rsi(short_data)
    assert rsi is None


def test_calculate_macd(sample_ohlcv):
    macd = calculate_macd(sample_ohlcv)
    assert macd is not None
    assert "macd" in macd
    assert "signal" in macd
    assert "histogram" in macd


def test_calculate_macd_insufficient_data():
    short_data = pd.DataFrame({"Close": [100] * 20})
    macd = calculate_macd(short_data)
    assert macd is None


def test_determine_signal_strong_buy():
    mas = {"MA5": 100, "MA20": 90, "MA50": 80}
    label, desc = determine_signal(110, mas)
    assert label == "STRONG BUY"
    assert "above all" in desc


def test_determine_signal_buy():
    mas = {"MA5": 100, "MA20": 90, "MA50": 80}
    label, desc = determine_signal(95, mas)
    assert label == "BUY"
    assert "above most" in desc


def test_determine_signal_strong_sell():
    mas = {"MA5": 100, "MA20": 110, "MA50": 120}
    label, desc = determine_signal(80, mas)
    assert label == "STRONG SELL"
    assert "below all" in desc


def test_determine_signal_empty_mas():
    label, desc = determine_signal(100, {})
    assert label == "NEUTRAL"
    assert "insufficient" in desc


def test_calculate_volume_metrics(sample_ohlcv):
    metrics = calculate_volume_metrics(sample_ohlcv)
    assert metrics is not None
    assert "current_volume" in metrics
    assert "avg_volume" in metrics
    assert "volume_ratio" in metrics
    assert "volume_spike" in metrics


def test_calculate_volume_metrics_insufficient_data():
    short_data = pd.DataFrame({"Volume": [100] * 5})
    metrics = calculate_volume_metrics(short_data)
    assert metrics is None
