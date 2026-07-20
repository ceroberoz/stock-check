"""DCA (Dollar Cost Averaging) analysis — technical analysis-based ranking."""

from __future__ import annotations


def calculate_dca_ranking(
    results: list[dict], amount: float = 0, exchange: str = "IDX"
) -> list[dict]:
    """Rank stocks for DCA based on technical analysis and compute allocation.

    Scoring factors:
    - Signal strength (40 points max)
    - RSI position (30 points max) — prefer 40-60 (neutral)
    - MACD momentum (20 points max)
    - MA alignment (10 points max)

    Parameters
    ----------
    results :
        List of stock data dicts with keys: ticker, last_price, signal, rsi, macd, mas.
    amount :
        Monthly investment amount for allocation calculation.
    exchange :
        Exchange code (IDX or US). IDX uses lots of 100 shares, US allows fractional.

    Returns
    -------
        Sorted list with added 'score', 'rank', and 'allocation' fields.
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

    if amount > 0 and len(scored) > 0:
        total_score = sum(r["score"] for r in scored)
        if total_score > 0:
            for r in scored:
                allocation = (r["score"] / total_score) * amount
                r["allocation"] = round(allocation, 2)
                price = r.get("last_price", 0)

                if exchange == "IDX":
                    lot_price = price * 100
                    if lot_price > 0:
                        r["lots"] = int(allocation // lot_price)
                        r["shares"] = r["lots"] * 100
                        r["actual_cost"] = r["shares"] * price
                    else:
                        r["lots"] = 0
                        r["shares"] = 0
                        r["actual_cost"] = 0
                else:
                    if price > 0:
                        r["shares"] = round(allocation / price, 4)
                        r["actual_cost"] = r["shares"] * price
                    else:
                        r["shares"] = 0
                        r["actual_cost"] = 0

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


def format_dca_output(
    ranked: list[dict], amount: float, currency_symbol: str, exchange: str = "IDX"
) -> str:
    """Format DCA analysis output as a rich box table."""
    WIDTH = 76

    lines = []
    lines.append("╔" + "═" * WIDTH + "╗")
    lines.append(f"║{'DCA Analysis':^{WIDTH}}║")
    lines.append("╠" + "═" * WIDTH + "╣")
    lines.append(f"║  Monthly Investment: {currency_symbol} {amount:,.2f}{'':<{WIDTH - 28}}║")
    lines.append("║" + "─" * WIDTH + "║")

    if exchange == "IDX":
        header = f"  {'Ticker':<8} {'Price':>10}  {'Signal':<12} {'RSI':>5} {'MACD':>7} {'Score':>6} {'Alloc':>12} {'Lots':>6}"
    else:
        header = f"  {'Ticker':<8} {'Price':>10}  {'Signal':<12} {'RSI':>5} {'MACD':>7} {'Score':>6} {'Alloc':>10} {'Shares':>8}"
    lines.append(f"║{header:<{WIDTH}}║")

    for r in ranked:
        signal_label = r["signal"][0]

        rsi_val = f"{r['rsi']:.1f}" if r.get("rsi") is not None else "—"

        macd = r.get("macd")
        if macd is not None:
            hist = macd["histogram"]
            macd_str = f"{hist:+.1f}"
        else:
            macd_str = "—"

        alloc = r.get("allocation", 0)

        if exchange == "IDX":
            lots = r.get("lots", 0)
            alloc_text = f"{currency_symbol}{alloc:>10,.0f}"
            shares_text = f"{lots}"
            row = f"  {r['ticker']:<8} {currency_symbol}{r['last_price']:>8,.2f}  {signal_label:<12} {rsi_val:>5} {macd_str:>7} {r['score']:>6.0f} {alloc_text} {shares_text:>6}"
        else:
            shares = r.get("shares", 0)
            row = f"  {r['ticker']:<8} {currency_symbol}{r['last_price']:>8,.2f}  {signal_label:<12} {rsi_val:>5} {macd_str:>7} {r['score']:>6.0f} {currency_symbol}{alloc:>8,.2f} {shares:>8.4f}"

        lines.append(f"║{row:<{WIDTH}}║")

    lines.append("║" + "─" * WIDTH + "║")

    winner = ranked[0]
    rec_lines = []
    rec_lines.append("  Recommended Allocation:")
    rec_lines.append(
        f"  - Top pick: {winner['ticker']} ({currency_symbol} {winner.get('actual_cost', 0):,.0f})"
    )
    rec_lines.append(
        f"  - Best signal: {winner['signal'][0]} | RSI: {winner.get('rsi', 'N/A')} | Score: {winner['score']:.0f}/100"
    )

    if exchange == "IDX":
        total_lots = sum(r.get("lots", 0) for r in ranked)
        total_cost = sum(r.get("actual_cost", 0) for r in ranked)
        remaining = amount - total_cost
        rec_lines.append(
            f"  - Total: {total_lots} lots | Cost: {currency_symbol} {total_cost:,.0f} | Remaining: {currency_symbol} {remaining:,.0f}"
        )
    else:
        rec_lines.append("  - Allocation based on weighted technical scores")

    for line in rec_lines:
        lines.append(f"║  {line:<{WIDTH - 4}}  ║")

    lines.append("╚" + "═" * WIDTH + "╝")

    return "\n".join(lines) + "\n"
