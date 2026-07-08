"""CLI argument parser and entry point for stock-checker."""

import argparse

from stock_checker.fetcher import fetch_stock_data
from stock_checker.formatter import format_summary
from stock_checker.indicators import calculate_mas, determine_signal


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
        help="Number of lookback trading days (default: 1)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    symbols = [s.strip() for s in args.check.split(",")]

    for symbol in symbols:
        try:
            data = fetch_stock_data(symbol, days=args.day)
            hist = data.pop("_hist")  # consume, not printed

            mas = calculate_mas(hist)
            signal = determine_signal(data["last_price"], mas)

            print(format_summary(data, mas, signal))
            print()
        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Unexpected error for {symbol}: {e}\n")


if __name__ == "__main__":
    main()
