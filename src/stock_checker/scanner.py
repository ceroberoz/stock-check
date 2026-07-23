"""Shared scan engine — fetch→indicators→score pipeline used by all modes."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from stock_checker.fetcher import fetch_stock_data
from stock_checker.indicators import (
    calculate_mas,
    calculate_macd,
    calculate_rsi,
    calculate_volume_metrics,
    determine_signal,
)

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """Result of scanning a single stock."""

    ticker: str
    last_price: float
    change: float
    change_pct: float
    mas: dict[str, float]
    signal_label: str
    signal_description: str
    rsi: float | None = None
    macd: dict | None = None
    volume_metrics: dict | None = None
    score: float = 0.0
    score_label: str = ""
    score_components: dict[str, float] = field(default_factory=dict)


def scan_stock(
    symbol: str,
    days: int = 30,
    interval: str = "1d",
    exchange: str = "IDX",
    custom_periods: list[int] | None = None,
    include_score: bool = False,
) -> ScanResult | None:
    """Fetch and analyze a single stock.

    Returns None on error (logs warning).
    """
    try:
        data = fetch_stock_data(symbol, days=days, interval=interval, exchange=exchange)
        hist = data.pop("_hist")
        hist_clean = hist.dropna(subset=["Close", "Open", "High", "Low"])

        mas = calculate_mas(hist_clean, interval=interval, custom_periods=custom_periods)
        signal_label, signal_description = determine_signal(data["last_price"], mas)
        rsi = calculate_rsi(hist_clean)
        macd = calculate_macd(hist_clean)
        volume_metrics = calculate_volume_metrics(hist_clean)

        result = ScanResult(
            ticker=data["ticker"],
            last_price=data["last_price"],
            change=data["change"],
            change_pct=data["change_pct"],
            mas=mas,
            signal_label=signal_label,
            signal_description=signal_description,
            rsi=rsi,
            macd=macd,
            volume_metrics=volume_metrics,
        )

        if include_score:
            from stock_checker.screener import calculate_screener_score

            score_result = calculate_screener_score(
                ticker=data["ticker"],
                last_price=data["last_price"],
                mas=mas,
                rsi=rsi,
                macd=macd,
                volume_metrics=volume_metrics,
                hist=hist_clean,
            )
            result.score = score_result["score"]
            result.score_label = score_result["signal"]
            result.score_components = score_result.get("components", {})

        return result

    except (ValueError, ConnectionError) as e:
        logger.warning("Skipping %s: %s", symbol, e)
        return None
    except Exception:
        logger.exception("Unexpected error scanning %s", symbol)
        return None


def scan_stocks(
    symbols: list[str],
    days: int = 30,
    interval: str = "1d",
    exchange: str = "IDX",
    min_price: float = 0.0,
    min_volume: float = 0.0,
    min_score: float = 0.0,
    include_score: bool = False,
    progress_callback: callable | None = None,
) -> list[ScanResult]:
    """Scan multiple stocks with filtering.

    Parameters
    ----------
    symbols :
        Stock symbols to scan.
    days :
        Lookback candles for indicator calculation.
    interval :
        Candle interval.
    exchange :
        Exchange code.
    min_price :
        Skip stocks below this price.
    min_volume :
        Skip stocks with avg_volume * price below this.
    min_score :
        Skip stocks with score below this (only if include_score=True).
    include_score :
        Calculate screener score for each stock.
    progress_callback :
        Optional callback after each stock: ``callback(symbol, index, total)``.

    Returns
    -------
    List of ScanResult, sorted by score (if included) or unsorted.
    """
    results: list[ScanResult] = []

    for i, symbol in enumerate(symbols):
        result = scan_stock(
            symbol,
            days=days,
            interval=interval,
            exchange=exchange,
            include_score=include_score,
        )

        if result is not None:
            # Apply filters
            if result.last_price < min_price:
                if progress_callback:
                    progress_callback(symbol, i + 1, len(symbols))
                continue

            if (
                min_volume > 0
                and result.volume_metrics
                and result.volume_metrics["avg_volume"] * result.last_price < min_volume
            ):
                if progress_callback:
                    progress_callback(symbol, i + 1, len(symbols))
                continue

            if include_score and result.score < min_score:
                if progress_callback:
                    progress_callback(symbol, i + 1, len(symbols))
                continue

            results.append(result)

        if progress_callback:
            progress_callback(symbol, i + 1, len(symbols))

    # Sort by score descending if scores were calculated
    if include_score:
        results.sort(key=lambda r: r.score, reverse=True)

    return results
