"""yfinance wrapper with exchange-aware suffix handling."""

import logging
import warnings

import pandas as pd
import yfinance as yf

from stock_checker.exchanges import ensure_suffix

warnings.filterwarnings("ignore", category=pd.errors.Pandas4Warning, module="yfinance")

_INTERVAL_PERIOD: dict[str, str] = {
    "1d": "3mo",
    "1wk": "1y",
    "1mo": "2y",
    "5d": "6mo",
    "1h": "2mo",
}

logger = logging.getLogger(__name__)


def fetch_history(
    symbol: str, days: int = 1, interval: str = "1d", exchange: str = "IDX", cache_ttl: int = 0
) -> tuple[str, pd.DataFrame]:
    """Download OHLCV history for *symbol* with enough data for MA calcs.

    Parameters
    ----------
    symbol :
        Stock symbol (with or without exchange suffix).
    days :
        Number of lookback candles to keep for the summary window.
    interval :
        Candle interval (1d, 1wk, 1mo, 5d, 1h).
    exchange :
        Exchange code (IDX, US, etc.).

    Returns
    -------
        ``(ticker, hist)`` where *hist* is a DataFrame.
    """
    ticker = ensure_suffix(symbol, exchange)
    period = _INTERVAL_PERIOD.get(interval, "3mo")

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

    if cache_ttl > 0:
        from stock_checker.cache import set_cached_hist

        set_cached_hist(ticker, period, interval, hist)

    return ticker, hist


def fetch_stock_data(
    symbol: str, days: int = 1, interval: str = "1d", exchange: str = "IDX"
) -> dict:
    """Fetch a lightweight summary dict for *symbol* over *days* lookback.

    Returns keys: ticker, last_price, change, change_pct, open, high,
    low, close, period.
    """
    ticker, hist = fetch_history(symbol, days, interval, exchange=exchange)

    hist_clean = hist.dropna(subset=["Close", "Open", "High", "Low"])
    
    if hist_clean.empty:
        raise ValueError(
            f"No valid data returned for {ticker} with interval={interval}. "
            f"All rows contain NaN values."
        )

    recent = hist_clean.tail(days) if len(hist_clean) >= days else hist_clean
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
