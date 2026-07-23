"""Handle --recommend mode: run screener and show top BUY/STRONG BUY signals."""

from __future__ import annotations

import argparse
import logging

from stock_checker.exchanges import get_exchange

logger = logging.getLogger(__name__)


def run(args: argparse.Namespace) -> None:
    """Execute --recommend mode."""
    from rich.console import Console

    from stock_checker.formatter import format_recommendation_terminal
    from stock_checker.notifier import format_recommendation_telegram
    from stock_checker.screener import run_daily_scan, save_recommendation

    exchange = args.exchange
    exchange_config = get_exchange(exchange)
    currency_symbol = exchange_config["currency_symbol"]
    console = Console()

    console.print("[bold cyan]📊 Running daily recommendation scan...[/bold cyan]")
    console.print()

    try:
        rec = run_daily_scan(
            sector=args.sector,
            min_score=args.min_score,
            top_n=args.top,
            min_volume=args.min_volume,
            min_price=args.min_price,
        )
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    except Exception as e:
        logger.exception("Unexpected error during scan")
        console.print(f"[red]Error during scan: {e}[/red]")
        return

    console.print(format_recommendation_terminal(rec, currency_symbol))

    if args.save_report:
        filepath = save_recommendation(rec)
        console.print(f"[green]Report saved to: {filepath}[/green]")

    if args.recommend_telegram:
        from stock_checker.config import load_config
        from stock_checker.notifier import send_telegram_text

        config = load_config("config.yaml")
        message = format_recommendation_telegram(rec)

        console.print("[cyan]Sending to Telegram...[/cyan]")
        ok = send_telegram_text(
            config.telegram.bot_token,
            config.telegram.chat_id,
            message,
        )
        if ok:
            console.print("[green]✓ Recommendation sent to Telegram[/green]")
        else:
            console.print("[red]✗ Failed to send to Telegram — check bot_token and chat_id[/red]")
