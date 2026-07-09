"""yfinance wrapper with auto .JK suffix for Indonesian stocks."""

import logging
import warnings

import pandas as pd
import yfinance as yf

# yfinance adds a 'default' filter for DeprecationWarning in its own module,
# which overrides Python's default 'ignore' and lets Pandas4Warning through.
# Re-assert silence for this specific subclass.
warnings.filterwarnings(
    "ignore", category=pd.errors.Pandas4Warning, module="yfinance"
)

IDX_SUFFIX = ".JK"

# For each candle interval, fetch at least this much calendar history
# so the longest MA window always has enough data.
_INTERVAL_PERIOD: dict[str, str] = {
    "1d": "3mo",   # 50 daily candles needed for MA50 → 3mo gives ~60
    "1wk": "1y",   # 24 weekly candles needed for MA24 → 1y gives ~52
    "1mo": "2y",   # 12 monthly candles needed for MA12 → 2y gives ~24
    "5d": "6mo",   # 9 five-day candles needed for MA9 → 6mo gives ~36
    "1h": "2mo",   # 50 hourly candles needed for MA50 → 2mo gives ~320
}

logger = logging.getLogger(__name__)


def _ensure_jk_suffix(symbol: str) -> str:
    """Append .JK suffix if the symbol doesn't already have it.

    Indonesian stocks on Yahoo Finance require the .JK suffix (e.g. BBCA.JK).
    """
    s = symbol.strip().upper()
    if not s.endswith(IDX_SUFFIX):
        s += IDX_SUFFIX
    return s


def fetch_history(
    symbol: str, days: int = 1, interval: str = "1d", cache_ttl: int = 0
) -> tuple[str, pd.DataFrame]:
    """Download OHLCV history for *symbol* with enough data for MA calcs.

    Parameters
    ----------
    symbol :
        Stock symbol (with or without .JK suffix).
    days :
        Number of lookback candles to keep for the summary window.
    interval :
        Candle interval (1d, 1wk, 1mo, 5d, 1h).

    Returns
    -------
        ``(ticker, hist)`` where *hist* is a DataFrame.
    """
    ticker = _ensure_jk_suffix(symbol)
    period = _INTERVAL_PERIOD.get(interval, "3mo")

    # Check cache first
    if cache_ttl > 0:
        from stock_checker.cache import get_cached_hist

        cached = get_cached_hist(ticker, period, interval, ttl=cache_ttl)
        if cached is not None:
            return ticker, cached

    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)

    if hist.empty:
        raise ValueError(
            f"No data returned for {ticker} with interval={interval}. "
            f"Check the symbol or your network connection."
        )

    # Store in cache
    if cache_ttl > 0:
        from stock_checker.cache import set_cached_hist

        set_cached_hist(ticker, period, interval, hist)

    return ticker, hist


def fetch_stock_data(
    symbol: str, days: int = 1, interval: str = "1d"
) -> dict:
    """Fetch a lightweight summary dict for *symbol* over *days* lookback.

    Returns keys: ticker, last_price, change, change_pct, open, high,
    low, close, period.
    """
    ticker, hist = fetch_history(symbol, days, interval)

    recent = hist.tail(days) if len(hist) >= days else hist
    last = recent.iloc[-1]
    first = recent.iloc[0]

    change = last["Close"] - first["Open"]
    change_pct = (change / first["Open"]) * 100

    period_label = _build_period_label(days, interval)

    return {
        "ticker": ticker,
        "last_price": round(last["Close"], 2),
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "open": round(last["Open"], 2),
        "high": round(last["High"], 2),
        "low": round(last["Low"], 2),
        "close": round(last["Close"], 2),
        "period": period_label,
        "_hist": hist,
    }


def _build_period_label(days: int, interval: str) -> str:
    """Human-readable period description for the summary box."""
    interval_names = {
        "1d": "trading day",
        "1wk": "week",
        "1mo": "month",
        "5d": "5-day candle",
        "1h": "hour",
    }
    name = interval_names.get(interval, interval)
    if days == 1:
        return f"1 {name}"
    return f"{days} {name}s"
