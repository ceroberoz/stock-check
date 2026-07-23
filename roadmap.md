# IDX Stock Checker — Roadmap

## Current State

A CLI tool for checking Indonesian (IDX) and US stocks via Yahoo Finance, with technical indicators, stock screening, DCA analysis, and Telegram alerts.

### Features

- **5 command modes**: `--check`, `--list`, `--screener`, `--recommend`, `--dca`
- **4 data sources**: IDX (ID) and US stocks via yfinance
- **Technical indicators**: MA, RSI, MACD, Support/Resistance
- **Telegram alerts**: Watch mode for price/breakout notifications
- **873 unique IDX stocks** across 19 sectors
- **23 unit tests**: indicators, scanner, screener

### Codebase (as of 2024)

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

---

## Completed

- [x] **Basic CLI** — Check single stock, list stocks, exchange support
- [x] **Technical indicators** — MA, RSI, MACD, Support/Resistance
- [x] **Screener** — Scan for 3-5% price potential
- [x] **DCA analysis** — Dollar-cost averaging with custom intervals
- [x] **Telegram alerts** — Watch mode with breakpoint notifications
- [x] **Config management** — YAML config, environment variables
- [x] **Caching** — File-based caching for API calls
- [x] **Refactoring (Phase 1-9)** — All completed:
  - Created `scanner.py` shared scan engine
  - Created `commands/` directory with 5 handlers
  - Merged `recommender.py` into `screener.py`
  - Added `format_recommendation_terminal()` and `format_recommendation_telegram()`
  - Added 23 unit tests (all passing)
  - Rewrote README.md for beginners
  - Updated roadmap.md

- [x] **Stock data improvements** — Deduplicated idx_stocks.py:
  - 1,158 → 873 unique tickers (0 duplicates)
  - Sector metadata with tiers (blue_chip, mid_cap, small_cap, micro_cap)
  - Reverse lookup: ticker → sector
  - Validation function for sector integrity

---

## In Progress

- [ ] **Documentation updates** — README.md and roadmap.md to reflect current state (DONE: roadmap rewritten, DONE: README rewritten)

---

## Next Steps

### Short Term
- [ ] **Additional tests** — Add more unit tests for edge cases and missing modules
- [ ] **Type hints** — Add comprehensive type annotations
- [ ] **Error handling** — Better error messages and retry logic
- [ ] **Documentation** — API documentation for idx_stocks.py functions

### Medium Term
- [ ] **Backtesting** — Historical DCA simulation
- [ ] **Portfolio tracking** — Track actual holdings and P&L
- [ ] **Advanced screening** — More indicators, pattern recognition
- [ ] **Web dashboard** — Optional web UI for results

### Long Term
- [ ] **Machine learning** — Price prediction models
- [ ] **Real-time alerts** — WebSocket for live prices
- [ ] **Multi-asset support** — Bonds, crypto, commodities

---

## Architecture Principles

1. **Command pattern** — Each mode in separate file under `commands/`
2. **Shared scanner** — Single source of truth for fetching data
3. **Formatter separation** — All output formatting in dedicated modules
4. **No duplicate logic** — `recommender.py` merged into `screener.py`
5. **Beginner-friendly** — README written for new users
6. **Test coverage** — Critical paths have unit tests

---

## Key Metrics

| Metric | Value |
|--------|-------|
| IDX stocks | 873 unique |
| Sectors | 19 |
| CLI commands | 5 modes |
| Unit tests | 23 (all passing) |
| Lint errors | 0 |

---

## File Sizes (as of last update)

| File | Lines |
|------|-------|
| `cli.py` | ~130 |
| `scanner.py` | ~200 |
| `screener.py` | ~350 |
| `formatter.py` | ~400 |
| `notifier.py` | ~300 |
| `indicators.py` | ~150 |
| `idx_stocks.py` | ~1,200 |
| `commands/*.py` | 50-150 each |
| `tests/*.py` | 30-80 each |

---

## Notes

- idx_stocks.py is NOT generated — manually maintained, manually curated
- Exchange support: IDX (default) and US (requires `--exchange US`)
- All modes now use shared scanner for consistency
- Watch mode runs as daemon with configurable intervals
