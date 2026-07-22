"""CLI argument parser and entry point for stock-checker."""

import argparse
import logging

from rich import print as rprint

from stock_checker.dca import calculate_dca_ranking, format_dca_output
from stock_checker.exchanges import EXCHANGES, get_exchange, get_stock_list
from stock_checker.fetcher import fetch_stock_data
from stock_checker.formatter import format_csv, format_json, format_list_table, format_summary
from stock_checker.indicators import calculate_macd, calculate_mas, calculate_rsi, calculate_volume_metrics, determine_signal

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stock-check",
        description="Check stock prices from various exchanges via Yahoo Finance.",
    )
    parser.add_argument(
        "--check",
        help="Stock symbol(s), comma-separated (e.g. BBCA or SPY,QQQ)",
    )
    parser.add_argument(
        "--list",
        help="List all stocks in an index (e.g. idx30, etf)",
    )
    parser.add_argument(
        "--exchange",
        choices=list(EXCHANGES.keys()),
        default="IDX",
        help="Stock exchange: IDX (default), US. Required for non-IDX stocks.",
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
    parser.add_argument(
        "--ma",
        help="Comma-separated MA periods to override defaults "
        "(e.g. --ma 5,20,50,200). Overrides interval-based MA selection.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format: text (default), json, or csv.",
    )
    parser.add_argument(
        "--dca",
        action="store_true",
        help="DCA (Dollar Cost Averaging) analysis mode. "
        "Ranks stocks by technical analysis for monthly investment.",
    )
    parser.add_argument(
        "--amount",
        type=float,
        default=10.0,
        help="Monthly DCA investment amount in local currency (default: 10). Used with --dca flag.",
    )
    parser.add_argument(
        "--screener",
        action="store_true",
        help="Stock screener mode. Scans all IDX stocks and ranks by 3-5 percent profit potential.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top stocks to show in screener mode (default: 20).",
    )
    parser.add_argument(
        "--min-volume",
        type=float,
        default=1_000_000,
        help="Minimum average daily volume in IDR (default: 1000000). Used with --screener.",
    )
    parser.add_argument(
        "--min-price",
        type=float,
        default=50.0,
        help="Minimum stock price in IDR (default: 50). Used with --screener.",
    )
    parser.add_argument(
        "--sector",
        help="Filter by sector (e.g. finance_banking, mining_coal). Used with --screener and --recommend.",
    )
    parser.add_argument(
        "--recommend",
        action="store_true",
        help="Daily recommendation mode. Run screener and show top BUY/STRONG BUY signals.",
    )
    parser.add_argument(
        "--recommend-telegram",
        action="store_true",
        help="Send daily recommendation to Telegram. Used with --recommend.",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=60.0,
        help="Minimum score for recommendations (default: 60 = BUY threshold). Used with --recommend.",
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save recommendation to reports/daily_YYYY-MM-DD.json. Used with --recommend.",
    )
    return parser


def _get_list_choices(exchange: str) -> list[str]:
    """Return available list names for the given exchange."""
    config = get_exchange(exchange)
    return list(config["lists"].keys())


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.check and not args.list and not args.screener and not args.recommend:
        parser.error("either --check, --list, --screener, or --recommend is required")

    if args.recommend:
        _handle_recommend_mode(args)
    elif args.screener:
        _handle_screener_mode(args)
    elif args.list:
        _handle_list_mode(args)
    elif args.dca:
        _handle_dca_mode(args)
    else:
        _handle_check_mode(args)


def _handle_list_mode(args: argparse.Namespace) -> None:
    """Handle --list mode: fetch all stocks and display as table."""
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn

    exchange = args.exchange
    available_lists = _get_list_choices(exchange)

    if args.list not in available_lists:
        rprint(
            f"Error: '{args.list}' is not available for {exchange}. "
            f"Available lists: {', '.join(available_lists)}"
        )
        return

    stocks = get_stock_list(exchange, args.list)
    exchange_config = get_exchange(exchange)
    suffix = exchange_config["suffix"]
    console = Console()
    results: list[dict] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Fetching {args.list.upper()} data...", total=len(stocks))

        for symbol in stocks:
            try:
                data = fetch_stock_data(
                    symbol, days=args.day, interval=args.interval, exchange=exchange
                )
                hist = data.pop("_hist")

                mas = calculate_mas(hist, interval=args.interval)
                signal = determine_signal(data["last_price"], mas)
                rsi = calculate_rsi(hist)

                display_ticker = data["ticker"].replace(suffix, "") if suffix else data["ticker"]

                results.append(
                    {
                        "ticker": display_ticker,
                        "last_price": data["last_price"],
                        "change": data["change"],
                        "change_pct": data["change_pct"],
                        "rsi": rsi,
                        "signal": signal[0],
                    }
                )
            except (ValueError, ConnectionError) as e:
                console.print(f"[yellow]Warning: {symbol} — {e}[/yellow]")
            except Exception as e:
                logger.exception("Unexpected error for %s", symbol)
                console.print(f"[red]Error: {symbol} — {e}[/red]")

            progress.advance(task)

    if results:
        currency_symbol = exchange_config["currency_symbol"]
        console.print(format_list_table(results, currency_symbol=currency_symbol))
    else:
        console.print("[red]No data retrieved.[/red]")


def _handle_check_mode(args: argparse.Namespace) -> None:
    """Handle --check mode: fetch and display individual stock summaries."""
    symbols = [s.strip() for s in args.check.split(",")]
    exchange = args.exchange
    exchange_config = get_exchange(exchange)
    currency_symbol = exchange_config["currency_symbol"]
    exchange_name = exchange_config["name"]

    custom_periods = None
    if args.ma:
        try:
            custom_periods = [int(p.strip()) for p in args.ma.split(",")]
        except ValueError:
            rprint("Error: --ma values must be comma-separated integers (e.g. --ma 5,20,50)")
            return

    for symbol in symbols:
        try:
            data = fetch_stock_data(
                symbol, days=args.day, interval=args.interval, exchange=exchange
            )
            hist = data.pop("_hist")

            mas = calculate_mas(hist, interval=args.interval, custom_periods=custom_periods)
            signal = determine_signal(data["last_price"], mas)
            rsi = calculate_rsi(hist)
            macd = calculate_macd(hist)

            if args.format == "json":
                print(
                    format_json(
                        data,
                        mas,
                        signal,
                        interval=args.interval,
                        rsi=rsi,
                        macd=macd,
                        currency_symbol=currency_symbol,
                        exchange_name=exchange_name,
                    )
                )
            elif args.format == "csv":
                print(
                    format_csv(
                        data,
                        mas,
                        signal,
                        interval=args.interval,
                        rsi=rsi,
                        macd=macd,
                        currency_symbol=currency_symbol,
                        exchange_name=exchange_name,
                    )
                )
            else:
                rprint(
                    format_summary(
                        data,
                        mas,
                        signal,
                        interval=args.interval,
                        rsi=rsi,
                        macd=macd,
                        currency_symbol=currency_symbol,
                        exchange_name=exchange_name,
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


def _handle_dca_mode(args: argparse.Namespace) -> None:
    """Handle --dca mode: DCA analysis with technical ranking."""
    from rich.console import Console

    symbols = [s.strip() for s in args.check.split(",")]
    exchange = args.exchange
    exchange_config = get_exchange(exchange)
    currency_symbol = exchange_config["currency_symbol"]
    console = Console()

    results = []
    for symbol in symbols:
        try:
            data = fetch_stock_data(
                symbol, days=args.day, interval=args.interval, exchange=exchange
            )
            hist = data.pop("_hist")

            mas = calculate_mas(hist, interval=args.interval)
            signal = determine_signal(data["last_price"], mas)
            rsi = calculate_rsi(hist)
            macd = calculate_macd(hist)

            results.append(
                {
                    "ticker": symbol.upper(),
                    "last_price": data["last_price"],
                    "signal": signal,
                    "rsi": rsi,
                    "macd": macd,
                    "mas": mas,
                }
            )
        except (ValueError, ConnectionError) as e:
            console.print(f"[yellow]Warning: {symbol} — {e}[/yellow]")
        except Exception as e:
            logger.exception("Unexpected error for %s", symbol)
            console.print(f"[red]Error: {symbol} — {e}[/red]")

    if not results:
        console.print("[red]No data retrieved.[/red]")
        return

    ranked = calculate_dca_ranking(results, args.amount, exchange)
    console.print(format_dca_output(ranked, args.amount, currency_symbol, exchange))


def _handle_screener_mode(args: argparse.Namespace) -> None:
    """Handle --screener mode: scan all IDX stocks and rank by profit potential."""
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

    from stock_checker.idx_stocks import get_all_idx_stocks, get_idx_stocks_by_sector, get_sector_names
    from stock_checker.screener import calculate_screener_score

    exchange = args.exchange
    exchange_config = get_exchange(exchange)
    currency_symbol = exchange_config["currency_symbol"]
    console = Console()

    console.print("[bold cyan]IDX Stock Screener — Scanning for 3-5% opportunities...[/bold cyan]")
    console.print()

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

    results: list[dict] = []
    errors: list[str] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning stocks...", total=len(all_stocks))

        for symbol in all_stocks:
            try:
                data = fetch_stock_data(
                    symbol, days=args.day, interval=args.interval, exchange=exchange
                )
                hist = data.pop("_hist")
                hist_clean = hist.dropna(subset=["Close", "Open", "High", "Low"])

                if data["last_price"] < args.min_price:
                    progress.advance(task)
                    continue

                mas = calculate_mas(hist_clean, interval=args.interval)
                signal = determine_signal(data["last_price"], mas)
                rsi = calculate_rsi(hist_clean)
                macd = calculate_macd(hist_clean)
                volume_metrics = calculate_volume_metrics(hist_clean)

                # Filter by volume
                if volume_metrics and volume_metrics["avg_volume"] * data["last_price"] < args.min_volume:
                    progress.advance(task)
                    continue

                # Calculate screener score
                score_result = calculate_screener_score(
                    ticker=symbol,
                    last_price=data["last_price"],
                    mas=mas,
                    rsi=rsi,
                    macd=macd,
                    volume_metrics=volume_metrics,
                    hist=hist,
                )

                display_ticker = symbol.upper()

                results.append({
                    "ticker": display_ticker,
                    "last_price": data["last_price"],
                    "change": data["change"],
                    "change_pct": data["change_pct"],
                    "rsi": rsi,
                    "macd": macd,
                    "signal": signal,
                    "score": score_result["score"],
                    "score_label": score_result["signal"],
                })

            except (ValueError, ConnectionError) as e:
                errors.append(f"{symbol}: {e}")
            except Exception as e:
                logger.exception("Unexpected error for %s", symbol)
                errors.append(f"{symbol}: {e}")

            progress.advance(task)

    if not results:
        console.print("[red]No stocks matched the filters.[/red]")
        return

    # Sort by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)

    # Take top N
    top_results = results[:args.top]

    # Format and display
    from stock_checker.formatter import format_screener_table
    console.print(format_screener_table(top_results, currency_symbol, len(all_stocks), len(errors)))

    if errors:
        console.print(f"\n[yellow]Warning: {len(errors)} stocks had errors (skipped)[/yellow]")


def _handle_recommend_mode(args: argparse.Namespace) -> None:
    """Handle --recommend mode: run screener and show top BUY/STRONG BUY signals."""
    from rich.console import Console

    from stock_checker.recommender import (
        format_recommendation_terminal,
        format_recommendation_telegram,
        run_daily_scan,
        save_recommendation,
    )

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


if __name__ == "__main__":
    main()
