"""Telegram push notification module using the HTTP API.

Sends formatted alert messages via Telegram's bot API
using only stdlib (urllib) — no external HTTP dependencies.
"""

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
            f"Action: {alert.action} \u2014 confirm on 1h chart",
        ]
    )
    return "\n".join(parts)


def send_telegram(bot_token: str, chat_id: str, alert: Alert) -> bool:
    """Send a formatted Telegram message for an alert.

    Returns True on success, False on failure.
    Uses urllib (stdlib) — no external HTTP dependencies.
    """
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
    """Send a plain text message via Telegram.

    Used for daily recommendations, status updates, and other non-alert messages.
    Returns True on success, False on failure.
    Uses urllib (stdlib) — no external HTTP dependencies.
    """
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
