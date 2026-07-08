"""yfinance wrapper with auto .JK suffix for Indonesian stocks."""

import pandas as pd
import yfinance as yf

IDX_SUFFIX = ".JK"
FETCH_BUFFER_DAYS = 30  # extra history so MA20 can be calculated even on --day 1


def _ensure_jk_suffix(symbol: str) -> str:
    """Append .JK suffix if the symbol doesn't already have it.

    Indonesian stocks on Yahoo Finance require the .JK suffix (e.g. BBCA.JK).
    """
    s = symbol.strip().upper()
    if not s.endswith(IDX_SUFFIX):
        s += IDX_SUFFIX
    return s


def fetch_history(symbol: str, days: int = 1) -> tuple[str, pd.DataFrame]:
    """Download OHLCV history for *symbol* with enough buffer for MA calcs.

    Returns ``(ticker, hist)`` where *hist* is a DataFrame with at least
    *days* rows (usually more to satisfy MA windows).
    """
    ticker = _ensure_jk_suffix(symbol)
    fetch_days = max(days, FETCH_BUFFER_DAYS)

    stock = yf.Ticker(ticker)
    hist = stock.history(period=f"{fetch_days}d")

    if hist.empty:
        raise ValueError(
            f"No data returned for {ticker}. "
            f"Check the symbol or your network connection."
        )
    return ticker, hist


def fetch_stock_data(symbol: str, days: int = 1) -> dict:
    """Fetch a lightweight summary dict for *symbol* over *days* lookback.

    Returns keys: ticker, last_price, change, change_pct, open, high,
    low, close, period.
    """
    ticker, hist = fetch_history(symbol, days)

    recent = hist.tail(days) if len(hist) >= days else hist
    last = recent.iloc[-1]
    first = recent.iloc[0]

    change = last["Close"] - first["Open"]
    change_pct = (change / first["Open"]) * 100

    return {
        "ticker": ticker,
        "last_price": round(last["Close"], 2),
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "open": round(last["Open"], 2),
        "high": round(last["High"], 2),
        "low": round(last["Low"], 2),
        "close": round(last["Close"], 2),
        "period": f"{days} trading day(s)" if days > 1 else "1 trading day",
        "_hist": hist,  # pass-through for indicators
    }
