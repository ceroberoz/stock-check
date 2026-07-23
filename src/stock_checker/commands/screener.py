"""Handle --screener mode: scan all IDX stocks and rank by profit potential."""

from __future__ import annotations

import argparse
import logging

from stock_checker.exchanges import get_exchange
from stock_checker.idx_stocks import get_all_idx_stocks, get_idx_stocks_by_sector, get_sector_names
from stock_checker.scanner import scan_stocks

logger = logging.getLogger(__name__)


def run(args: argparse.Namespace) -> None:
    """Execute --screener mode."""
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

    from stock_checker.formatter import format_screener_table

    exchange = args.exchange
    exchange_config = get_exchange(exchange)
    currency_symbol = exchange_config["currency_symbol"]
    console = Console()

    console.print("[bold cyan]IDX Stock Screener — Scanning for 3-5% opportunities...[/bold cyan]")
    console.print()

    # Get stocks to scan
    if args.sector:
        available_sectors = get_sector_names()
        if args.sector not in available_sectors:
            console.print(f"[red]Error: Unknown sector '{args.sector}'[/red]")
            console.print(f"Available sectors: {', '.join(available_sectors)}")
            return
        all_stocks = get_idx_stocks_by_sector(args.sector)
        console.print(f"Scanning {args.sector.upper()} sector: {len(all_stocks)} stocks")
    else:
        all_stocks = get_all_idx_stocks()
        console.print(f"Found {len(all_stocks)} IDX stocks to scan")

    console.print(f"Filters: min volume = {currency_symbol} {args.min_volume:,.0f}, min price = {currency_symbol} {args.min_price:,.2f}")
    console.print()

    errors: list[str] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning stocks...", total=len(all_stocks))

        def on_progress(symbol: str, current: int, total: int) -> None:
            progress.advance(task)

        scan_results = scan_stocks(
            all_stocks,
            days=args.day,
            interval=args.interval,
            exchange=exchange,
            min_price=args.min_price,
            min_volume=args.min_volume,
            include_score=True,
            progress_callback=on_progress,
        )

    if not scan_results:
        console.print("[red]No stocks matched the filters.[/red]")
        return

    # Convert to format expected by formatter
    results = [
        {
            "ticker": r.ticker.split(".")[0],  # Remove .JK suffix for display
            "last_price": r.last_price,
            "change": r.change,
            "change_pct": r.change_pct,
            "rsi": r.rsi,
            "macd": r.macd,
            "signal": (r.signal_label, r.signal_description),
            "score": r.score,
            "score_label": r.score_label,
        }
        for r in scan_results[:args.top]
    ]

    console.print(format_screener_table(results, currency_symbol, len(all_stocks), len(errors)))
