"""Handle --list mode: display stocks from an index (e.g. idx30, etf)."""

from __future__ import annotations

import argparse
import logging

from stock_checker.exchanges import get_exchange, get_stock_list
from stock_checker.formatter import format_list_table
from stock_checker.scanner import scan_stocks

logger = logging.getLogger(__name__)


def run(args: argparse.Namespace) -> None:
    """Execute --list mode."""
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

    exchange = args.exchange
    exchange_config = get_exchange(exchange)
    suffix = exchange_config["suffix"]
    currency_symbol = exchange_config["currency_symbol"]
    console = Console()

    # Validate list name
    available_lists = list(exchange_config["lists"].keys())
    if args.list not in available_lists:
        console.print(
            f"[red]Error: '{args.list}' is not available for {exchange}. "
            f"Available lists: {', '.join(available_lists)}[/red]"
        )
        return

    stocks = get_stock_list(exchange, args.list)
    console.print(f"[cyan]Fetching {args.list.upper()} data...[/cyan]")

    results: list[dict] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Fetching {args.list.upper()} data...", total=len(stocks))

        for symbol in stocks:
            result = scan_stocks(
                [symbol],
                days=args.day,
                interval=args.interval,
                exchange=exchange,
            )

            if result:
                r = result[0]
                display_ticker = r.ticker.replace(suffix, "") if suffix else r.ticker
                results.append({
                    "ticker": display_ticker,
                    "last_price": r.last_price,
                    "change": r.change,
                    "change_pct": r.change_pct,
                    "rsi": r.rsi,
                    "signal": r.signal_label,
                })

            progress.advance(task)

    if results:
        console.print(format_list_table(results, currency_symbol=currency_symbol))
    else:
        console.print("[red]No data retrieved.[/red]")
