"""Handle --dca mode: DCA analysis with technical ranking."""

from __future__ import annotations

import argparse
import logging

from stock_checker.dca import calculate_dca_ranking, format_dca_output
from stock_checker.exchanges import get_exchange
from stock_checker.scanner import scan_stocks

logger = logging.getLogger(__name__)


def run(args: argparse.Namespace) -> None:
    """Execute --dca mode."""
    from rich.console import Console

    symbols = [s.strip() for s in args.check.split(",")]
    exchange = args.exchange
    exchange_config = get_exchange(exchange)
    currency_symbol = exchange_config["currency_symbol"]
    console = Console()

    scan_results = scan_stocks(
        symbols,
        days=args.day,
        interval=args.interval,
        exchange=exchange,
    )

    if not scan_results:
        console.print("[red]No data retrieved.[/red]")
        return

    # Convert to format expected by dca module
    results = [
        {
            "ticker": r.ticker,
            "last_price": r.last_price,
            "signal": (r.signal_label, r.signal_description),
            "rsi": r.rsi,
            "macd": r.macd,
            "mas": r.mas,
        }
        for r in scan_results
    ]

    ranked = calculate_dca_ranking(results, args.amount, exchange)
    console.print(format_dca_output(ranked, args.amount, currency_symbol, exchange))
