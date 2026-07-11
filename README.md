# IDX Stock Checker

CLI tool to check stock prices from various exchanges (IDX, US) via Yahoo Finance. Includes technical indicators (MA, RSI, MACD), trend signals, DCA analysis, and optional Telegram alerts.

## Features

- Check individual stocks with `--check BBCA`
- **Multi-exchange support** — IDX (Indonesia) and US markets
- View all IDX30 stocks with `--list idx30`
- Technical indicators: Moving Averages, RSI(14), MACD(12/26/9)
- Auto `.JK` suffix for Indonesian stocks
- Rich terminal output with colors
- JSON and CSV output for scripting (`--format json|csv`)
- Custom MA periods (`--ma 5,20,50,200`)
- **DCA (Dollar Cost Averaging) analysis** with technical ranking (`--dca`)
- Telegram alert bot (watch mode)
- File-based caching for repeated queries

## Installation

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/):

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/stock-check.git
cd stock-check

# Install dependencies
uv sync

# Run the tool
uv run stock-check --check BBCA
```

## Usage

### Check a Stock (IDX - Default Exchange)

```bash
uv run stock-check --check BBCA
```

### Check US Stocks

For US stocks, use `--exchange US`:

```bash
uv run stock-check --check SCHG --exchange US
uv run stock-check --check SPY,QQQ --exchange US
```

**Note:** `--exchange` is required for non-IDX stocks. IDX is the default and doesn't need the flag.

### Available Exchanges

| Exchange | Suffix | Currency | Flag | Example |
|----------|--------|----------|------|---------|
| **IDX** (Jakarta) | `.JK` | Rp (IDR) | *(default)* | `--check BBCA` |
| **US Market** | *(none)* | $ (USD) | `--exchange US` | `--check SCHG --exchange US` |

Output:

```
╔══════════════════════════════════════════════╗
║    IDX Stock Checker — Executive Summary     ║
╠══════════════════════════════════════════════╣
║  Ticker      : BBCA.JK                       ║
║  Exchange    : Jakarta Stock Exchange        ║
║  Date        : 2026-07-10                    ║
║  Period      : 1 trading day                 ║
║  Interval    : 1d                            ║
║──────────────────────────────────────────────║
║  Last Price  : Rp 6,175                      ║
║  Change      : -125 (-1.98%)                 ║
║  Open / High : 6,300 / 6,300                 ║
║  Low / Close : 6,125 / 6,175                 ║
║──────────────────────────────────────────────║
║  Moving Averages (MA)                        ║
║    MA5  (1w) :    6,195  ▼  bearish          ║
║    MA9  (2w) :    5,997  ▲  bullish          ║
║    MA20 (1m) :    6,061  ▲  bullish          ║
║    MA50 (2.5m) :    5,936  ▲  bullish        ║
║──────────────────────────────────────────────║
║  Oscillators                                 ║
║    RSI(14)     :   54.41  neutral            ║
║    MACD(12/26/9) :      +34  ▲  bullish      ║
║──────────────────────────────────────────────║
║      Signal : BUY  (price above most MAs)    ║
║       Action : ACCUM  (need MA50 5,936)      ║
╚══════════════════════════════════════════════╝
```

### List All IDX30 Stocks

```bash
uv run stock-check --list idx30
```

Output:

```
                              IDX30 Stock Overview                              
┏━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Ticker  ┃  Last Price ┃        Change ┃       RSI ┃ Signal       ┃ Action    ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ BBCA    │    Rp 6,175 │  -125 (-2.0%) │      54.4 │ BUY          │ ACCUM     │
│ BBRI    │    Rp 2,790 │    +0 (+0.0%) │      45.9 │ STRONG SELL  │ EXIT      │
│ TLKM    │    Rp 2,480 │    +0 (+0.0%) │      44.8 │ STRONG SELL  │ EXIT      │
│ ...     │ ...         │ ...           │ ...       │ ...          │ ...       │
└─────────┴─────────────┴───────────────┴───────────┴──────────────┴───────────┘
```

### Check Multiple Stocks

```bash
uv run stock-check --check BBCA,BBRI,ASII
```

### Use Different Intervals

```bash
uv run stock-check --check BBCA --interval 1wk
uv run stock-check --check BBCA --interval 1h
```

### Lookback Period

```bash
uv run stock-check --check BBCA --day 5
```

### Custom MA Periods

Override the default moving average periods with `--ma`:

```bash
# Use custom periods (comma-separated)
uv run stock-check --check BBCA --ma 5,20,50,200

# Combine with interval
uv run stock-check --check BBCA --interval 1wk --ma 4,12,24
```

The `--ma` flag overrides the interval-based MA selection, letting you use any periods you want.

### Output Formats

Switch between text, JSON, and CSV output:

```bash
# Default rich terminal output
uv run stock-check --check BBCA

# JSON output (for scripting/piping)
uv run stock-check --check BBCA --format json

