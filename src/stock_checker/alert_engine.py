"""State comparison engine — detects signal changes, MA crossovers, RSI threshold breaches, and MACD histogram flips.

This module is pure logic: no I/O, no external dependencies beyond stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from stock_checker.config import AlertConfig

_ACTION_MAP: dict[str, str] = {
    "STRONG BUY": "HOLD",
    "BUY": "ACCUM",
    "NEUTRAL": "WAIT",
    "SELL": "AVOID",
    "STRONG SELL": "EXIT",
}


def _action(signal_label: str) -> str:
    """Map a signal label to a trading action."""
    return _ACTION_MAP.get(signal_label, "WATCH")


@dataclass
class Alert:
    """An alert produced by comparing previous and current stock state."""

    ticker: str  # e.g. "BBCA.JK"
    alert_type: str  # "signal_change" | "ma_crossover" | "rsi" | "macd"
    severity: str  # "P1" | "P2" | "P3"
    title: str  # short headline
    message: str  # detail text for Telegram
    emoji: str  # emoji character
    action: str = "WATCH"  # HOLD | ACCUM | WAIT | AVOID | EXIT


# ---------------------------------------------------------------------------
# Individual detectors — each returns Alert | None
# ---------------------------------------------------------------------------


def _signal_changed(prev: dict[str, Any], curr: dict[str, Any]) -> Alert | None:
    """Detect when the consolidated signal label changes."""
    prev_signal = prev.get("signal")
    curr_signal = curr.get("signal")

    if prev_signal is None or curr_signal is None:
        return None
    if prev_signal == curr_signal:
        return None

    price = curr.get("price", "?")
    title = f"Signal changed: {prev_signal} → {curr_signal}"
    message = f"{curr_signal} (was {prev_signal}) · Price: {price}"
    return Alert(
        ticker=curr.get("ticker", ""),
        alert_type="signal_change",
        severity="P1",
        title=title,
        message=message,
        emoji="🚨",
        action=_action(curr_signal),
    )


def _ma_crossover(prev: dict[str, Any], curr: dict[str, Any]) -> Alert | None:
    """Detect golden cross (MA5 ↑ MA20) or death cross (MA5 ↓ MA20)."""
    prev_mas = prev.get("mas", {})
    curr_mas = curr.get("mas", {})

    if not isinstance(prev_mas, dict) or not isinstance(curr_mas, dict):
        return None

    ma5_prev = prev_mas.get("MA5")
    ma20_prev = prev_mas.get("MA20")
    ma5_curr = curr_mas.get("MA5")
    ma20_curr = curr_mas.get("MA20")

    if any(v is None for v in (ma5_prev, ma20_prev, ma5_curr, ma20_curr)):
        return None

    price = curr.get("price", "?")

    # Golden cross: MA5 crosses above MA20
    if ma5_prev < ma20_prev and ma5_curr >= ma20_curr:
        title = "Golden cross — MA5 crossed above MA20"
        message = f"MA5 ({ma5_curr:.2f}) crossed above MA20 ({ma20_curr:.2f}) · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="ma_crossover",
            severity="P1",
            title=title,
            message=message,
            emoji="🔄",
            action=_action(curr.get("signal", "")),
        )

    # Death cross: MA5 crosses below MA20
    if ma5_prev > ma20_prev and ma5_curr <= ma20_curr:
        title = "Death cross — MA5 crossed below MA20"
        message = f"MA5 ({ma5_curr:.2f}) crossed below MA20 ({ma20_curr:.2f}) · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="ma_crossover",
            severity="P1",
            title=title,
            message=message,
            emoji="🔄",
            action=_action(curr.get("signal", "")),
        )

    return None


def _rsi_breach(curr: dict[str, Any], config: AlertConfig) -> Alert | None:
    """Detect RSI entering overbought or oversold territory."""
    rsi = curr.get("rsi")
    if rsi is None:
        return None

    price = curr.get("price", "?")

    if rsi >= config.rsi_overbought:
        title = f"RSI overbought: {rsi:.1f}"
        message = f"RSI hit {rsi:.1f} (threshold ≥{config.rsi_overbought}) · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="rsi",
            severity="P2",
            title=title,
            message=message,
            emoji="⚠️",
            action=_action(curr.get("signal", "")),
        )

    if rsi <= config.rsi_oversold:
        title = f"RSI oversold: {rsi:.1f}"
        message = f"RSI hit {rsi:.1f} (threshold ≤{config.rsi_oversold}) · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="rsi",
            severity="P2",
            title=title,
            message=message,
            emoji="⚠️",
            action=_action(curr.get("signal", "")),
        )

    return None


def _macd_flip(prev: dict[str, Any], curr: dict[str, Any]) -> Alert | None:
    """Detect MACD histogram crossing zero (bullish / bearish flip)."""
    prev_hist = prev.get("macd_histogram")
    curr_hist = curr.get("macd_histogram")

    if prev_hist is None or curr_hist is None:
        return None

    price = curr.get("price", "?")

    # Bullish crossover: was negative, now positive
    if prev_hist < 0 and curr_hist >= 0:
        title = "MACD bullish crossover — histogram turned positive"
        message = f"MACD histogram: {prev_hist:.4f} → {curr_hist:.4f} · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="macd",
            severity="P2",
            title=title,
            message=message,
            emoji="📊",
            action=_action(curr.get("signal", "")),
        )

    # Bearish crossover: was positive, now negative
    if prev_hist > 0 and curr_hist <= 0:
        title = "MACD bearish crossover — histogram turned negative"
        message = f"MACD histogram: {prev_hist:.4f} → {curr_hist:.4f} · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="macd",
            severity="P2",
            title=title,
            message=message,
            emoji="📊",
            action=_action(curr.get("signal", "")),
        )

    return None


def _volume_spike(curr: dict[str, Any], config: AlertConfig) -> Alert | None:
    """Detect if current volume is a significant spike above average."""
    if not curr.get("volume_spike"):
        return None

    ratio = curr.get("volume_ratio", 0)
    curr_vol = curr.get("current_volume", 0)
    avg_vol = curr.get("avg_volume", 0)
    price = curr.get("price", "?")

    title = f"Volume spike: {ratio:.1f}x average"
    message = f"Volume: {curr_vol:.0f} vs avg {avg_vol:.0f} ({ratio:.1f}x) · Price: {price}"
    return Alert(
        ticker=curr.get("ticker", ""),
        alert_type="volume_spike",
        severity="P2",
        title=title,
        message=message,
        emoji="📊",
        action=_action(curr.get("signal", "")),
    )


def _rsi_recovery(
    prev: dict[str, Any],
    curr: dict[str, Any],
    config: AlertConfig,
) -> Alert | None:
    """Detect RSI recovering from oversold or overbought territory."""
    prev_rsi = prev.get("rsi")
    curr_rsi = curr.get("rsi")

    if prev_rsi is None or curr_rsi is None:
        return None

    price = curr.get("price", "?")

    # Recovered from oversold: was below threshold, now above threshold + 5
    if prev_rsi < config.rsi_oversold and curr_rsi >= config.rsi_oversold + 5:
        title = f"RSI recovered from oversold: {curr_rsi:.1f}"
        message = f"RSI climbed from {prev_rsi:.1f} to {curr_rsi:.1f} · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="rsi",
            severity="P3",
            title=title,
            message=message,
            emoji="✅",
            action=_action(curr.get("signal", "")),
        )

    # Recovered from overbought: was above threshold, now below threshold - 5
    if prev_rsi > config.rsi_overbought and curr_rsi <= config.rsi_overbought - 5:
        title = f"RSI recovered from overbought: {curr_rsi:.1f}"
        message = f"RSI dropped from {prev_rsi:.1f} to {curr_rsi:.1f} · Price: {price}"
        return Alert(
            ticker=curr.get("ticker", ""),
            alert_type="rsi",
            severity="P3",
            title=title,
            message=message,
            emoji="✅",
            action=_action(curr.get("signal", "")),
        )

    return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def compare_state(
    ticker: str,
    prev: dict[str, Any] | None,
    curr: dict[str, Any],
    config: AlertConfig,
) -> list[Alert]:
    """Compare previous and current state dicts and return triggered alerts.

    Parameters
    ----------
    ticker:
        Stock ticker symbol (e.g. "BBCA.JK").
    prev:
        Previous state dictionary, or *None* on first run (no alerts emitted).
    curr:
        Current state dictionary.
    config:
        Alert configuration determining thresholds and which checks are enabled.

    Returns
    -------
    list[Alert]
        Alerts triggered by the state transition, ordered by detection priority.
    """
    if prev is None:
        return []

    alerts: list[Alert] = []

    # Attach ticker to state dicts so detectors can use curr.get("ticker")
    curr["ticker"] = ticker
    prev["ticker"] = ticker

    # -- Signal change (P1) --------------------------------------------------
    if getattr(config, "signal_change", True):
        result = _signal_changed(prev, curr)
        if result is not None:
            alerts.append(result)

    # -- MA crossover (P1) ---------------------------------------------------
    if getattr(config, "ma_crossover", True):
        result = _ma_crossover(prev, curr)
        if result is not None:
            alerts.append(result)

    # -- RSI breach (P2) -----------------------------------------------------
    if getattr(config, "rsi_breach", True):
        result = _rsi_breach(curr, config)
        if result is not None:
            alerts.append(result)

    # -- MACD flip (P2) ------------------------------------------------------
    if getattr(config, "macd_flip", True):
        result = _macd_flip(prev, curr)
        if result is not None:
            alerts.append(result)

    # -- RSI recovery (P3) ---------------------------------------------------
    if getattr(config, "rsi_recovery", True):
        result = _rsi_recovery(prev, curr, config)
        if result is not None:
            alerts.append(result)

    # -- Volume spike (P2) ----------------------------------------------------
    if getattr(config, "volume_spike", True):
        result = _volume_spike(curr, config)
        if result is not None:
            alerts.append(result)

    return alerts
