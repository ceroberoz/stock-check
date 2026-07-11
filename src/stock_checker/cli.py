"""CLI argument parser and entry point for stock-checker."""

import argparse
import logging

from rich import print as rprint

from stock_checker.dca import calculate_dca_ranking, format_dca_output
from stock_checker.exchanges import EXCHANGES, get_exchange, get_stock_list
from stock_checker.fetcher import fetch_stock_data
from stock_checker.formatter import format_csv, format_json, format_list_table, format_summary
from stock_checker.indicators import calculate_macd, calculate_mas, calculate_rsi, determine_signal

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
    return parser


def _get_list_choices(exchange: str) -> list[str]:
    """Return available list names for the given exchange."""
    config = get_exchange(exchange)
    return list(config["lists"].keys())


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.check and not args.list:
        parser.error("either --check or --list is required")

    if args.list:
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
        console.print(format_list_table(results))
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


if __name__ == "__main__":
    main()
