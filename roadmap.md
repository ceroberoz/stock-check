# Roadmap — IDX Stock Checker (yahoo-finance)

A Python CLI tool to check Indonesian stock prices from Bursa Efek Indonesia (IDX) via Yahoo Finance. Run with `uv`:

```bash
uv stock-check --check BBCA --day 1
```

All features below are weighted by **Eisenhower Matrix** urgency/importance.

---

## Eisenhower Matrix Legend

| Quadrant | Label | Priority |
|---|---|---|
| **Q1 — Urgent & Important** | 🏆 **Must Have** | Do first |
| **Q2 — Not Urgent & Important** | 📅 **Should Have** | Schedule |
| **Q3 — Urgent & Not Important** | 🙋 **Could Have** | Delegate / next sprints |
| **Q4 — Not Urgent & Not Important** | 🗓️ **Won't Have (yet)** | Later / maybe never |

---

## 🏆 Q1 — Must Have (Do First)

| # | Feature | Why | Delivery |
|---|---|---|---|
| 1.1 | **`pyproject.toml` scaffold** with `[project.scripts]` entry (`stock-check`) so `uv stock-check …` works | Core UX: user runs the tool with `uv`, no manual install | Sprint 1 |
| 1.2 | **CLI arg parser** — `--check` (symbol), `--day` (lookback days), `--interval` (candle interval, default `1d`) | Minimal viable interface | Sprint 1 |
| 1.3 | **yfinance integration** — fetch historical OHLCV data for a given ticker + period | Data source — nothing works without data | Sprint 1 |
| 1.4 | **Auto `.JK` suffix** for Indonesian stocks (e.g. `BBCA` → `BBCA.JK`) | IDX stocks require `.JK` on Yahoo Finance | Sprint 1 |
| 1.5 | **Moving Average calculation** — rolling mean via `pandas.Series.rolling().mean()` | The core metric the user asked for | Sprint 1 |
| 1.6 | **Executive summary output** (printed to stdout) — includes ticker, date range, last price, MA values, simple trend signal | The deliverable — what the user sees | Sprint 1 |

### Must Have — Acceptance Criteria

```
$ uv stock-check --check BBCA --day 1
╔══════════════════════════════════════════════╗
║  IDX Stock Checker — Executive Summary      ║
╠══════════════════════════════════════════════╣
║  Ticker    : BBCA.JK                         ║
║  Exchange  : Jakarta Stock Exchange          ║
║  Date      : 2026-07-08                      ║
║  Period    : 1 trading day(s)                ║
║  Interval  : 1d                              ║
║──────────────────────────────────────────────║
║  Last Price   : Rp 10.200                    ║
║  Change       : +125 (+1.24%)                ║
║  Open / High  : 10.100 / 10.250              ║
║  Low  / Close : 10.050 / 10.200              ║
║──────────────────────────────────────────────║
║  Moving Averages (MA)                        ║
║    MA5   (1w) : 10.050  ▲  bullish           ║
║    MA9   (2w) : 9.980   ▲  bullish           ║
║    MA20  (1m) : 9.750   ▲  bullish           ║
║──────────────────────────────────────────────║
║  Signal : STRONG BUY  (price above all MAs)  ║
╚══════════════════════════════════════════════╝
```

---

## 📅 Q2 — Should Have (Schedule)

| # | Feature | Why | Delivery |
|---|---|---|---|
| 2.1 | **Smart MA period selection** based on `--interval` | MA5/9/20 makes sense for `1d` interval but not for `1wk` or `1mo` | Sprint 2 |
| 2.2 | **Error handling** — invalid symbol, network failure, no data, rate limit | Without this the tool crashes on bad input | Sprint 2 |
| 2.3 | **`--interval` flag** support (`1d`, `1wk`, `1mo`, `5d`, `1h`) | Users may want weekly/monthly views, not just daily | Sprint 2 |
| 2.4 | **Multiple tickers** — `--check BBCA,BBRI,ASII` | Compare stocks in one run | Sprint 2 |
| 2.5 | **Rich(r) formatting** — colours (green/red for up/down), table alignment, unicode box-drawing | Readability at a glance | Sprint 2 |
| 2.6 | **Help flag** — `--help` with full docs for all flags | Basic UX courtesy | Sprint 2 |
| 2.7 | **IDX30 list view** — `--list idx30` shows all IDX30 stocks in a compact table | Quick market overview without checking each ticker individually | Sprint 3 |

