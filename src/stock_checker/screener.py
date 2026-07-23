"""Screener — scoring engine for identifying 3-5% short-term profit potential."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from datetime import date, timezone, timedelta

import pandas as pd

logger = logging.getLogger(__name__)

# WIB timezone (UTC+7)
_WIB = timezone(timedelta(hours=7))


def calculate_screener_score(
    ticker: str,
    last_price: float,
    mas: dict[str, float],
    rsi: float | None = None,
    macd: dict | None = None,
    volume_metrics: dict | None = None,
    hist: pd.DataFrame | None = None,
    atr_pct: float | None = None,
) -> dict:
    """Calculate a comprehensive technical screener score (0-100) for short-term momentum trading.

    Optimized for finding stocks with 2-3% recent positive movement that have
    potential to continue 5-10% based on volume confirmation and momentum.

    ==================  =====  ================================================
    Factor               Pts    Rationale
    ==================  =====  ================================================
    Recent Movement       40    1-3 day price change of 2-3% is the sweet spot.
    Volume Confirmation   25    Volume above average confirms conviction.
    Momentum              20    RSI and MACD show room to run.
    Trend Alignment       15    Price above key MAs supports continuation.
    ==================  =====  ================================================

    Parameters
    ----------
    ticker :
        Stock ticker symbol.
    last_price :
        Most recent closing price.
    mas :
        Moving averages dict from :func:`indicators.calculate_mas`.
    rsi :
        RSI value from :func:`indicators.calculate_rsi` (optional).
    macd :
        MACD dict from :func:`indicators.calculate_macd` (optional).
    volume_metrics :
        Volume metrics dict from :func:`indicators.calculate_volume_metrics`
        (optional).
    hist :
        OHLCV DataFrame from yfinance — used for recent price movement
        calculation (optional).
    atr_pct :
        Pre-calculated ATR as a percentage of price (optional, not used in
        current scoring).

    Returns
    -------
    dict with keys:
        - **ticker** (*str*) — stock symbol.
        - **last_price** (*float*) — closing price.
        - **score** (*float*) — total 0-100 score.
        - **components** (*dict*) — per-factor breakdown.
        - **signal** (*str*) — STRONG BUY / BUY / WATCH / AVOID / EXIT.
    """
    components: dict[str, float] = {
        "recent_movement": _score_recent_movement(hist),
        "volume_confirmation": _score_volume_confirmation(volume_metrics),
        "momentum": _score_momentum(rsi, macd),
        "trend_alignment": _score_trend_alignment(last_price, mas),
    }

    total_score = sum(components.values())
    signal = _interpret_score(total_score)

    return {
        "ticker": ticker,
        "last_price": last_price,
        "score": round(total_score, 1),
        "components": {k: round(v, 1) for k, v in components.items()},
        "signal": signal,
    }


# ---------------------------------------------------------------------------
# Factor scorers (each returns 0 — N pts, where N is the factor max)
# ---------------------------------------------------------------------------


def _score_recent_movement(hist: pd.DataFrame | None) -> float:
    """Score recent price movement over 1-3 days (0-40 pts).

    Optimized for finding stocks with 2-3% positive movement that have
    potential to continue 5-10%.

    Breakdown:
    - 1-day change: max 20 pts
    - 3-day change: max 20 pts

    Sweet spot: 2-3% positive change.
    """
    if hist is None or hist.empty or len(hist) < 2:
        return 0.0

    close = hist["Close"]
    
    # 1-day change
    if len(close) >= 2:
        prev_close = close.iloc[-2]
        curr_close = close.iloc[-1]
        if prev_close > 0:
            change_1d = ((curr_close - prev_close) / prev_close) * 100.0
        else:
            change_1d = 0.0
    else:
        change_1d = 0.0

    # 3-day change
    if len(close) >= 4:
        close_3d_ago = close.iloc[-4]
        if close_3d_ago > 0:
            change_3d = ((curr_close - close_3d_ago) / close_3d_ago) * 100.0
        else:
            change_3d = 0.0
    else:
        change_3d = change_1d

    score = 0.0

    # 1-day scoring (0-20 pts)
    if 2.0 <= change_1d <= 3.0:
        score += 20.0  # Sweet spot
    elif 3.0 < change_1d <= 5.0:
        score += 15.0  # Good but extended
    elif 1.0 <= change_1d < 2.0:
        score += 12.0  # Decent
    elif 0.0 < change_1d < 1.0:
        score += 6.0   # Weak
    elif change_1d > 5.0:
        score += 8.0   # Overextended, may pull back
    # Negative or zero: 0 pts

    # 3-day scoring (0-20 pts)
    if 3.0 <= change_3d <= 5.0:
        score += 20.0  # Sweet spot
    elif 5.0 < change_3d <= 8.0:
        score += 15.0  # Strong but extended
    elif 2.0 <= change_3d < 3.0:
        score += 12.0  # Decent
    elif 0.0 < change_3d < 2.0:
        score += 6.0   # Weak
    elif change_3d > 8.0:
        score += 8.0   # Overextended
    # Negative or zero: 0 pts

    return min(40.0, score)


def _score_volume_confirmation(volume_metrics: dict | None) -> float:
    """Score volume confirmation (0-25 pts).

    Volume above average confirms conviction behind the move.
    Sweet spot: 1.5-3x average volume.
    """
    if volume_metrics is None:
        return 0.0

    ratio = volume_metrics.get("volume_ratio")
    if ratio is None:
        return 0.0

    # fmt: off
    if 1.5 <= ratio <= 3.0:
        return 25.0  # Ideal — strong conviction
    if 3.0 < ratio <= 5.0:
        return 20.0  # Very strong — possible climax but still good
    if 1.2 <= ratio < 1.5:
        return 18.0  # Good — above average
    if 1.0 <= ratio < 1.2:
        return 12.0  # Slightly above average
    if 0.7 <= ratio < 1.0:
        return 6.0   # Below average
    return 2.0        # Very low volume
    # fmt: on


def _score_momentum(rsi: float | None, macd: dict | None) -> float:
    """Score momentum from RSI and MACD (0-20 pts).

    RSI (0-10 pts): Sweet spot 50-65 (room to run, not overbought).
    MACD (0-10 pts): Positive histogram and bullish crossover.
    """
    score = 0.0

    # RSI scoring (0-10 pts)
    if rsi is not None:
        if 50.0 <= rsi <= 65.0:
            score += 10.0  # Sweet spot
        elif 45.0 <= rsi < 50.0 or 65.0 < rsi <= 70.0:
            score += 7.0   # Decent
        elif 40.0 <= rsi < 45.0 or 70.0 < rsi <= 75.0:
            score += 4.0   # Edge
        elif rsi > 75.0:
            score += 1.0   # Overbought
        elif rsi < 40.0:
            score += 2.0   # Oversold bounce potential

    # MACD scoring (0-10 pts)
    if macd is not None:
        macd_line = macd.get("macd", 0.0)
        signal_line = macd.get("signal", 0.0)
        hist_val = macd.get("histogram", 0.0)

        # Bullish crossover: MACD above signal (5 pts)
        if macd_line > signal_line:
            score += 5.0

        # Positive histogram (3 pts)
        if hist_val > 0:
            score += 3.0

        # Histogram strength (2 pts)
        if hist_val > 10:
            score += 2.0
        elif hist_val > 5:
            score += 1.0

    return min(20.0, score)


def _score_trend_alignment(last_price: float, mas: dict[str, float]) -> float:
    """Score trend alignment with moving averages (0-15 pts).

    Price above key MAs supports continuation.
    MA20 > MA50 shows bullish structure.
    """
    score = 0.0

    ma20 = mas.get("MA20")
    ma50 = mas.get("MA50")

    # Price above MA20 (6 pts)
    if ma20 and ma20 > 0 and last_price >= ma20:
        score += 6.0

    # Price above MA50 (4 pts)
    if ma50 and ma50 > 0 and last_price >= ma50:
        score += 4.0

    # MA alignment: MA20 > MA50 (5 pts)
    if ma20 and ma50 and ma20 > 0 and ma50 > 0 and ma20 > ma50:
        score += 5.0

    return min(15.0, score)


# ---------------------------------------------------------------------------
# Signal classification
# ---------------------------------------------------------------------------


def _interpret_score(score: float) -> str:
    """Map a 0-100 score to a trading signal.

    =============  ==============
    Score Range    Signal
    =============  ==============
    75 — 100       STRONG BUY
    60 —  74       BUY
    45 —  59       WATCH
    30 —  44       AVOID
     0 —  29       EXIT
    =============  ==============
    """
    if score >= 75.0:
        return "STRONG BUY"
    if score >= 60.0:
        return "BUY"
    if score >= 45.0:
        return "WATCH"
    if score >= 30.0:
        return "AVOID"
    return "EXIT"


# ---------------------------------------------------------------------------
# Batch screening
# ---------------------------------------------------------------------------


def screen_stocks(stocks: list[dict]) -> list[dict]:
    """Score a list of stocks and return them sorted by score with signals.

    Parameters
    ----------
    stocks :
        List of stock data dictionaries. Each dict **should** contain:

        - **ticker** (*str*) — stock symbol.
        - **last_price** (*float*) — current close.
        - **mas** (*dict*) — moving averages from ``indicators.calculate_mas``.
        - **rsi** (*float*, optional) — from ``indicators.calculate_rsi``.
        - **macd** (*dict*, optional) — from ``indicators.calculate_macd``.
        - **volume_metrics** (*dict*, optional) — from
          ``indicators.calculate_volume_metrics``.
        - **hist** (*DataFrame*, optional) — OHLCV data for ATR/pattern
          calculations.

    Returns
    -------
        Sorted list where each dict has been enriched with:
        **score** (*float*), **components** (*dict*), **signal** (*str*),
        and **target_pct** (*int*).
    """
    results: list[dict] = []

    for stock in stocks:
        score_result = calculate_screener_score(
            ticker=stock.get("ticker", "UNKNOWN"),
            last_price=stock.get("last_price", 0.0),
            mas=stock.get("mas", {}),
            rsi=stock.get("rsi"),
            macd=stock.get("macd"),
            volume_metrics=stock.get("volume_metrics"),
            hist=stock.get("hist"),
        )

        # Enrich the original dict with score data (preserves any extra keys)
        result = {**stock, **score_result}
        results.append(result)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# Daily recommendation (merged from recommender.py)
# ---------------------------------------------------------------------------

_SIGNAL_THRESHOLDS = {
    "STRONG BUY": 75.0,
    "BUY": 60.0,
    "WATCH": 45.0,
    "AVOID": 30.0,
}


@dataclass
class DailyRecommendation:
    """Structured daily recommendation output."""

    date: str
    total_scanned: int
    recommendations: list[dict]
    sector: str | None
    scan_duration: float
    min_score: float
    errors: int = 0


def run_daily_scan(
    sector: str | None = None,
    min_score: float = 60.0,
    top_n: int = 10,
    min_volume: float = 1_000_000,
    min_price: float = 50.0,
    interval: str = "1d",
) -> DailyRecommendation:
    """Run full screener scan and return recommendations."""
    from stock_checker.idx_stocks import get_all_idx_stocks, get_idx_stocks_by_sector, get_sector_names
    from stock_checker.scanner import scan_stocks

    start_time = time.time()

    if sector:
        if sector not in get_sector_names():
            raise ValueError(f"Unknown sector: {sector}. Available: {', '.join(get_sector_names())}")
        all_stocks = get_idx_stocks_by_sector(sector)
    else:
        all_stocks = get_all_idx_stocks()

    logger.info("Scanning %d stocks in sector: %s", len(all_stocks), sector or "ALL")

    scan_results = scan_stocks(
        all_stocks,
        days=30,
        interval=interval,
        min_price=min_price,
        min_volume=min_volume,
        min_score=min_score,
        include_score=True,
    )

    top_results = [
        {
            "ticker": r.ticker,
            "last_price": r.last_price,
            "change": r.change,
            "change_pct": r.change_pct,
            "rsi": r.rsi,
            "macd": r.macd,
            "mas": r.mas,
            "signal_label": r.signal_label,
            "score": r.score,
            "score_label": r.score_label,
            "components": r.score_components,
        }
        for r in scan_results[:top_n]
    ]

    duration = time.time() - start_time

    return DailyRecommendation(
        date=date.today().isoformat(),
        total_scanned=len(all_stocks),
        recommendations=top_results,
        sector=sector,
        scan_duration=duration,
        min_score=min_score,
        errors=0,
    )


def format_recommendation_json(rec: DailyRecommendation) -> str:
    """Format recommendation as JSON for logging/analysis."""
    output = {
        "date": rec.date,
        "total_scanned": rec.total_scanned,
        "sector": rec.sector,
        "min_score": rec.min_score,
        "scan_duration_seconds": round(rec.scan_duration, 2),
        "errors": rec.errors,
        "recommendations": [
            {
                "ticker": s["ticker"],
                "score": s["score"],
                "score_label": s["score_label"],
                "last_price": s["last_price"],
                "change": s["change"],
                "change_pct": s["change_pct"],
                "rsi": s.get("rsi"),
                "macd_histogram": s.get("macd", {}).get("histogram") if s.get("macd") else None,
                "signal_label": s.get("signal_label"),
                "components": s.get("components", {}),
            }
            for s in rec.recommendations
        ],
    }

    return json.dumps(output, indent=2)


def save_recommendation(rec: DailyRecommendation, directory: str = "reports") -> str:
    """Save recommendation to JSON file for historical tracking."""
    from pathlib import Path

    report_dir = Path(directory)
    report_dir.mkdir(parents=True, exist_ok=True)

    filename = f"daily_{rec.date}.json"
    filepath = report_dir / filename

    filepath.write_text(format_recommendation_json(rec), encoding="utf-8")
    logger.info("Saved recommendation to %s", filepath)

    return str(filepath)
