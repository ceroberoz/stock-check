"""Unit tests for scanner module."""

import pandas as pd
import pytest

from stock_checker.scanner import ScanResult, scan_stock, scan_stocks


@pytest.fixture
def mock_fetch(monkeypatch):
    """Mock fetch_stock_data to return test data."""
    dates = pd.date_range("2026-01-01", periods=60, freq="D")
    close = [100 + i * 0.5 for i in range(60)]
    hist = pd.DataFrame(
        {
            "Open": [c - 0.5 for c in close],
            "High": [c + 1.0 for c in close],
            "Low": [c - 1.0 for c in close],
            "Close": close,
            "Volume": [1_000_000] * 60,
        },
        index=dates,
    )

    def fake_fetch(symbol, days=1, interval="1d", exchange="IDX"):
        return {
            "ticker": f"{symbol}.JK",
            "last_price": 100.0,
            "change": 5.0,
            "change_pct": 5.0,
            "open": 95.0,
            "high": 105.0,
            "low": 90.0,
            "close": 100.0,
            "period": "1 trading day",
            "_hist": hist,
        }

    monkeypatch.setattr("stock_checker.scanner.fetch_stock_data", fake_fetch)


def test_scan_stock_returns_result(mock_fetch):
    result = scan_stock("BBCA")
    assert result is not None
    assert isinstance(result, ScanResult)
    assert result.ticker == "BBCA.JK"
    assert result.last_price == 100.0


def test_scan_stock_includes_indicators(mock_fetch):
    result = scan_stock("BBCA")
    assert result.mas is not None
    assert result.signal_label in ("STRONG BUY", "BUY", "NEUTRAL", "SELL", "STRONG SELL")


def test_scan_stock_with_score(mock_fetch):
    result = scan_stock("BBCA", include_score=True)
    assert result is not None
    assert result.score > 0
    assert result.score_label != ""


def test_scan_stock_error_returns_none(monkeypatch):
    def failing_fetch(*args, **kwargs):
        raise ValueError("No data")

    monkeypatch.setattr("stock_checker.scanner.fetch_stock_data", failing_fetch)
    result = scan_stock("INVALID")
    assert result is None


def test_scan_stocks_filters_by_price(mock_fetch):
    results = scan_stocks(["BBCA", "BBRI"], min_price=200)
    assert len(results) == 0


def test_scan_stocks_with_progress_callback(mock_fetch):
    progress_calls = []

    def on_progress(symbol, current, total):
        progress_calls.append((symbol, current, total))

    results = scan_stocks(["BBCA", "BBRI"], progress_callback=on_progress)
    assert len(results) == 2
    assert len(progress_calls) == 2
