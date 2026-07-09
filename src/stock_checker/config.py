"""Typed config loader — reads config.yaml into typed dataclasses."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class AlertConfig:
    """Alert threshold and toggle configuration."""

    dedup_hours: int = 24
    signal_change: bool = True
    ma_crossover: bool = True
    rsi_breach: bool = True
    rsi_recovery: bool = True
    macd_flip: bool = True
    rsi_overbought: float = 70.0
    rsi_oversold: float = 30.0
    volume_spike: bool = True
    volume_spike_window: int = 20
    volume_spike_multiplier: float = 2.0


@dataclass
class TelegramConfig:
    """Telegram bot credentials."""

    bot_token: str = ""
    chat_id: str = ""


@dataclass
class WatchConfig:
    """Watch loop configuration."""

    interval_minutes: int = 55
    stocks: list[str] = field(default_factory=list)


@dataclass
class AppConfig:
    """Top-level application configuration."""

    watch: WatchConfig = field(default_factory=WatchConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    alerts: AlertConfig = field(default_factory=AlertConfig)


def _env_or_val(value: str, env_var: str) -> str:
    """Return *value* if non-empty, otherwise fall back to environment variable."""
    if value:
        return value
    return os.environ.get(env_var, "")


def load_config(path: str = "config.yaml") -> AppConfig:
    """Load and validate configuration from a YAML file.

    Parameters
    ----------
    path :
        Path to the YAML configuration file.

    Returns
    -------
    AppConfig
        Typed configuration object.

    Raises
    ------
    FileNotFoundError
        If the config file does not exist.
    ValueError
        If required fields are missing or invalid.
    """
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}\n"
            f"Copy config.yaml.example to config.yaml and fill in your settings."
        )

    raw: dict = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    # ── Watch section ─────────────────────────────────────────────────────
    watch_raw = raw.get("watch", {})
    stocks: list[str] = watch_raw.get("stocks", [])
    if not stocks:
        raise ValueError("'watch.stocks' must contain at least one ticker symbol.")

    watch = WatchConfig(
        interval_minutes=int(watch_raw.get("interval_minutes", 55)),
        stocks=[s.strip().upper() for s in stocks],
    )

    # ── Telegram section ──────────────────────────────────────────────────
    telegram_raw = raw.get("telegram", {})
    bot_token = _env_or_val(
        str(telegram_raw.get("bot_token", "")), "STOCK_CHECK_BOT_TOKEN"
    )
    chat_id = _env_or_val(
        str(telegram_raw.get("chat_id", "")), "STOCK_CHECK_CHAT_ID"
    )

    if not bot_token:
        raise ValueError(
            "'telegram.bot_token' is required. "
            "Set it in config.yaml or via STOCK_CHECK_BOT_TOKEN env var."
        )
    if not chat_id:
        raise ValueError(
            "'telegram.chat_id' is required. "
            "Set it in config.yaml or via STOCK_CHECK_CHAT_ID env var."
        )

    telegram = TelegramConfig(bot_token=bot_token, chat_id=chat_id)

    # ── Alerts section ────────────────────────────────────────────────────
    alerts_raw = raw.get("alerts", {})
    alerts = AlertConfig(
        dedup_hours=int(alerts_raw.get("dedup_hours", 24)),
        signal_change=bool(alerts_raw.get("signal_change", True)),
        ma_crossover=bool(alerts_raw.get("ma_crossover", True)),
        rsi_breach=bool(alerts_raw.get("rsi_breach", True)),
        rsi_recovery=bool(alerts_raw.get("rsi_recovery", True)),
        macd_flip=bool(alerts_raw.get("macd_flip", True)),
        rsi_overbought=float(alerts_raw.get("rsi_overbought", 70.0)),
        rsi_oversold=float(alerts_raw.get("rsi_oversold", 30.0)),
        volume_spike=bool(alerts_raw.get("volume_spike", True)),
        volume_spike_window=int(alerts_raw.get("volume_spike_window", 20)),
        volume_spike_multiplier=float(alerts_raw.get("volume_spike_multiplier", 2.0)),
    )

    return AppConfig(watch=watch, telegram=telegram, alerts=alerts)
