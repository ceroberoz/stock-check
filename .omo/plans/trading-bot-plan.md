# Trading Bot — Implementation Plan

## Goal

Build a headless watch daemon (`stock-check watch`) that polls configured IDX stocks every hour, detects signal changes / MA crossovers / RSI extremes / MACD flips on hourly candles, and pushes actionable Telegram alerts — giving the user at least **1 hour early warning** before the signal materializes on the daily chart.

## Prerequisites

- Python >= 3.11, uv
- Telegram bot token (user creates via [@BotFather](https://t.me/botfather))
- Existing codebase: `cli.py`, `fetcher.py`, `indicators.py`, `formatter.py` (all stable)

---

## Step-by-Step Tasks

### Step 1: Add `pyyaml` dependency & new CLI entry

**Files:** `pyproject.toml`

- Add `pyyaml>=6.0` to `[project.dependencies]`
- Add new script entry: `stock-check-watch = "stock_checker.watcher:main"`

**Verify:** `uv lock` succeeds

---

### Step 2: Create `config.yaml` (user-facing config file)

**Files:** `config.yaml` (project root)

Structure:

```yaml
# config.yaml — Trading Bot Configuration
watch:
  interval_minutes: 55          # How often to poll (min)
  stocks:                       # Tickers to watch
    - BBCA
    - TLKM
    - BBRI

telegram:
  bot_token: "YOUR_BOT_TOKEN"   # From @BotFather
  chat_id: "YOUR_CHAT_ID"       # Your Telegram chat ID

alerts:
  # Minimum time (hours) before re-alerting the same trigger type per ticker
  dedup_hours: 24

  # Enable/disable specific triggers
  signal_change: true           # BUY→SELL, NEUTRAL→BUY, etc.
  ma_crossover: true            # MA5 crosses MA20 (golden/death cross)
  rsi_overbought: 70.0          # Alert when RSI exceeds this
  rsi_oversold: 30.0            # Alert when RSI drops below this
  macd_crossover: true          # MACD line crosses signal line
```

**Must do:**
- Ship a `config.yaml.example` (so git doesn't track secrets)
- Add `config.yaml` to `.gitignore`
- Validate all required fields on load

---

### Step 3: Create `config.py` — typed config loader

**Files:** `src/stock_checker/config.py`

- `@dataclass` classes: `AlertConfig`, `TelegramConfig`, `WatchConfig`, `AppConfig`
- `load_config(path: str = "config.yaml") -> AppConfig` — reads YAML, validates, returns typed object
- Provide sensible defaults for all alert thresholds
- Raise `ValueError` with clear message on missing required fields (`bot_token`, `chat_id`, empty `stocks`)

---

### Step 4: Create `alert_engine.py` — signal change & crossover detection

**Files:** `src/stock_checker/alert_engine.py`

Core logic — compares **current** fetch result against **previous** persisted state and returns a list of triggered alerts.

**State schema** (persisted to `state.json`, keyed by ticker):

```json
{
  "BBCA.JK": {
    "signal": "BUY",
    "price": 6125,
    "mas": {"MA12": 6100, "MA26": 6050, "MA50": 5930},
    "rsi": 53.5,
    "macd_histogram": 31,
    "macd_line": 150,
    "macd_signal": 119,
    "updated_at": "2026-07-09T10:00:00"
  }
}
```

**Detectors (each returns None or an Alert object):**

| Detector | Trigger | Example message |
|---|---|---|
| `signal_changed(prev, curr)` | Signal label changed | `Signal: NEUTRAL → BUY ↑` |
| `ma_crossover(prev, curr)` | MA5 crosses MA20 | `MA5(6,155) crossed above MA20(6,040) — Golden Cross on hourly` |
| `rsi_breach(curr, config)` | RSI > 70 or < 30 | `RSI(14) at 72.3 — overbought zone` |
| `macd_flip(prev, curr)` | MACD histogram sign change | `MACD flipped from -12 to +8 — bullish crossover` |
| `rsi_recovery(prev, curr, config)` | RSI was <30 now >35 | `RSI recovering from 28.5 to 36.2 — exiting oversold` |

**Alert dataclass:**

```python
@dataclass
class Alert:
    ticker: str
    alert_type: str          # "signal_change" | "ma_crossover" | "rsi" | "macd"
    severity: str            # "P1" | "P2" | "P3"
    title: str               # short headline
    message: str             # detail text for Telegram
    emoji: str               # 🚨 | ⚠️ | 📊 | 🔄
```

**Must do:**
- `compare_state(prev: dict, curr: dict, config: AlertConfig) -> list[Alert]` — main entry point
- Handle missing/empty previous state gracefully (first run = no alerts, just seed state)
- RSI recovery detector — RSI leaving oversold/overbought is an actionable signal

**Must not do:**
- No yfinance calls — this is pure logic on already-fetched data
- No I/O — caller passes state

---

### Step 5: Create `notifier.py` — Telegram push via HTTP API

**Files:** `src/stock_checker/notifier.py`

- `send_telegram(bot_token: str, chat_id: str, alert: Alert) -> bool`
- Uses `urllib.request` (stdlib) to POST to `https://api.telegram.org/bot{token}/sendMessage`
- Message format with `parse_mode="HTML"`:

```
🚨 <b>IDX Alert — BBCA.JK</b>
━━━━━━━━━━━━━━━━━━
Signal: NEUTRAL → <b>BUY</b> ↑
Price : Rp 6,125 (+0.41%)
RSI   : 53.50 (neutral)
MACD  : +31 ▲ bullish
Trigger: MA5 crossed above MA20 (golden cross on hourly)
━━━━━━━━━━━━━━━━━━
<b>Action</b>: ACCUMULATE
```

- Handle API errors gracefully — log warning, don't crash
- Optional: add `disable_notification=True` for non-urgent alert types

---

### Step 6: Create `watcher.py` — main watch loop & CLI

**Files:** `src/stock_checker/watcher.py`

**CLI entry:** `stock-check watch` (via `main()`)

**Flow:**

```
1. Load config.yaml → AppConfig
2. Load state.json → prev_state (empty dict if missing)
3. For each stock in config.stocks:
   a. fetch_stock_data(symbol, days=3, interval="1h")
      — "3 days" ensures enough hourly candles for MA50
   b. Calculate MA12, MA26, MA50 via calculate_mas(hist, interval="1h")
   c. Calculate RSI via calculate_rsi(hist)
   d. Calculate MACD via calculate_macd(hist)
   e. Determine signal via determine_signal(last_price, mas)
   f. alert_engine.compare_state(prev_state[ticker], current, config.alerts)
   g. If alerts: notifier.send_telegram(...) for each alert
   h. Update state.json with current state
4. Sleep config.watch.interval_minutes (default 55)
5. Repeat from step 2
```

**Error handling:**
- Network error → log, skip that ticker, continue next
- Invalid symbol → log, skip, notify once via Telegram
- yfinance rate limit → exponential backoff (1min, 2min, 4min, max 15min)

**Signals:**
- `SIGTERM` / `SIGINT` — flush state.json, log shutdown, exit cleanly

**Must do:**
- Logging to `stock-checker.log` with rotation (via `logging.handlers.RotatingFileHandler`)
- Print startup banner with watched tickers and Telegram status
- Print a heartbeat log line every cycle

---

### Step 7: Wire up `cli.py` with `watch` subcommand

**Files:** `src/stock_checker/cli.py`

- Add a `watch` subcommand (`argparse subparsers`) or
- Keep `watcher.py` as standalone `stock-check-watch` entry point (simpler, clearer separation)

**Recommendation:** separate entry point `stock-check-watch` — keeps existing CLI clean and allows `ps aux | grep stock-check-watch` for status checking.

---

### Step 8: `.gitignore` + `config.yaml.example`

- Add `config.yaml` to `.gitignore`
- Create `config.yaml.example` with placeholder values

---

## Files Summary

| Action | File | Purpose |
|---|---|---|
| **MODIFY** | `pyproject.toml` | Add `pyyaml` dep, add `stock-check-watch` entry |
| **CREATE** | `config.yaml` | User config (gitignored) |
| **CREATE** | `config.yaml.example` | Template with placeholders |
| **CREATE** | `src/stock_checker/config.py` | Typed config loader |
| **CREATE** | `src/stock_checker/alert_engine.py` | State comparison + alert triggers |
| **CREATE** | `src/stock_checker/notifier.py` | Telegram HTTP push |
| **CREATE** | `src/stock_checker/watcher.py` | Main watch loop + entry point |
| **MODIFY** | `.gitignore` | Add `config.yaml`, `state.json`, `*.log` |

---

## Verification

1. `uv lock` succeeds (deps resolved)
2. `uv run python -c "from stock_checker.config import load_config; c = load_config('config.yaml.example'); print(c)"` — config loads
3. `uv run python -c "from stock_checker.alert_engine import compare_state"` — imports clean
4. `uv run stock-check-watch --dry-run` — runs one cycle, logs alerts, no Telegram sent
5. `uv run stock-check-watch` — runs, sends real Telegram if triggers fire
6. Kill with Ctrl+C — state.json is valid JSON, restart resumes cleanly
