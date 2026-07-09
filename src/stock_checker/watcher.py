"""Watch loop daemon — polls stocks, detects alerts, sends notifications, persists state."""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import signal
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from stock_checker.alert_engine import Alert, compare_state
from stock_checker.config import AppConfig, load_config
from stock_checker.fetcher import fetch_stock_data
from stock_checker.indicators import (
    calculate_mas,
    calculate_macd,
    calculate_rsi,
    calculate_volume_metrics,
    determine_signal,
)
from stock_checker.notifier import send_telegram

log = logging.getLogger(__name__)

_STATE_FILE = "state.json"


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def _setup_logging() -> None:
    """Configure root logger with rotating file handler and stderr stream."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Rotating file handler: 5 MB per file, 3 backups
    fh = logging.handlers.RotatingFileHandler(
        "stock-checker.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # Stderr stream handler
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    root.addHandler(sh)


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------


def _load_state() -> dict:
    """Read *state.json* from the current working directory.

    Returns an empty dict when the file does not exist or is corrupt.
    """
    path = Path(_STATE_FILE)
    if not path.exists():
        return {}
    try:
        with path.open(encoding="utf-8") as f:
            data: dict = json.load(f)
        return data
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Failed to load state: %s — starting fresh", exc)
        return {}


def _save_state(state: dict) -> None:
    """Atomically write *state* to ``state.json`` via a temporary file."""
    path = Path(_STATE_FILE)
    tmp = path.with_suffix(".json.tmp")
    try:
        tmp.write_text(json.dumps(state, indent=2, default=str), encoding="utf-8")
        tmp.rename(path)
    except OSError as exc:
        log.error("Failed to save state: %s", exc)


# ---------------------------------------------------------------------------
# State builder
# ---------------------------------------------------------------------------


def _build_current_state(hist, mas, signal, rsi, macd, last_price, volume=None) -> dict:  # noqa: ARG001
    """Build a state dict from the current data snapshot.

    Parameters
    ----------
    hist :
        OHLCV DataFrame — unused directly (all computed values are passed separately).
    mas :
        Moving averages dict (e.g. ``{"MA12": 6100.0}``).
    signal :
        Tuple ``(label, description)`` from *determine_signal*.
    rsi :
        RSI value or ``None``.
    macd :
        MACD result dict or ``None``.
    last_price :
        Most recent close price.

    Returns
    -------
    dict
        State dict matching the persisted schema.
    """
    signal_label, _ = signal  # (label, desc) tuple

    if macd is None:
        macd_histogram = 0.0
        macd_line = 0.0
        macd_signal = 0.0
    else:
        macd_histogram = macd.get("histogram", 0.0)
        macd_line = macd.get("macd", 0.0)
        macd_signal = macd.get("signal", 0.0)

    result = {
        "signal": signal_label,
        "price": last_price,
        "mas": mas,
        "rsi": rsi,
        "macd_histogram": macd_histogram,
        "macd_line": macd_line,
        "macd_signal": macd_signal,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if volume is not None:
        result["current_volume"] = volume.get("current_volume", 0)
        result["avg_volume"] = volume.get("avg_volume", 0)
        result["volume_spike"] = volume.get("volume_spike", False)
        result["volume_ratio"] = volume.get("volume_ratio", 0.0)

    return result


# ---------------------------------------------------------------------------
# Telegram dedup helper
# ---------------------------------------------------------------------------


def _send_with_dedup(alert: Alert, state: dict, config: AppConfig) -> bool:
    """Send a Telegram alert unless a duplicate was sent within the dedup window.

    Uses ticker-qualified keys (``{ticker}_{alert_type}``) inside the
    ``_sent_alerts`` sub-dict so different tickers never collide.

    Returns ``True`` when the message was sent, ``False`` when skipped.
    """
    dedup_key = f"{alert.ticker}_{alert.alert_type}"
    sent_alerts: dict = state.setdefault("_sent_alerts", {})

    now = datetime.now(timezone.utc)
    last_sent_str = sent_alerts.get(dedup_key)

    if last_sent_str is not None:
        try:
            last_sent = datetime.fromisoformat(last_sent_str)
            elapsed = now - last_sent
            if elapsed < timedelta(hours=config.alerts.dedup_hours):
                log.debug(
                    "Skipping duplicate %s for %s — sent %s ago",
                    alert.alert_type,
                    alert.ticker,
                    elapsed,
                )
                return False
        except (ValueError, TypeError):
            pass  # Corrupt timestamp — send anyway

    ok = send_telegram(
        config.telegram.bot_token, config.telegram.chat_id, alert
    )
    if ok:
        sent_alerts[dedup_key] = now.isoformat()
    return ok


# ---------------------------------------------------------------------------
# Core watch cycle
# ---------------------------------------------------------------------------


def _run_cycle(config: AppConfig, state: dict, dry_run: bool) -> None:
    """Run one watch cycle: fetch, analyse, alert, persist."""
    stocks = config.watch.stocks
    log.info("Starting watch cycle — %d stock(s) to check", len(stocks))

    total_alerts = 0

    for symbol in stocks:
        log.info("Checking %s...", symbol)
        try:
            data = fetch_stock_data(symbol, days=3, interval="1h")
        except ValueError as exc:
            log.warning("%s: %s", symbol, exc)
            continue
        except ConnectionError as exc:
            log.warning("%s network error: %s", symbol, exc)
            continue
        except Exception as exc:
            log.error("%s unexpected error: %s", symbol, exc, exc_info=True)
            continue

        ticker_jk: str = data["ticker"]
        last_price: float = data["last_price"]
        hist = data["_hist"]

        mas = calculate_mas(hist, interval="1h")
        rsi = calculate_rsi(hist)
        macd = calculate_macd(hist)
        volume_metrics = calculate_volume_metrics(
            hist,
            window=config.alerts.volume_spike_window,
            multiplier=config.alerts.volume_spike_multiplier,
        )
        signal_result = determine_signal(last_price, mas)

        prev = state.get(ticker_jk)
        curr = _build_current_state(
            hist, mas, signal_result, rsi, macd, last_price, volume=volume_metrics
        )

        alerts = compare_state(ticker_jk, prev, curr, config.alerts)

        for alert in alerts:
            total_alerts += 1
            if dry_run:
                log.info("DRY RUN: Would send alert: %s", alert.title)
            else:
                _send_with_dedup(alert, state, config)

        state[ticker_jk] = curr
        _save_state(state)

    log.info("Cycle complete — %d alert(s) triggered", total_alerts)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for ``stock-check watch``."""
    parser = argparse.ArgumentParser(
        prog="stock-check-watch",
        description="IDX stock watch daemon with Telegram alerts.",
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to config file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run one cycle without sending Telegram messages",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single cycle and exit (instead of looping)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    _setup_logging()
    state = _load_state()

    # ── Startup banner ──────────────────────────────────────────────────
    telegram_ok = bool(config.telegram.bot_token and config.telegram.chat_id)
    telegram_label = "Connected" if telegram_ok else "Disconnected"
    dry_run_label = "Yes" if args.dry_run else "No"
    stocks_display = ", ".join(config.watch.stocks)

    banner = (
        "╔══════════════════════════════════════════════╗\n"
        "║     IDX Stock Watch — Telegram Alert Bot    ║\n"
        "╠══════════════════════════════════════════════╣\n"
        f"║  Stocks    : {stocks_display:<30s}║\n"
        f"║  Interval  : Every {config.watch.interval_minutes} minutes{' ' * 15}║\n"
        f"║  Telegram  : {telegram_label:<29s}║\n"
        f"║  Dry run   : {dry_run_label:<29s}║\n"
        "╚══════════════════════════════════════════════╝"
    )
    log.info("\n" + banner)

    # ── Startup notification ────────────────────────────────────────────
    if not args.dry_run and telegram_ok:
        startup_alert = Alert(
            ticker=",".join(config.watch.stocks),
            alert_type="_startup",
            severity="P1",
            title="Bot is online",
            message=(
                f"Watching {len(config.watch.stocks)} stock(s): {stocks_display}\n"
                f"Interval: Every {config.watch.interval_minutes} minutes\n"
                f"Alerts: signal_change, ma_crossover, RSI breach, MACD flip, volume_spike\n"
                f"Dedup: {config.alerts.dedup_hours}h per alert type"
            ),
            emoji="📡",
        )
        ok = send_telegram(config.telegram.bot_token, config.telegram.chat_id, startup_alert)
        if ok:
            log.info("Startup notification sent to Telegram")
        else:
            log.warning("Failed to send startup notification — check your bot_token and chat_id")

    # ── Signal handling ─────────────────────────────────────────────────
    def _handle_signal(signum, frame) -> None:  # noqa: ARG001
        """Graceful shutdown on SIGINT / SIGTERM."""
        log.info("Received signal %s — shutting down...", signum)
        _save_state(state)
        sys.exit(0)

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    # ── Main loop ───────────────────────────────────────────────────────
    while True:
        _run_cycle(config, state, dry_run=args.dry_run)
        if args.once:
            break
        interval = config.watch.interval_minutes
        log.info("Sleeping for %d minutes...", interval)
        time.sleep(interval * 60)