### Smart MA Period Strategy (Q2.1 detail)

The MA periods adapt dynamically to the candle interval so they map to roughly the same *time spans*:

| `--interval` | MA periods | Time-span meaning |
|---|---|---|
| `1d` (daily) | MA5, MA9, MA20, MA50 | 1w, 2w, 1m, 2.5m |
| `1wk` (weekly) | MA4, MA12, MA24 | 1m, 1q, 6m |
| `1mo` (monthly) | MA3, MA6, MA12 | 1q, 6m, 1y |
| `5d` | MA5, MA9 | 25d, 45d |
| `1h` (hourly) | MA12, MA26, MA50 | ~half-day, ~week, ~2weeks |

> **Rationale:** Fixed MA periods (5/9/20) on daily candles map to ~calendar periods (1w/2w/1m). When the candle interval changes, the MA periods shift so the *time horizon stays consistent*. If the user wants raw periods they can override with a `--ma 5,9,20,50` flag (Q3).

### IDX30 List View (Q2.7 detail)

A new `--list` flag that displays a compact table of all IDX30 stocks with key technical metrics.

**Usage:**
```bash
uv stock-check --list idx30
```

**Output format (Rich table):**
```
╔══════════════════════════════════════════════════════════════════════╗
║                    IDX30 Stock Overview                            ║
╠══════════╦═══════════╦═══════════╦═══════════╦═══════════╦═════════╣
║ Ticker   ║ Last Price║ Change    ║ RSI       ║ Signal    ║ Action  ║
╠══════════╬═══════════╬═══════════╬═══════════╬═══════════╬═════════╣
║ BBCA     ║  6,175    ║ -125(-2%) ║  54.41    ║ BUY       ║ ACCUM   ║
║ BBRI     ║  4,850    ║  +50(+1%) ║  62.30    ║ BUY       ║ ACCUM   ║
║ TLKM     ║  2,340    ║  -10(0%)  ║  45.20    ║ NEUTRAL   ║ WAIT    ║
║ ...      ║ ...       ║ ...       ║ ...       ║ ...       ║ ...     ║
╚══════════╩═══════════╩═══════════╩═══════════╩═══════════╩═════════╝
```

**Columns:**
| Column | Source | Description |
|--------|--------|-------------|
| Ticker | Symbol without .JK | Stock symbol |
| Last Price | `fetch_stock_data()["last_price"]` | Current close price |
| Change | `fetch_stock_data()["change_pct"]` | Price change (%) |
| RSI | `calculate_rsi()` | RSI(14) value |
| Signal | `determine_signal()` | STRONG BUY/BUY/NEUTRAL/SELL/STRONG SELL |
| Action | `_ACTIONS[signal]` | HOLD/ACCUM/WAIT/AVOID/EXIT |

**Behavior:**
- Fetches data for all IDX30 stocks sequentially (with progress indicator)
- Skips stocks with no data (shows warning)
- Sorts by signal priority: STRONG BUY → BUY → NEUTRAL → SELL → STRONG SELL
- Uses Rich tables for alignment and colors (green/red for change)
- Supports `--interval` flag for different timeframes
- Respects `--day` flag for lookback period

**Implementation plan:**
1. Add `--list` argument to CLI parser in `cli.py`
2. Create `format_list_table()` function in `formatter.py` using Rich tables
3. Add IDX30 constant list to `config.py` (same as in config.yaml.example)
4. Update `cli.py:main()` to handle `--list` mode
5. Add progress bar using Rich for feedback during fetch

**Acceptance criteria:**
- [ ] `uv stock-check --list idx30` displays all 30 stocks
- [ ] Table includes all 6 columns (Ticker, Last Price, Change, RSI, Signal, Action)
- [ ] Colors applied: green for positive change, red for negative
- [ ] Signal column colored by signal strength
- [ ] Stocks sorted by signal priority (strongest first)
- [ ] Progress indicator shows during fetch
- [ ] Handles network errors gracefully (skips failed tickers)
- [ ] Runs in < 30 seconds for all 30 stocks

