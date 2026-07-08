"""Technical indicators — moving averages and trend signals."""

import pandas as pd

# Window → display-label mapping (for daily interval)
MA_WINDOWS: dict[str, int] = {
    "MA5": 5,
    "MA9": 9,
    "MA20": 20,
}

# Human-readable period labels keyed by MA name
MA_PERIOD_LABELS: dict[str, str] = {
    "MA5": "1w",
    "MA9": "2w",
    "MA20": "1m",
}


def calculate_mas(hist: pd.DataFrame) -> dict[str, float]:
    """Calculate rolling moving averages from OHLCV *hist*.

    Returns a dict like ``{"MA5": 10050.0, "MA9": 9980.0}``, only including
    windows that have enough data.
    """
    close = hist["Close"]
    mas: dict[str, float] = {}
    for label, window in MA_WINDOWS.items():
        if len(close) >= window:
            mas[label] = round(close.rolling(window=window).mean().iloc[-1], 2)
    return mas


def determine_signal(
    last_price: float, mas: dict[str, float]
) -> tuple[str, str]:
    """Determine a trend signal based on price position vs moving averages.

    Returns ``(label, description)``, e.g. ``("STRONG BUY", "price above all MAs")``.
    """
    if not mas:
        return "NEUTRAL", "insufficient data for MA analysis"

    above = sum(1 for ma in mas.values() if last_price >= ma)
    total = len(mas)

    if above == total:
        return "STRONG BUY", "price above all MAs"
    if above >= total * 2 / 3:
        return "BUY", "price above most MAs"
    if above > total / 3:
        return "SELL", "price below most MAs"
    return "STRONG SELL", "price below all MAs"
