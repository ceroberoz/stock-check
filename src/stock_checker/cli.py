"""CLI argument parser and entry point for stock-checker."""

import argparse
import logging

from stock_checker.fetcher import fetch_stock_data
from stock_checker.formatter import format_summary
from stock_checker.indicators import calculate_mas, determine_signal

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stock-check",
        description="Check Indonesian stock prices from IDX via Yahoo Finance.",
    )
    parser.add_argument(
        "--check",
        required=True,
        help="Stock symbol(s), comma-separated (e.g. BBCA or BBCA,BBRI)",
    )
    parser.add_argument(
        "--day",
        type=int,
        default=1,
        help="Number of lookback candles (default: 1). "
        "Combined with --interval to define the window shown.",
    )
    parser.add_argument(
        "--interval",
        choices=["1d", "1wk", "1mo", "5d", "1h"],
        default="1d",
        help="Candle interval: 1d (daily), 1wk (weekly), "
        "1mo (monthly), 5d (5-day), 1h (hourly) (default: 1d). "
        "MA periods adjust automatically to map to consistent time spans.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    symbols = [s.strip() for s in args.check.split(",")]

    for symbol in symbols:
        try:
            data = fetch_stock_data(symbol, days=args.day, interval=args.interval)
            hist = data.pop("_hist")  # consume, not printed

            mas = calculate_mas(hist, interval=args.interval)
            signal = determine_signal(data["last_price"], mas)

            print(format_summary(data, mas, signal, interval=args.interval))
            print()
        except ValueError as e:
            print(f"Error: {e}\n")
        except ConnectionError as e:
            print(f"Network error for {symbol}: {e}\n")
        except Exception as e:
            logger.exception("Unexpected error for %s", symbol)
            print(f"Unexpected error for {symbol}: {e}\n")


if __name__ == "__main__":
    main()