---

## 🙋 Q3 — Could Have (Next Sprints)

| # | Feature | Why | Notes |
|---|---|---|---|
| 3.1 | **RSI (Relative Strength Index)** and **MACD** indicators | RSI is the single highest-signal companion to MA for retail traders | Needs `ta-lib` or manual calc |
| 3.2 | **Volume analysis** — average volume, volume spike detection | Confirms price moves | |
| 3.3 | **`--start / --end`** date range instead of `--day` | Power users want arbitrary range | |
| 3.4 | **JSON / CSV output** via `--format json|csv` | Pipe-able to other tools | |
| 3.5 | **Caching** — cache yfinance responses for N minutes (`--cache-ttl 300`) | Speed up repeated runs on same ticker | |
| 3.6 | **`--ma` override** — user-specified MA periods (`--ma 5,9,20,50`) | Power users may want custom periods | |
| 3.7 | **Support for other exchanges** — set globally (`--exchange .JK`) or per-ticker | Makes the tool generic beyond IDX | |
| 3.8 | **Tabulate output** — alignment, pipe/column separation | Readable multi-ticker output | |

---

## 🗓️ Q4 — Won't Have (Yet) / Later

| # | Feature | Why not now |
|---|---|---|
| 4.1 | **Real-time / WebSocket streaming** | Overkill for a CLI checker; adds complexity, socket management |
| 4.2 | **GUI / Web dashboard** | Scope creep — this is a CLI tool |
| 4.3 | **ML price prediction** | No reliable model exists; false confidence is dangerous |
| 4.4 | **Portfolio tracker** (P&L, holdings) | Different product entirely |
| 4.5 | **Backtesting engine** | Massive scope — would need strategy DSL, slippage model, etc. |
| 4.6 | **Notification / alerting** (email, Telegram, Slack) | Better served by dedicated alerting infra |
| 4.7 | **Auto-update / version manager** | `uv` handles this already |

---

## Suggested Architecture

```
stock-checker/
├── pyproject.toml             # uv project config + entry point
├── src/
│   └── stock_checker/
│       ├── __init__.py
│       ├── __main__.py        # `uv run stock-checker` fallback
│       ├── cli.py             # argparse, entry point
│       ├── fetcher.py         # yfinance wrapper, .JK suffix logic
│       ├── indicators.py      # MA calc, future RSI/MACD
│       ├── formatter.py       # terminal output formatting
│       └── config.py          # defaults, constants
├── tests/
│   ├── test_cli.py
│   ├── test_fetcher.py
│   └── test_indicators.py
└── roadmap.md
```

### Key `pyproject.toml` fields

```toml
[project]
name = "stock-checker"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "yfinance>=0.2.50",
    "pandas>=2.0",
]

[project.scripts]
stock-check = "stock_checker.cli:main"
```

### Core tech decisions

| Decision | Choice | Why |
|---|---|---|
| Dependencies | `yfinance` + `pandas` only (core); `rich` or `tabulate` optional | Minimal surface area — `uv` installs fast |
| CLI framework | `argparse` (stdlib) | Zero dependencies, good enough |
| Indonesian stocks | Auto `.JK` suffix via internal lookup | User types `BBCA`, not `BBCA.JK` |
| MA calculation | `pandas.Series.rolling(window=N).mean()` | Built into pandas, no extra deps |
| Output encoding | UTF-8 with box-drawing characters | Clean terminal display on macOS/Linux |

### MA edge cases (must handle)

| Case | Behaviour |
|---|---|
| `--day 1` with `MA20` | Fetch 30+ days of data internally, calculate MA20, but only **show** the last 1 day's summary |
| Insufficient data for requested MA | Emit warning, show MAs that *can* be calculated, skip the rest |
| Stock just listed (< 20 days of history) | Fall back to available MAs (e.g. only MA5, MA9), warn user |

