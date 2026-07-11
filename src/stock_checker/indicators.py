"""Technical indicators — moving averages, RSI, MACD, and trend signals."""

import pandas as pd

# Which MA windows to calculate for each candle interval.
# Maps from interval → {label: window_size}
_INTERVAL_MAS: dict[str, dict[str, int]] = {
    "1d": {"MA5": 5, "MA9": 9, "MA20": 20, "MA50": 50},
    "1wk": {"MA4": 4, "MA12": 12, "MA24": 24},
    "1mo": {"MA3": 3, "MA6": 6, "MA12": 12},
    "5d": {"MA5": 5, "MA9": 9},
    "1h": {"MA12": 12, "MA26": 26, "MA50": 50},
}

# Human-readable time-span label for each MA label, per interval.
_INTERVAL_PERIOD_LABELS: dict[str, dict[str, str]] = {
    "1d": {"MA5": "1w", "MA9": "2w", "MA20": "1m", "MA50": "2.5m"},
    "1wk": {"MA4": "1m", "MA12": "1q", "MA24": "6m"},
    "1mo": {"MA3": "1q", "MA6": "6m", "MA12": "1y"},
    "5d": {"MA5": "25d", "MA9": "45d"},
    "1h": {"MA12": "~half-day", "MA26": "~week", "MA50": "~2weeks"},
}


def _get_ma_defs(interval: str) -> dict[str, int]:
    """Return the MA window definition for the given *interval*.

    Falls back to ``1d`` windows if *interval* is unknown.
    """
    return _INTERVAL_MAS.get(interval, _INTERVAL_MAS["1d"])


def _get_period_labels(interval: str) -> dict[str, str]:
    """Return human-readable period labels for the given *interval*."""
    return _INTERVAL_PERIOD_LABELS.get(interval, _INTERVAL_PERIOD_LABELS["1d"])


def calculate_mas(
    hist: pd.DataFrame, interval: str = "1d", custom_periods: list[int] | None = None
) -> dict[str, float]:
    """Calculate rolling moving averages from OHLCV *hist*.

    Parameters
    ----------
    hist :
        OHLCV DataFrame from yfinance.
    interval :
        Candle interval used to select the appropriate MA windows.
    custom_periods :
        Optional list of custom MA periods (e.g. [5, 20, 50, 200]).
        Overrides interval-based MA selection when provided.

    Returns
    -------
        Dict like ``{"MA5": 10050.0, "MA9": 9980.0}``, only including
        windows that have enough data.
    """
    close = hist["Close"]

    if custom_periods:
        mas: dict[str, float] = {}
        for period in custom_periods:
            label = f"MA{period}"
            if len(close) >= period:
                mas[label] = round(close.rolling(window=period).mean().iloc[-1], 2)
        return mas
    else:
        ma_defs = _get_ma_defs(interval)
        mas: dict[str, float] = {}
        for label, window in ma_defs.items():
            if len(close) >= window:
                mas[label] = round(close.rolling(window=window).mean().iloc[-1], 2)
        return mas


def calculate_rsi(hist: pd.DataFrame, period: int = 14) -> float | None:
    """Calculate Relative Strength Index using Wilder's smoothing.

    Returns ``None`` when there are fewer than ``period + 1`` candles.
    """
    close = hist["Close"]
    if len(close) < period + 1:
        return None

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Initial SMA over the first N periods
    avg_gain = gain.iloc[1 : period + 1].mean()
    avg_loss = loss.iloc[1 : period + 1].mean()

    if avg_loss == 0:
        return 100.0

    # Wilder smoothing: (prev_avg * (N-1) + current) / N
    for i in range(period + 1, len(gain)):
        avg_gain = (avg_gain * (period - 1) + gain.iloc[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(rsi, 2)


def calculate_macd(
    hist: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> dict[str, float] | None:
    """Calculate MACD line, signal line, and histogram.

    Returns ``None`` when there are fewer than ``slow`` candles.

    Returned dict keys: ``macd`` (MACD line), ``signal`` (signal line),
    ``histogram`` (MACD line - signal line).
    """
    close = hist["Close"]
    if len(close) < slow:
        return None

    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        "macd": round(macd_line.iloc[-1], 2),
        "signal": round(signal_line.iloc[-1], 2),
        "histogram": round(histogram.iloc[-1], 2),
    }


def determine_signal(last_price: float, mas: dict[str, float]) -> tuple[str, str]:
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


def calculate_volume_metrics(
    hist: pd.DataFrame,
    window: int = 20,
    multiplier: float = 2.0,
) -> dict | None:
    """Calculate volume metrics for spike detection.

    Returns None when there are fewer than ``window + 1`` candles.

    Returned dict keys:
    - current_volume (float): latest candle volume
    - avg_volume (float): rolling mean volume over window
    - volume_spike (bool): current > avg * multiplier
    - volume_ratio (float): current / avg (rounded to 2 decimals)
    """
    volume = hist["Volume"]
    if len(volume) < window + 1:
        return None

    avg_volume = volume.iloc[-window:].mean()
    current_volume = volume.iloc[-1]
    ratio = current_volume / avg_volume if avg_volume > 0 else 0.0

    return {
        "current_volume": round(current_volume, 2),
        "avg_volume": round(avg_volume, 2),
        "volume_spike": ratio >= multiplier,
        "volume_ratio": round(ratio, 2),
    }
