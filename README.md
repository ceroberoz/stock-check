# IDX Stock Checker

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

CLI tool untuk cek saham Indonesia (IDX) dan US via Yahoo Finance. Termasuk indikator teknikal (MA, RSI, MACD), sinyal trend, analisis DCA, dan Telegram alerts.

## Quick Start

```bash
# Install
git clone https://github.com/YOUR_USERNAME/stock-check.git
cd stock-check
uv sync

# Cek saham
uv run stock-check --check BBCA

# Lihat semua saham IDX30
uv run stock-check --list idx30

# Scan saham potensial
uv run stock-check --screener
```

## Features

| Command | Deskripsi | Contoh |
|---------|-----------|--------|
| `--check` | Cek 1 atau lebih saham | `stock-check --check BBCA` |
| `--list` | List semua saham di indeks | `stock-check --list idx30` |
| `--screener` | Scan saham potensial 3-5% | `stock-check --screener` |
| `--recommend` | Rekomendasi harian | `stock-check --recommend` |
| `--dca` | Analisis DCA | `stock-check --check BBCA,BBRI --dca` |
| `--watch` | Telegram alerts | `stock-check-watch` |

## Setup

### 1. Install

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/YOUR_USERNAME/stock-check.git
cd stock-check
uv sync
```

### 2. Basic Usage

```bash
# Cek saham IDX (default)
uv run stock-check --check BBCA

# Cek saham US
uv run stock-check --check SCHG --exchange US

# Cek multiple saham
uv run stock-check --check BBCA,BBRI,TLKM

# Format JSON
uv run stock-check --check BBCA --format json
```

### 3. Telegram Setup (opsional)

1. Buat bot via [@BotFather](https://t.me/botfather)
2. Dapatkan chat ID via [@userinfobot](https://t.me/userinfobot)
3. Copy `config.yaml.example` ke `config.yaml` dan isi credentials:

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
```

### 4. Konfigurasi

| Variable | Deskripsi |
|----------|-----------|
| `STOCK_CHECK_BOT_TOKEN` | Telegram bot token |
| `STOCK_CHECK_CHAT_ID` | Telegram chat ID |

## Commands

### Check Saham

```bash
# IDX (default, tanpa --exchange)
uv run stock-check --check BBCA

# US stocks (requires --exchange US)
uv run stock-check --check SCHG --exchange US

# Custom interval
uv run stock-check --check BBCA --interval 1wk

# Custom lookback
uv run stock-check --check BBCA --day 5

# Custom MA periods
uv run stock-check --check BBCA --ma 5,20,50,200
```

### List Saham

```bash
# IDX30
uv run stock-check --list idx30

# US ETFs
uv run stock-check --list etf --exchange US
```

### Screener

```bash
# Full IDX scan (873 stocks)
uv run stock-check --screener

# Filter by sector
uv run stock-check --screener --sector mining_coal

# Custom filters
uv run stock-check --screener --min-volume 500000 --min-price 100 --top 10
```

### DCA Analysis

```bash
# IDX
uv run stock-check --check BBCA,BBRI,TLKM --dca --amount 1000000

# US
uv run stock-check --check SCHG,SPY,QQQ --exchange US --dca --amount 100
```

### Daily Recommendation

```bash
# Run recommendation
uv run stock-check --recommend

# Save report
uv run stock-check --recommend --save-report

# Send to Telegram
uv run stock-check --recommend --recommend-telegram
```

### Watch Mode (Telegram Alerts)

```bash
# Run once (test mode)
uv run stock-check-watch --dry-run --once

# Run as daemon
uv run stock-check-watch
```

## IDX Stock Sectors

873 unique stocks across 19 sectors:

| Sector | Stocks | Tier |
|--------|--------|------|
| Finance / Banking | 50 | blue_chip |
| Mining / Coal | 56 | blue_chip |
| Consumer / Food & Beverage | 49 | blue_chip |
| Infrastructure | 30 | blue_chip |
| Consumer / Tobacco | 3 | blue_chip |
| Basic Materials | 57 | mid_cap |
| Industrial | 54 | mid_cap |
| Property & Real Estate | 53 | mid_cap |
| Technology | 46 | mid_cap |
| Transportation & Logistics | 43 | mid_cap |
| Trade & Services | 37 | small_cap |
| Agriculture | 34 | mid_cap |
| Finance / Insurance | 29 | mid_cap |
| Healthcare | 25 | mid_cap |
| Hotels & Tourism | 18 | small_cap |
| Consumer / Household | 13 | mid_cap |
| Energy | 12 | mid_cap |
| Investment | 7 | small_cap |
| Miscellaneous | 257 | small_cap |

### Programmatic Access

```python
from stock_checker.idx_stocks import (
    get_all_idx_stocks,           # List all 873 tickers
    get_idx_stocks_by_sector,     # Get tickers by sector
    get_sector_for_ticker,        # Reverse lookup: ticker → sector
    get_sector_info,              # Sector metadata (name, tier, description)
    get_sector_names,             # List all sector keys
    validate_sectors,             # Check for duplicates
)

# Example: find which sector BBCA belongs to
sector = get_sector_for_ticker("BBCA")  # → "finance_banking"
info = get_sector_info(sector)
print(f"{info.name} ({info.tier})")  # → "Finance / Banking (blue_chip)"
```

## Technical Indicators

### Moving Averages

MA periods adapt to candle interval:

| Interval | MA Periods | Time Span |
|----------|------------|-----------|
| 1d (daily) | MA5, MA9, MA20, MA50 | 1w, 2w, 1m, 2.5m |
| 1wk (weekly) | MA4, MA12, MA24 | 1m, 1q, 6m |
| 1mo (monthly) | MA3, MA6, MA12 | 1q, 6m, 1y |

**Override:** `--ma 5,20,50,200`

### RSI (Relative Strength Index)

- Overbought: > 70
- Oversold: < 30
- Neutral: 30–70

### MACD

- Bullish: histogram > 0
- Bearish: histogram < 0
- Crossover: histogram flips sign

## Architecture

```
src/stock_checker/
├── cli.py              — Thin dispatcher (~130 lines)
├── scanner.py          — Shared scan engine
├── commands/
│   ├── check.py        — --check mode
│   ├── list_cmd.py     — --list mode
│   ├── dca.py          — --dca mode
│   ├── screener.py     — --screener mode
│   └── recommend.py    — --recommend mode
├── screener.py         — Scoring + recommendations
├── formatter.py        — All formatting
├── notifier.py         — Telegram + formatting
├── indicators.py       — MA, RSI, MACD
├── fetcher.py          — yfinance wrapper
├── exchanges.py        — Exchange registry
├── config.py           — Config loader
├── idx_stocks.py       — Stock data (873 tickers, 19 sectors)
├── dca.py              — DCA analysis
├── alert_engine.py     — Alert triggers
├── cache.py            — File cache
└── watcher.py          — Watch daemon
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run linter
uv run ruff check src/

# Run formatter
uv run ruff format src/

# Run tests
uv run pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer

This tool is for educational and informational purposes only. It does not constitute financial advice. Always do your own research before making investment decisions.