---

## Dependency Graph (Must Have → Should Have)

```
1.1 pyproject.toml scaffold     ←── no deps
1.2 CLI arg parser              ←── 1.1
1.3 yfinance integration        ←── 1.2 (needs symbol from CLI)
1.4 Auto .JK suffix             ←── 1.2, 1.3 (applied during fetch)
1.5 MA calculation              ←── 1.3 (needs OHLCV data)
1.6 Executive summary output    ←── 1.4, 1.5
                                    │
2.1 Smart MA periods ───────────┘  needs indicator engine
2.2 Error handling ─────────────── needs fetcher (1.3)
2.3 --interval flag ────────────── needs fetcher + MA
2.4 Multiple tickers ───────────── needs CLI + fetcher
2.5 Rich formatting ────────────── needs formatter (1.6)
2.7 IDX30 list view ────────────── needs 2.4 + 2.5 + indicators
```

## Sprint Plan

| Sprint | Focus | Items |
|---|---|---|
| **Sprint 1** | Core (Must Have) | 1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 |
| **Sprint 2** | Hardening (Must Have + Should Have) | 2.1, 2.2, 2.6, 2.3 |
| **Sprint 3** | Multi-ticker + formatting + list view | 2.4, 2.5, 2.7 |
| **Sprint 4+** | Q3 items | 3.1–3.8 (pick by popularity) |

---

## Phase 2 — Automated Watcher & Telegram Alerts

New product direction: a headless daemon that watches configured stocks every hour, detects signal changes / crossovers in real-time, and pushes actionable alerts to Telegram. User trades manually — the bot is purely an early-warning system (at least **1 hour before** the signal shows on daily charts).

### Eisenhower Matrix Legend

| Quadrant | Label | Priority |
|---|---|---|
| **Q1 — Urgent & Important** | 🏆 **Must Have** | Do first |
| **Q2 — Not Urgent & Important** | 📅 **Should Have** | Schedule |
| **Q3 — Urgent & Not Important** | 🙋 **Could Have** | Delegate / next sprints |
| **Q4 — Not Urgent & Not Important** | 🗓️ **Won't Have (yet)** | Later / maybe never |

### 🏆 Q1 — Must Have (Do First)

| # | Feature | Why | Delivery |
|---|---|---|---|
| P1.1 | **`config.yaml`** — stocks list, Telegram creds, alert thresholds, interval, watch schedule | Single source of truth; no hardcoded values | Sprint 1 |
| P1.2 | **`config.py`** — typed dataclass loader for `config.yaml` | Clean typed access across all modules | Sprint 1 |
| P1.3 | **State persistence** (`state.json`) — last-known signal, price, MA levels, RSI, MACD per ticker | Needed to detect *changes* between checks | Sprint 1 |
| P1.4 | **Alert triggers** — signal change detection, MA crossover (golden/death cross), RSI threshold breach, MACD histogram flip | The core intelligence — what fires the alert | Sprint 1 |
| P1.5 | **Telegram notifier** — push formatted alert messages via Telegram Bot HTTP API | Delivery channel — user gets the alert | Sprint 1 |
| P1.6 | **Watch loop** (`stock-check watch`) — continuous fetch→analyze→compare→alert→save cycle | The daemon that runs the bot | Sprint 1 |

### 📅 Q2 — Should Have (Schedule)

| # | Feature | Why | Notes |
|---|---|---|---|
| P2.1 | **Alert deduplication** — don't re-alert same signal within N hours | Prevents spam during flat/range-bound markets | |
| P2.2 | **Graceful error handling** — network outage, yfinance rate-limit, invalid symbols | Daemon must survive transient failures without crashing | |
| P2.3 | **Logging to file** — structured logs with rotation | Debugging and audit trail | |
| P2.4 | **Boot persistence** — systemd `--user` timer or crontab | Bot restarts automatically after reboot | |
| P2.5 | **Alert priority levels** — P1 (signal change), P2 (MA crossover), P3 (RSI/MACD) | User can filter noise vs. high-signal alerts | |

### 🙋 Q3 — Could Have (Next)

