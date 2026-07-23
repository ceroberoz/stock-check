"""Telegram push notification module using the HTTP API."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request

from stock_checker.alert_engine import Alert

logger = logging.getLogger(__name__)

_TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
_SEPARATOR = "─" * 29


def _build_message(alert: Alert) -> str:
    """Format an Alert into a compact Telegram HTML message."""
    parts: list[str] = [
        f"{alert.emoji} <b>{alert.ticker}</b>",
        _SEPARATOR,
    ]
    if alert.title:
        parts.append(alert.title)
    if alert.message:
        parts.append(alert.message)
    parts.extend(
        [
            _SEPARATOR,
            f"Action: {alert.action} — confirm on 1h chart",
        ]
    )
    return "\n".join(parts)


def send_telegram(bot_token: str, chat_id: str, alert: Alert) -> bool:
    """Send a formatted Telegram message for an alert."""
    if not bot_token or not chat_id:
        logger.error("bot_token and chat_id must be non-empty")
        return False

    text = _build_message(alert)
    payload: dict[str, object] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_notification": False,
    }

    url = _TELEGRAM_API.format(token=bot_token)
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                body = resp.read().decode("utf-8", errors="replace")
                logger.warning("Telegram API returned HTTP %d: %s", resp.status, body)
                return False
            return True
    except urllib.error.URLError as e:
        logger.warning("Telegram API network error: %s", e)
        return False
    except json.JSONEncodeError as e:
        logger.error("Telegram message JSON encode error: %s", e)
        return False
    except Exception as e:
        logger.error("Unexpected error sending Telegram message: %s", e)
        return False


def send_telegram_text(bot_token: str, chat_id: str, text: str) -> bool:
    """Send a plain text message via Telegram."""
    if not bot_token or not chat_id:
        logger.error("bot_token and chat_id must be non-empty")
        return False

    payload: dict[str, object] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_notification": False,
    }

    url = _TELEGRAM_API.format(token=bot_token)
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                body = resp.read().decode("utf-8", errors="replace")
                logger.warning("Telegram API returned HTTP %d: %s", resp.status, body)
                return False
            return True
    except urllib.error.URLError as e:
        logger.warning("Telegram API network error: %s", e)
        return False
    except json.JSONEncodeError as e:
        logger.error("Telegram message JSON encode error: %s", e)
        return False
    except Exception as e:
        logger.error("Unexpected error sending Telegram message: %s", e)
        return False


def format_recommendation_telegram(rec) -> str:
    """Format recommendation as Telegram HTML message."""
    lines: list[str] = []

    lines.append(f"📊 <b>Daily Stock Recommendations — {rec.date}</b>")
    lines.append("─" * 30)

    sector_label = rec.sector.upper() if rec.sector else "ALL"
    lines.append(f"Scanned: {rec.total_scanned} stocks | Sector: {sector_label}")
    lines.append(f"Min Score: {rec.min_score:.0f} (BUY threshold)")
    lines.append("")

    if not rec.recommendations:
        lines.append("⚠️ No stocks met the minimum score threshold.")
        return "\n".join(lines)

    for i, stock in enumerate(rec.recommendations, 1):
        score_label = stock["score_label"]
        score = stock["score"]
        ticker = stock["ticker"]
        price = stock["last_price"]
        change = stock["change"]
        change_pct = stock["change_pct"]
        rsi = stock.get("rsi")
        macd = stock.get("macd")

        if score >= 75:
            emoji = "🏆"
        elif score >= 60:
            emoji = "✅"
        else:
            emoji = "👀"

        change_sign = "+" if change >= 0 else ""

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

        if macd is not None:
            hist = macd.get("histogram", 0)
            macd_arrow = "▲" if hist >= 0 else "▼"
            macd_trend = "bullish" if hist >= 0 else "bearish"
            macd_text = f"MACD: {hist:+.1f} {macd_arrow} {macd_trend}"
        else:
            macd_text = "MACD: —"

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

        lines.append(f"{emoji} <b>{i}. {ticker}</b> — {score_label} (Score: {score:.0f})")
        lines.append(f"   Price: Rp {price:,.0f} ({change_sign}{change_pct:+.1f}%)")
        lines.append(f"   {rsi_text}")
        lines.append(f"   {macd_text}")
        lines.append(f"   MA: {ma_text}")
        lines.append("")

    lines.append("─" * 30)
    lines.append("Action: STRONG BUY (75+) | BUY (60-74)")
    lines.append("⚠️ For educational purposes only. Do your own research.")

    return "\n".join(lines)
