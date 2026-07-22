"""Daily stock recommendation engine — runs screener and formats top BUY/STRONG BUY signals."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from datetime import date, timezone, timedelta

from stock_checker.fetcher import fetch_stock_data
from stock_checker.idx_stocks import get_all_idx_stocks, get_idx_stocks_by_sector, get_sector_names
from stock_checker.indicators import calculate_mas, calculate_macd, calculate_rsi, calculate_volume_metrics, determine_signal
from stock_checker.screener import calculate_screener_score

logger = logging.getLogger(__name__)

# WIB timezone (UTC+7)
_WIB = timezone(timedelta(hours=7))

# Signal thresholds (matching screener.py)
_SIGNAL_THRESHOLDS = {
    "STRONG BUY": 75.0,
    "BUY": 60.0,
    "WATCH": 45.0,
    "AVOID": 30.0,
}


@dataclass
class DailyRecommendation:
    """Structured daily recommendation output."""
    
    date: str  # "2026-07-23"
    total_scanned: int
    recommendations: list[dict]
    sector: str | None
    scan_duration: float  # seconds
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
    """Run full screener scan and return recommendations.
    
    Parameters
    ----------
    sector :
        Filter by sector name (e.g. "finance_banking") or None for all sectors.
    min_score :
        Minimum score to include in recommendations (default: 60 = BUY threshold).
    top_n :
        Maximum number of recommendations to return.
    min_volume :
        Minimum average daily volume in IDR.
    min_price :
        Minimum stock price in IDR.
    interval :
        Candle interval for technical analysis.
    
    Returns
    -------
    DailyRecommendation
        Structured recommendation data.
    """
    start_time = time.time()
    
    # Get stocks to scan
    if sector:
        if sector not in get_sector_names():
            raise ValueError(f"Unknown sector: {sector}. Available: {', '.join(get_sector_names())}")
        all_stocks = get_idx_stocks_by_sector(sector)
    else:
        all_stocks = get_all_idx_stocks()
    
    logger.info("Scanning %d stocks in sector: %s", len(all_stocks), sector or "ALL")
    
    results: list[dict] = []
    errors: list[str] = []
    
    for symbol in all_stocks:
        try:
            data = fetch_stock_data(symbol, days=30, interval=interval)
            hist = data.pop("_hist")
            hist_clean = hist.dropna(subset=["Close", "Open", "High", "Low"])
            
            # Filter by price
            if data["last_price"] < min_price:
                continue
            
            # Calculate indicators
            mas = calculate_mas(hist_clean, interval=interval)
            signal = determine_signal(data["last_price"], mas)
            rsi = calculate_rsi(hist_clean)
            macd = calculate_macd(hist_clean)
            volume_metrics = calculate_volume_metrics(hist_clean)
            
            # Filter by volume
            if volume_metrics and volume_metrics["avg_volume"] * data["last_price"] < min_volume:
                continue
            
            # Calculate screener score
            score_result = calculate_screener_score(
                ticker=symbol,
                last_price=data["last_price"],
                mas=mas,
                rsi=rsi,
                macd=macd,
                volume_metrics=volume_metrics,
                hist=hist_clean,
            )
            
            # Only include if score meets minimum threshold
            if score_result["score"] >= min_score:
                results.append({
                    "ticker": symbol,
                    "last_price": data["last_price"],
                    "change": data["change"],
                    "change_pct": data["change_pct"],
                    "rsi": rsi,
                    "macd": macd,
                    "mas": mas,
                    "signal_label": signal[0],
                    "score": score_result["score"],
                    "score_label": score_result["signal"],
                    "components": score_result.get("components", {}),
                })
        
        except (ValueError, ConnectionError) as e:
            errors.append(f"{symbol}: {e}")
        except Exception as e:
            logger.exception("Unexpected error for %s", symbol)
            errors.append(f"{symbol}: {e}")
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Take top N
    top_results = results[:top_n]
    
    duration = time.time() - start_time
    
    return DailyRecommendation(
        date=date.today().isoformat(),
        total_scanned=len(all_stocks),
        recommendations=top_results,
        sector=sector,
        scan_duration=duration,
        min_score=min_score,
        errors=len(errors),
    )


def format_recommendation_terminal(rec: DailyRecommendation, currency_symbol: str = "Rp") -> str:
    """Format recommendation as detailed terminal output (Option B).
    
    Returns
    -------
    str
        Formatted string ready for terminal display.
    """
    from io import StringIO
    from rich.console import Console
    
    buf = StringIO()
    console = Console(file=buf, width=80)
    
    # Header
    console.print()
    console.print(f"[bold cyan]📊 Daily Stock Recommendations — {rec.date}[/bold cyan]")
    console.print("─" * 60)
    
    sector_label = rec.sector.upper() if rec.sector else "ALL"
    console.print(f"Scanned: {rec.total_scanned} stocks | Sector: {sector_label} | Min Score: {rec.min_score:.0f}")
    console.print()
    
    if not rec.recommendations:
        console.print("[yellow]No stocks met the minimum score threshold.[/yellow]")
        console.print()
        return buf.getvalue()
    
    # Recommendations
    for i, stock in enumerate(rec.recommendations, 1):
        score_label = stock["score_label"]
        score = stock["score"]
        ticker = stock["ticker"]
        price = stock["last_price"]
        change = stock["change"]
        change_pct = stock["change_pct"]
        rsi = stock.get("rsi")
        macd = stock.get("macd")
        
        # Score color
        if score >= 75:
            score_color = "bold green"
        elif score >= 60:
            score_color = "green"
        elif score >= 45:
            score_color = "yellow"
        else:
            score_color = "red"
        
        # Change color
        change_color = "green" if change >= 0 else "red"
        
        # RSI status
        if rsi is not None:
            if rsi >= 70:
                rsi_status = "[red]overbought[/red]"
            elif rsi <= 30:
                rsi_status = "[green]oversold[/green]"
            else:
                rsi_status = "neutral"
            rsi_text = f"RSI: {rsi:.1f} ({rsi_status})"
        else:
            rsi_text = "RSI: —"
        
        # MACD
        if macd is not None:
            hist = macd.get("histogram", 0)
            macd_arrow = "▲" if hist >= 0 else "▼"
            macd_color = "green" if hist >= 0 else "red"
            macd_text = f"MACD: {hist:+.1f} [{macd_color}]{macd_arrow} bullish[/{macd_color}]" if hist >= 0 else f"MACD: {hist:+.1f} [{macd_color}]{macd_arrow} bearish[/{macd_color}]"
        else:
            macd_text = "MACD: —"
        
        # MA alignment check
        mas = stock.get("mas", {})
        ma20 = mas.get("MA20")
        ma50 = mas.get("MA50")
        ma_checks = []
        if ma20 and price >= ma20:
            ma_checks.append("MA20 ✓")
        if ma50 and price >= ma50:
            ma_checks.append("MA50 ✓")
        if ma20 and ma50 and ma20 > ma50:
            ma_checks.append("MA20>MA50 ✓")
        ma_text = " | ".join(ma_checks) if ma_checks else "No MA alignment"
        
        # Print stock
        console.print(f"[bold]{i}. {ticker}[/bold] — [{score_color}]{score_label}[/{score_color}] (Score: {score:.0f})")
        console.print(f"   Price: {currency_symbol} {price:,.0f} ([{change_color}]{change:+,.0f} ({change_pct:+.1f}%)[/{change_color}])")
        console.print(f"   {rsi_text} | {macd_text}")
        console.print(f"   MA alignment: {ma_text}")
        console.print()
    
    # Footer
    console.print("─" * 60)
    console.print("[dim]Action Guide: STRONG BUY (75-100) | BUY (60-74)[/dim]")
    console.print("[dim]⚠️ For educational purposes only. Do your own research.[/dim]")
    console.print()
    
    return buf.getvalue()


def format_recommendation_telegram(rec: DailyRecommendation) -> str:
    """Format recommendation as Telegram HTML message.
    
    Returns
    -------
    str
        HTML-formatted string for Telegram.
    """
    lines: list[str] = []
    
    # Header
    lines.append(f"📊 <b>Daily Stock Recommendations — {rec.date}</b>")
    lines.append("─" * 30)
    
    sector_label = rec.sector.upper() if rec.sector else "ALL"
    lines.append(f"Scanned: {rec.total_scanned} stocks | Sector: {sector_label}")
    lines.append(f"Min Score: {rec.min_score:.0f} (BUY threshold)")
    lines.append("")
    
    if not rec.recommendations:
        lines.append("⚠️ No stocks met the minimum score threshold.")
        return "\n".join(lines)
    
    # Recommendations
    for i, stock in enumerate(rec.recommendations, 1):
        score_label = stock["score_label"]
        score = stock["score"]
        ticker = stock["ticker"]
        price = stock["last_price"]
        change = stock["change"]
        change_pct = stock["change_pct"]
        rsi = stock.get("rsi")
        macd = stock.get("macd")
        
        # Emoji based on score
        if score >= 75:
            emoji = "🏆"
        elif score >= 60:
            emoji = "✅"
        else:
            emoji = "👀"
        
        # Change sign
        change_sign = "+" if change >= 0 else ""
        
        # RSI
        if rsi is not None:
            if rsi >= 70:
                rsi_status = "⚠️ overbought"
            elif rsi <= 30:
                rsi_status = "🟢 oversold"
            else:
                rsi_status = "neutral"
            rsi_text = f"RSI: {rsi:.1f} ({rsi_status})"
        else:
            rsi_text = "RSI: —"
        
        # MACD
        if macd is not None:
            hist = macd.get("histogram", 0)
            macd_arrow = "▲" if hist >= 0 else "▼"
            macd_trend = "bullish" if hist >= 0 else "bearish"
            macd_text = f"MACD: {hist:+.1f} {macd_arrow} {macd_trend}"
        else:
            macd_text = "MACD: —"
        
        # MA alignment
        mas = stock.get("mas", {})
        ma20 = mas.get("MA20")
        ma50 = mas.get("MA50")
        ma_checks = []
        if ma20 and price >= ma20:
            ma_checks.append("MA20 ✓")
        if ma50 and price >= ma50:
            ma_checks.append("MA50 ✓")
        if ma20 and ma50 and ma20 > ma50:
            ma_checks.append("MA20>MA50 ✓")
        ma_text = " | ".join(ma_checks) if ma_checks else "No MA alignment"
        
        # Build message
        lines.append(f"{emoji} <b>{i}. {ticker}</b> — {score_label} (Score: {score:.0f})")
        lines.append(f"   Price: Rp {price:,.0f} ({change_sign}{change_pct:+.1f}%)")
        lines.append(f"   {rsi_text}")
        lines.append(f"   {macd_text}")
        lines.append(f"   MA: {ma_text}")
        lines.append("")
    
    # Footer
    lines.append("─" * 30)
    lines.append("Action: STRONG BUY (75+) | BUY (60-74)")
    lines.append("⚠️ For educational purposes only. Do your own research.")
    
    return "\n".join(lines)


def format_recommendation_json(rec: DailyRecommendation) -> str:
    """Format recommendation as JSON for logging/analysis.
    
    Returns
    -------
    str
        JSON string.
    """
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
    """Save recommendation to JSON file for historical tracking.
    
    Parameters
    ----------
    rec :
        Daily recommendation to save.
    directory :
        Directory to save reports (default: "reports").
    
    Returns
    -------
    str
        Path to saved file.
    """
    from pathlib import Path
    
    report_dir = Path(directory)
    report_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"daily_{rec.date}.json"
    filepath = report_dir / filename
    
    filepath.write_text(format_recommendation_json(rec), encoding="utf-8")
    logger.info("Saved recommendation to %s", filepath)
    
    return str(filepath)