| # | Feature | Why | Notes |
|---|---|---|---|
| P3.1 | **Volume spike detection** — hourly volume > 2x average | Confirms breakout on hourly chart | |
| P3.2 | **Multiple alert channels** — email, Slack webhook | Flexibility beyond Telegram | |
| P3.3 | **Per-stock overrides** — different thresholds per ticker | BBCA may have different RSI bands than TLKM | |
| P3.4 | **`--dry-run` mode** — log what *would* be sent without sending | Safe testing | |

### 🗓️ Q4 — Won't Have (Yet)

| # | Feature | Why not now |
|---|---|---|
| P4.1 | **GUI dashboard** | CLI + Telegram push covers the use case; UI is scope creep |
| P4.2 | **Auto-trading / order execution** | User explicitly wants manual trade — auto-execution adds regulatory + financial risk |
| P4.3 | **WebSocket real-time feed** | Hourly interval doesn't need sub-second data; yfinance REST is sufficient |
| P4.4 | **Backtesting engine** | Would need a strategy DSL, slippage model, historical data store — massive scope |
| P4.5 | **Mobile app** | Telegram *is* the mobile experience |

### Key Design Decisions

| Decision | Choice | Why |
|---|---|---|
| Telegram library | Raw HTTP API (`urllib`/`httpx`) | Zero extra deps, simpler error handling |
| State storage | Local `state.json` | Zero infra, trivially inspectable, survives reboot |
| Scheduler | Built-in loop in `watcher.py` + crontab | No extra libs, works on any Unix, simple to monitor |
| Config format | `config.yaml` via `pyyaml` | Human-readable, self-documenting |
| Interval | 55-minute sleep (not 60) | Avoids drift against the hour boundary; catches candle close ASAP |
| Alert trigger priority | Signal change > MA crossover > MACD flip > RSI breach | Fight noise; signal change is the strongest actionable alert |

### "1 Hour Early" — How It Works

```
Hourly candle closes at :00
         │
         ▼
Watcher wakes at ~:01, fetches latest hourly candle
         │
         ▼
Calculates MA12/26/50, RSI(14), MACD(12/26/9) on hourly data
         │
         ▼
Compares vs previous state (state.json):
  ├─ Signal just flipped?           (NEUTRAL → BUY)
  ├─ MA crossover happened?         (MA5 crossed above MA20 = golden cross)
  ├─ RSI entered extreme zone?      (above 70 or below 30)
  └─ MACD histogram flipped sign?   (bearish → bullish)
         │
         ▼
Any trigger? → Telegram push alert
No trigger? → silent, just update state.json
         │
         ▼
Sleep 55 min, repeat
```

**Why this is 1 hour early:** Hourly candles reflect intraday shifts that haven't yet propagated to the daily chart. An MA crossover on the hourly chart typically precedes the daily crossover by 4–8 hours. The watcher catches the moment the hourly candle closes — not minutes later when you'd check manually.

### Dependency Graph (Watcher Phase)

```
P1.1 config.yaml   ←── no deps
P1.2 config.py     ←── P1.1 (needs config.yaml schema)
P1.3 state.json    ←── P1.2 (needs ticker list from config)
P1.4 alert_engine  ←── P1.2, P1.3 (needs config thresholds + state diff)
P1.5 notifier      ←── P1.2 (needs Telegram creds)
P1.6 watcher loop  ←── P1.2, P1.3, P1.4, P1.5 (assembles everything)
                              │
P2.1 dedup ───────────────────┘ needs alert_engine + state
P2.2 error handling ────────── needs watcher loop
P2.3 logging ───────────────── needs watcher loop
```

### Sprint Plan

| Sprint | Focus | Items |
|---|---|---|
| **Sprint 1** | Core Watcher | P1.1 → P1.2 → P1.3 → P1.4 → P1.5 → P1.6 |
| **Sprint 2** | Hardening | P2.1, P2.2, P2.3, P2.4 |
| **Sprint 3** | Alert Quality | P2.5, P3.1, P3.3 |
| **Sprint 4+** | Multi-channel | P3.2, P3.4 |

---

*Last updated: 2026-07-09*
