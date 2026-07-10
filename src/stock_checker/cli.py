"""CLI argument parser and entry point for stock-checker."""

import argparse
import logging
import sys

from rich import print as rprint

from stock_checker.config import IDX30_STOCKS
from stock_checker.fetcher import fetch_stock_data
from stock_checker.formatter import format_list_table, format_summary
from stock_checker.indicators import calculate_macd, calculate_mas, calculate_rsi, determine_signal

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stock-check",
        description="Check Indonesian stock prices from IDX via Yahoo Finance.",
    )
    parser.add_argument(
        "--check",
        help="Stock symbol(s), comma-separated (e.g. BBCA or BBCA,BBRI)",
    )
    parser.add_argument(
        "--list",
        choices=["idx30"],
        help="List all stocks in an index (e.g. idx30)",
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

    if not args.check and not args.list:
        parser.error("either --check or --list is required")

    if args.list:
        _handle_list_mode(args)
    else:
        _handle_check_mode(args)


def _handle_list_mode(args: argparse.Namespace) -> None:
    """Handle --list mode: fetch all stocks and display as table."""
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

    stocks = IDX30_STOCKS
    console = Console()
    results: list[dict] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching IDX30 data...", total=len(stocks))

        for symbol in stocks:
            try:
                data = fetch_stock_data(symbol, days=args.day, interval=args.interval)
                hist = data.pop("_hist")

                mas = calculate_mas(hist, interval=args.interval)
                signal = determine_signal(data["last_price"], mas)
                rsi = calculate_rsi(hist)

                results.append({
                    "ticker": data["ticker"].replace(".JK", ""),
                    "last_price": data["last_price"],
                    "change": data["change"],
                    "change_pct": data["change_pct"],
                    "rsi": rsi,
                    "signal": signal[0],
                })
            except (ValueError, ConnectionError) as e:
                console.print(f"[yellow]Warning: {symbol} — {e}[/yellow]")
            except Exception as e:
                logger.exception("Unexpected error for %s", symbol)
                console.print(f"[red]Error: {symbol} — {e}[/red]")

            progress.advance(task)

    if results:
        console.print(format_list_table(results))
    else:
        console.print("[red]No data retrieved.[/red]")


def _handle_check_mode(args: argparse.Namespace) -> None:
    """Handle --check mode: fetch and display individual stock summaries."""
    symbols = [s.strip() for s in args.check.split(",")]

    for symbol in symbols:
        try:
            data = fetch_stock_data(symbol, days=args.day, interval=args.interval)
            hist = data.pop("_hist")  # consume, not printed

            mas = calculate_mas(hist, interval=args.interval)
            signal = determine_signal(data["last_price"], mas)
            rsi = calculate_rsi(hist)
            macd = calculate_macd(hist)

            rprint(
                format_summary(
                    data, mas, signal, interval=args.interval, rsi=rsi, macd=macd
                )
            )
            rprint()
        except ValueError as e:
            rprint(f"Error: {e}\n")
        except ConnectionError as e:
            rprint(f"Network error for {symbol}: {e}\n")
        except Exception as e:
            logger.exception("Unexpected error for %s", symbol)
            rprint(f"Unexpected error for {symbol}: {e}\n")


if __name__ == "__main__":
    main()
