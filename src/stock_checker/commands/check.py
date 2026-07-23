"""Handle --check mode: fetch and display individual stock summaries."""

from __future__ import annotations

import argparse
import logging

from rich import print as rprint

from stock_checker.exchanges import get_exchange
from stock_checker.formatter import format_csv, format_json, format_summary
from stock_checker.indicators import calculate_mas, calculate_macd, calculate_rsi, determine_signal
from stock_checker.fetcher import fetch_stock_data

logger = logging.getLogger(__name__)


def run(args: argparse.Namespace) -> None:
    """Execute --check mode."""
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
