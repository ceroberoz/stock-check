"""Unit tests for screener scoring engine."""

import pandas as pd
import pytest

from stock_checker.screener import (
    calculate_screener_score,
    screen_stocks,
)


@pytest.fixture
def sample_hist():
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


def test_calculate_screener_score_returns_dict():
    result = calculate_screener_score(
        ticker="TEST",
        last_price=100.0,
        mas={"MA5": 95, "MA20": 90},
    )
    assert "score" in result
    assert "signal" in result
    assert "components" in result
    assert 0 <= result["score"] <= 100


def test_calculate_screener_score_with_all_indicators(sample_hist):
    result = calculate_screener_score(
        ticker="TEST",
        last_price=100.0,
        mas={"MA5": 95, "MA20": 90, "MA50": 85},
        rsi=55.0,
        macd={"macd": 5.0, "signal": 3.0, "histogram": 2.0},
        volume_metrics={"volume_ratio": 1.5},
        hist=sample_hist,
    )
    assert result["score"] > 0
    assert result["signal"] in ("STRONG BUY", "BUY", "WATCH", "AVOID", "EXIT")


def test_screen_stocks_sorts_by_score():
    stocks = [
        {"ticker": "A", "last_price": 100, "mas": {"MA5": 90}},
        {"ticker": "B", "last_price": 100, "mas": {"MA5": 95}},
    ]
    results = screen_stocks(stocks)
    assert len(results) == 2
    assert results[0]["score"] >= results[1]["score"]


def test_screen_stocks_enriches_with_score():
    stocks = [{"ticker": "TEST", "last_price": 100, "mas": {}}]
    results = screen_stocks(stocks)
    assert "score" in results[0]
    assert "signal" in results[0]
