"""CLI argument parser and entry point for stock-checker."""

import argparse

from stock_checker.exchanges import EXCHANGES

# Command imports are lazy (inside main) to keep startup fast.


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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.check and not args.list and not args.screener and not args.recommend:
        parser.error("either --check, --list, --screener, or --recommend is required")

    # Lazy imports for fast startup
    if args.recommend:
        from stock_checker.commands.recommend import run
        run(args)
    elif args.screener:
        from stock_checker.commands.screener import run
        run(args)
    elif args.list:
        from stock_checker.commands.list_cmd import run
        run(args)
    elif args.dca:
        from stock_checker.commands.dca import run
        run(args)
    else:
        from stock_checker.commands.check import run
        run(args)


if __name__ == "__main__":
    main()