# CSV output (for spreadsheets)
uv run stock-check --check BBCA --format csv

# Multiple stocks in CSV
uv run stock-check --check BBCA,BBRI,ASII --format csv
```

**JSON output example:**
```json
{
  "ticker": "BBCA.JK",
  "exchange": "Jakarta Stock Exchange",
  "date": "2026-07-11",
  "price": {
    "last": 6175.0,
    "change": -125.0,
    "change_pct": -1.98
  },
  "moving_averages": {
    "MA5": 6195.0,
    "MA9": 5997.22,
    "MA20": 6061.25,
    "MA50": 5935.5
  },
  "signal": {
    "label": "BUY",
    "description": "price above most MAs"
  },
  "rsi": 54.41,
  "macd": {
    "macd": 64.53,
    "signal": 30.1,
    "histogram": 34.42
  }
}
```

## DCA (Dollar Cost Averaging) Analysis

Compare multiple stocks and find the best pick for monthly investing using technical analysis-based scoring.

### Usage

```bash
# IDX stocks (default)
uv run stock-check --check BBCA,BBRI,TLKM --dca --amount 1000000

# US stocks
uv run stock-check --check SCHG,SPY,QQQ --exchange US --dca --amount 10
```

### Scoring Factors

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| **Signal** | 40 pts | BUY/SELL recommendation strength |
| **RSI** | 30 pts | Room to grow (40-60 ideal) vs overbought (>70) |
| **MACD** | 20 pts | Momentum direction and strength |
| **MA Alignment** | 10 pts | Price vs moving average positioning |

### Example Output

```
╔══════════════════════════════════════════════════════╗
║              DCA Analysis — IDX Stocks                ║
╠══════════════════════════════════════════════════════╣
║  Monthly Investment: Rp 1,000,000                     ║
║──────────────────────────────────────────────────────║
║  Ticker  Price    Signal    RSI   MACD   Score  Rank  ║
║──────────────────────────────────────────────────────║
║  BBCA    Rp 6,175 BUY       54.4  +34.4  84/100  1    ║
║  PGEO    Rp 1,005 STRONG BUY 68.2  +15.9  78/100  2    ║
║  ELSA    Rp 655   STRONG BUY 68.2  +14.1  78/100  3    ║
║──────────────────────────────────────────────────────║
║  Recommendation: BBCA                                  ║
╚══════════════════════════════════════════════════════╝
```

## Telegram Alerts (Watch Mode)

Set up a Telegram bot to receive alerts when technical signals change.

### Setup

1. Create a Telegram bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID (send a message to [@userinfobot](https://t.me/userinfobot))
3. Copy `config.yaml.example` to `config.yaml` and fill in credentials:

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  chat_id: "YOUR_CHAT_ID"

watch:
  stocks:
    - BBCA
    - BBRI
    - TLKM
  interval_minutes: 55

alerts:
  signal_change: true
  ma_crossover: true
  rsi_breach: true
  macd_flip: true
```

### Run Watcher

```bash
# Run once (test mode)
uv run stock-check-watch --dry-run --once

# Run as daemon
uv run stock-check-watch

# Use environment variables for credentials
STOCK_CHECK_BOT_TOKEN="your_token" STOCK_CHECK_CHAT_ID="your_id" uv run stock-check-watch
```

### Alert Types

| Alert | Priority | Description |
|-------|----------|-------------|
| Signal change | P1 | STRONG BUY → BUY, etc. |
| MA crossover | P1 | Golden cross (MA5 ↑ MA20) or death cross |
| RSI breach | P2 | RSI > 70 (overbought) or < 30 (oversold) |
| MACD flip | P2 | Histogram crosses zero |
| Volume spike | P2 | Volume > 2x average |

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `STOCK_CHECK_BOT_TOKEN` | Telegram bot token |
| `STOCK_CHECK_CHAT_ID` | Telegram chat ID |

### config.yaml

See `config.yaml.example` for all available options.

## Technical Indicators

### Moving Averages

MA periods adapt to candle interval for consistent time horizons:

| Interval | MA Periods | Time Span |
|----------|------------|-----------|
| 1d (daily) | MA5, MA9, MA20, MA50 | 1w, 2w, 1m, 2.5m |
| 1wk (weekly) | MA4, MA12, MA24 | 1m, 1q, 6m |
| 1mo (monthly) | MA3, MA6, MA12 | 1q, 6m, 1y |

**Override:** Use `--ma 5,20,50,200` to specify custom periods instead of the defaults.

### RSI (Relative Strength Index)

- Overbought: > 70
- Oversold: < 30
- Neutral: 30–70

### MACD

- Bullish: histogram > 0
- Bearish: histogram < 0
- Crossover: histogram flips sign

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run linter
uv run ruff check src/

# Run formatter
uv run ruff format src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer

This tool is for educational and informational purposes only. It does not constitute financial advice. Always do your own research before making investment decisions.
