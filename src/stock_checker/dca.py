"""DCA (Dollar Cost Averaging) analysis — technical analysis-based ranking."""

from __future__ import annotations


def calculate_dca_ranking(results: list[dict]) -> list[dict]:
    """Rank stocks for DCA based on technical analysis.

    Scoring factors:
    - Signal strength (40 points max)
    - RSI position (30 points max) — prefer 40-60 (neutral)
    - MACD momentum (20 points max)
    - MA alignment (10 points max)

    Parameters
    ----------
    results :
        List of stock data dicts with keys: ticker, last_price, signal, rsi, macd, mas.

    Returns
    -------
        Sorted list with added 'score' and 'rank' fields.
    """
    scored = []

    for r in results:
        score = 0

        signal_label = r["signal"][0]
        signal_score = _score_signal(signal_label)
        score += signal_score

        rsi = r.get("rsi")
        if rsi is not None:
            rsi_score = _score_rsi(rsi)
            score += rsi_score

        macd = r.get("macd")
        if macd is not None:
            macd_score = _score_macd(macd)
            score += macd_score

        mas = r.get("mas", {})
        if mas:
            ma_score = _score_ma_alignment(r["last_price"], mas)
            score += ma_score

        r["score"] = round(score, 1)
        scored.append(r)

    scored.sort(key=lambda x: x["score"], reverse=True)

    for i, r in enumerate(scored, 1):
        r["rank"] = i

    return scored


def _score_signal(label: str) -> float:
    """Score based on signal strength (0-40 points)."""
    scores = {
        "STRONG BUY": 40,
        "BUY": 30,
        "NEUTRAL": 15,
        "SELL": 5,
        "STRONG SELL": 0,
    }
    return scores.get(label, 15)


def _score_rsi(rsi: float) -> float:
    """Score based on RSI position (0-30 points).

    Prefer 40-60 (neutral zone) — room to grow without being overbought.
    """
    if 40 <= rsi <= 60:
        return 30
    elif 30 <= rsi < 40:
        return 20
    elif 60 < rsi <= 70:
        return 15
    elif rsi < 30:
        return 10
    else:
        return 5


def _score_macd(macd: dict) -> float:
    """Score based on MACD momentum (0-20 points)."""
    histogram = macd.get("histogram", 0)
    if histogram > 0:
        return min(20, 10 + histogram / 5)
    else:
        return max(0, 10 + histogram / 5)


def _score_ma_alignment(price: float, mas: dict[str, float]) -> float:
    """Score based on how many MAs price is above (0-10 points)."""
    if not mas:
        return 5
    above = sum(1 for v in mas.values() if price >= v)
    total = len(mas)
    return (above / total) * 10


def format_dca_output(ranked: list[dict], amount: float, currency_symbol: str) -> str:
    """Format DCA analysis output as a rich box table."""
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    WIDTH = 60

    lines = []
    lines.append("╔" + "═" * WIDTH + "╗")
    lines.append(f"║{'DCA Analysis':^{WIDTH}}║")
    lines.append("╠" + "═" * WIDTH + "╣")
    lines.append(f"║  Monthly Investment: {currency_symbol} {amount:,.2f}{'':<{WIDTH - 28}}║")
    lines.append("║" + "─" * WIDTH + "║")

    table = Table(
        show_header=True, header_style="bold cyan", show_lines=False, box=None, padding=(0, 1)
    )
    table.add_column("Ticker", style="bold", width=8)
    table.add_column("Price", justify="right", width=12)
    table.add_column("Signal", width=12)
    table.add_column("RSI", justify="right", width=8)
    table.add_column("MACD", justify="right", width=10)
    table.add_column("Score", justify="right", width=8)
    table.add_column("Rank", justify="right", width=6)

    signal_styles = {
        "STRONG BUY": "bold green",
        "BUY": "green",
        "NEUTRAL": "yellow",
        "SELL": "red",
        "STRONG SELL": "bold red",
    }

    for r in ranked:
        signal_label = r["signal"][0]
        signal_style = signal_styles.get(signal_label, "")
        signal_text = Text(signal_label, style=signal_style)

        rsi_val = f"{r['rsi']:.1f}" if r.get("rsi") is not None else "—"

        macd = r.get("macd")
        if macd is not None:
            hist = macd["histogram"]
            macd_str = f"{hist:+.1f}"
            macd_style = "green" if hist >= 0 else "red"
            macd_text = Text(macd_str, style=macd_style)
        else:
            macd_text = Text("—")

        score_text = Text(f"{r['score']:.0f}", style="bold")
        rank_text = Text(f"#{r['rank']}", style="bold" if r["rank"] == 1 else "")

        table.add_row(
            r["ticker"],
            f"{currency_symbol} {r['last_price']:,.2f}",
            signal_text,
            rsi_val,
            macd_text,
            score_text,
            rank_text,
        )

    from io import StringIO

    buf = StringIO()
    console = Console(file=buf, width=WIDTH + 4)
    console.print(table)
    table_str = buf.getvalue()

    for line in table_str.rstrip().split("\n"):
        lines.append(f"║  {line:<{WIDTH - 4}}  ║")

    lines.append("║" + "─" * WIDTH + "║")

    winner = ranked[0]
    rec = (
        f"  Recommendation: {winner['ticker']}\n"
        f"  - Best signal: {winner['signal'][0]}\n"
        f"  - RSI: {winner.get('rsi', 'N/A')}\n"
        f"  - Score: {winner['score']:.0f}/100"
    )
    for line in rec.split("\n"):
        lines.append(f"║  {line:<{WIDTH - 4}}  ║")

    lines.append("╚" + "═" * WIDTH + "╝")

    from io import StringIO as SIO

    buf2 = SIO()
    c = Console(file=buf2, width=WIDTH + 4)
    c.print("\n".join(lines))
    return buf2.getvalue()
