"""Simple file-based cache for yfinance OHLCV responses."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

_CACHE_FILE = ".stock-cache.json"
_DEFAULT_TTL = 300  # 5 minutes


def _cache_path() -> Path:
    return Path(_CACHE_FILE)


def _load_cache() -> dict:
    path = _cache_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache: dict) -> None:
    path = _cache_path()
    tmp = path.with_suffix(".json.tmp")
    try:
        tmp.write_text(json.dumps(cache, indent=2), encoding="utf-8")
        tmp.rename(path)
    except OSError:
        pass


def _cache_key(ticker: str, period: str, interval: str) -> str:
    return f"{ticker}_{period}_{interval}"


def hist_to_jsonable(df: pd.DataFrame) -> list:
    """Convert OHLCV DataFrame to JSON-serializable list of dicts."""
    if df.empty:
        return []
    records = df.reset_index().to_dict(orient="records")
    result = []
    for record in records:
        row = {}
        for key, value in record.items():
            if isinstance(key, pd.Timestamp):
                row[str(key)] = str(value) if isinstance(value, pd.Timestamp) else value
            else:
                row[str(key)] = str(value) if isinstance(value, pd.Timestamp) else value
        result.append(row)
    return result


def jsonable_to_hist(data: list) -> pd.DataFrame:
    """Restore OHLCV DataFrame from JSON-serializable list."""
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date")
    elif "index" in df.columns:
        df["index"] = pd.to_datetime(df["index"])
        df = df.set_index("index")
    # Ensure numeric columns
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def get_cached_hist(
    ticker: str, period: str, interval: str, ttl: int = _DEFAULT_TTL
) -> pd.DataFrame | None:
    """Return cached OHLCV DataFrame if fresh, otherwise None.
    
    Parameters
    ----------
    ticker:
        Ticker symbol including suffix (e.g. "BBCA.JK").
    period:
        yfinance period string (e.g. "3mo").
    interval:
        Candle interval (e.g. "1d", "1h").
    ttl:
        Cache TTL in seconds. Pass 0 to disable caching for this call.
    
    Returns
    -------
    DataFrame or None if cache miss or expired.
    """
    if ttl <= 0:
        return None
    
    cache = _load_cache()
    key = _cache_key(ticker, period, interval)
    entry = cache.get(key)
    if entry is None:
        return None
    
    cached_at = entry.get("cached_at", 0)
    age = time.time() - cached_at
    if age > ttl:
        return None
    
    data = entry.get("data", [])
    if not data:
        return None
    
    log.debug("Cache HIT for %s (age=%.0fs, ttl=%ds)", key, age, ttl)
    return jsonable_to_hist(data)


def set_cached_hist(
    ticker: str, period: str, interval: str, hist: pd.DataFrame
) -> None:
    """Store OHLCV DataFrame in cache.
    
    Silently skips empty DataFrames.
    """
    if hist.empty:
        return
    
    cache = _load_cache()
    key = _cache_key(ticker, period, interval)
    cache[key] = {
        "cached_at": time.time(),
        "data": hist_to_jsonable(hist),
    }
    _save_cache(cache)


def clear_cache() -> None:
    """Delete the cache file entirely."""
    path = _cache_path()
    try:
        if path.exists():
            path.unlink()
            log.info("Cache cleared: %s", _CACHE_FILE)
    except OSError:
        pass
