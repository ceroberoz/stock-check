"""Terminal output formatting — executive summary with box-drawing."""

import re
from datetime import date

from stock_checker.indicators import _get_period_labels

# Inner content width (sans the ║ borders)
WIDTH = 46

_SIGNAL_COLORS: dict[str, str] = {
    "STRONG BUY": "bold green",
    "BUY": "green",
    "NEUTRAL": "yellow",
    "SELL": "red",
    "STRONG SELL": "bold red",
}

_ACTIONS: dict[str, str] = {
    "STRONG BUY": "HOLD",
    "BUY": "ACCUM",
    "NEUTRAL": "WAIT",
    "SELL": "AVOID",
    "STRONG SELL": "EXIT",
}


def _action_detail(signal_label: str, mas: dict[str, float], lp: float) -> str:
    """One-line action note referencing the key MA level."""
    if not mas:
        return "insufficient data"

    sorted_items = sorted(mas.items(), key=lambda x: int(x[0].replace("MA", "")))

    if signal_label == "STRONG BUY":
        label, val = sorted_items[-1]
        return f"stop {label} {val:,.0f}"
    elif signal_label == "BUY":
        label, val = sorted_items[-1]
        return f"need {label} {val:,.0f}"
    elif signal_label == "NEUTRAL":
        return "await MA crossover"
    elif signal_label == "SELL":
        for label, val in sorted_items:
            if val > lp:
                return f"resist {label} {val:,.0f}"
        label, val = sorted_items[-1]
        return f"resist {label} {val:,.0f}"
    elif signal_label == "STRONG SELL":
        label, val = sorted_items[0]
        return f"resist {label} {val:,.0f}"
    return ""


def _sep(char: str = "═") -> str:
    return f"║{char * WIDTH}║"


def _kv(label: str, value: str, label_w: int = 12) -> str:
    val_w = WIDTH - label_w - 6
    return f"║  {label:<{label_w}}: {value:<{val_w}}  ║"


def _title(text: str) -> str:
    return f"║  {text:^{WIDTH - 4}}  ║"


def _section_header(text: str) -> str:
    return f"║  {text:<{WIDTH - 4}}  ║"


def _colorize(lines: list[str], data: dict, signal: tuple[str, str], **kwargs: object) -> list[str]:
    """Apply rich markup to rendered lines for terminal color.

    Colors are applied *after* alignment so padding stays correct — rich
    renders markup tags as zero-width.
    """
    change = data.get("change", 0)
    change_color = "green" if change >= 0 else "red"
    signal_label = signal[0]
    action_label = _ACTIONS.get(signal_label, "")

    colored: list[str] = []
    for line in lines:
        # Change value + percentage
        if "Change" in line and ":" in line:
            m = re.search(r"[+-]?[\d,]+\.?\d*\s*\([+-]?\d+\.\d+%\)", line)
            if m:
                wrapped = f"[{change_color}]{m.group()}[/{change_color}]"
                line = line[: m.start()] + wrapped + line[m.end() :]

        # RSI status color
        elif "RSI" in line and ("overbought" in line or "oversold" in line or "neutral" in line):
            if "overbought" in line:
                line = line.replace("overbought", "[red]overbought[/red]")
            elif "oversold" in line:
                line = line.replace("oversold", "[green]oversold[/green]")
            elif "neutral" in line:
                line = line.replace("neutral", "[yellow]neutral[/yellow]")

        # MACD: MACD arrows and trend labels
        elif "MACD" in line and "▲" in line and "bullish" in line:
            line = line.replace("▲  bullish", "[green]▲  bullish[/green]")
        elif "MACD" in line and "▼" in line and "bearish" in line:
            line = line.replace("▼  bearish", "[red]▼  bearish[/red]")

        # MA arrows and trend labels
        elif "▲" in line and "bullish" in line:
            line = line.replace("▲  bullish", "[green]▲  bullish[/green]")
        elif "▼" in line and "bearish" in line:
            line = line.replace("▼  bearish", "[red]▼  bearish[/red]")

        # Signal / Action lines
        elif signal_label in line or action_label in line:
            sig_color = _SIGNAL_COLORS.get(signal_label, "")
            if sig_color:
                if signal_label in line:
                    line = line.replace(signal_label, f"[{sig_color}]{signal_label}[/{sig_color}]")
                if action_label in line:
                    line = line.replace(action_label, f"[{sig_color}]{action_label}[/{sig_color}]")

        colored.append(line)
    return colored


def _rsi_status(rsi: float) -> str:
    """Classify RSI as overbought (>70), oversold (<30), or neutral."""
    if rsi >= 70:
        return "overbought"
    if rsi <= 30:
        return "oversold"
    return "neutral"


def format_summary(
    data: dict,
    mas: dict[str, float],
    signal: tuple[str, str],
    interval: str = "1d",
    rsi: float | None = None,
    macd: dict[str, float] | None = None,
) -> str:
    """Build the full executive summary box table with rich markup."""
    today = date.today().isoformat()
    lp = data["last_price"]
    period_labels = _get_period_labels(interval)
    lines: list[str] = []

    # ── top ──
    lines.append("╔" + "═" * WIDTH + "╗")
    lines.append(_title("IDX Stock Checker — Executive Summary"))
    lines.append("╠" + "═" * WIDTH + "╣")

    # ── metadata ──
    lines.append(_kv("Ticker", data["ticker"]))
    lines.append(_kv("Exchange", "Jakarta Stock Exchange"))
    lines.append(_kv("Date", today))
    lines.append(_kv("Period", data["period"]))
    lines.append(_kv("Interval", interval))

    lines.append(_sep("─"))

    # ── price snapshot ──
    change_str = f"{data['change']:+,.0f} ({data['change_pct']:+.2f}%)"
    lines.append(_kv("Last Price", f"Rp {lp:,.0f}"))
    lines.append(_kv("Change", change_str))
    lines.append(_kv("Open / High", f"{data['open']:,.0f} / {data['high']:,.0f}"))
    lines.append(_kv("Low / Close", f"{data['low']:,.0f} / {data['close']:,.0f}"))

    lines.append(_sep("─"))

    # ── moving averages ──
    lines.append(_section_header("Moving Averages (MA)"))

    for label, value in mas.items():
        period_lbl = period_labels.get(label, "")
        arrow = "▲" if lp >= value else "▼"
        trend = "bullish" if lp >= value else "bearish"
        ma_text = f"  {label:4s} ({period_lbl}) : {value:>8,.0f}  {arrow}  {trend}"
        lines.append(f"║  {ma_text:<{WIDTH - 4}}  ║")

    lines.append(_sep("─"))

    # ── oscillators (RSI / MACD) ──
    if rsi is not None or macd is not None:
        lines.append(_section_header("Oscillators"))

    if rsi is not None:
        rsi_label = _rsi_status(rsi)
        rsi_text = f"  RSI(14)     : {rsi:>7.2f}  {rsi_label}"
        lines.append(f"║  {rsi_text:<{WIDTH - 4}}  ║")

    if macd is not None:
        hist_val = macd["histogram"]
        macd_arrow = "▲" if hist_val >= 0 else "▼"
        macd_trend = "bullish" if hist_val >= 0 else "bearish"
        macd_text = f"  MACD(12/26/9) : {hist_val:>+8,.0f}  {macd_arrow}  {macd_trend}"
        lines.append(f"║  {macd_text:<{WIDTH - 4}}  ║")

    lines.append(_sep("─"))

    # ── signal ──
    signal_label, signal_desc = signal
    signal_text = f"  Signal : {signal_label}  ({signal_desc})"
    lines.append(f"║{signal_text:^{WIDTH}}║")

    # ── action recommendation ──
    action_label = _ACTIONS.get(signal_label, "")
    action_detail = _action_detail(signal_label, mas, data["last_price"])
    action_text = f"  Action : {action_label}  ({action_detail})"
    lines.append(f"║{action_text:^{WIDTH}}║")

    # ── bottom ──
    lines.append("╚" + "═" * WIDTH + "╝")

    return "\n".join(_colorize(lines, data, signal, rsi=rsi, macd=macd))


def format_list_table(results: list[dict]) -> str:
    """Format a list of stock results as a Rich table string."""
    from rich.table import Table
    from rich.text import Text

    table = Table(
        title="IDX30 Stock Overview",
        show_header=True,
        header_style="bold cyan",
        show_lines=False,
    )

    table.add_column("Ticker", style="bold", width=8)
    table.add_column("Last Price", justify="right", width=12)
    table.add_column("Change", justify="right", width=14)
    table.add_column("RSI", justify="right", width=10)
    table.add_column("Signal", width=14)
    table.add_column("Action", width=10)

    signal_styles = {
        "STRONG BUY": "bold green",
        "BUY": "green",
        "NEUTRAL": "yellow",
        "SELL": "red",
        "STRONG SELL": "bold red",
    }

    for r in results:
        change_color = "green" if r["change"] >= 0 else "red"
        change_str = f"{r['change']:+,.0f} ({r['change_pct']:+.1f}%)"
        change_text = Text(change_str, style=change_color)

        rsi_val = f"{r['rsi']:.1f}" if r["rsi"] is not None else "—"

        signal_label = r["signal"]
        signal_style = signal_styles.get(signal_label, "")
        signal_text = Text(signal_label, style=signal_style)

        action_label = _ACTIONS.get(signal_label, "WATCH")
        action_text = Text(action_label, style=signal_style)

        table.add_row(
            r["ticker"],
            f"Rp {r['last_price']:,.0f}",
            change_text,
            rsi_val,
            signal_text,
            action_text,
        )

    from io import StringIO
    from rich.console import Console

    buf = StringIO()
    console = Console(file=buf, width=80)
    console.print(table)
    return buf.getvalue()


def format_json(
    data: dict,
    mas: dict[str, float],
    signal: tuple[str, str],
    interval: str = "1d",
    rsi: float | None = None,
    macd: dict[str, float] | None = None,
) -> str:
    """Format stock data as JSON."""
    import json
    from datetime import date

    output = {
        "ticker": data["ticker"],
        "exchange": "Jakarta Stock Exchange",
        "date": date.today().isoformat(),
        "period": data["period"],
        "interval": interval,
        "price": {
            "last": data["last_price"],
            "change": data["change"],
            "change_pct": data["change_pct"],
            "open": data["open"],
            "high": data["high"],
            "low": data["low"],
            "close": data["close"],
        },
        "moving_averages": mas,
        "signal": {
            "label": signal[0],
            "description": signal[1],
        },
    }

    if rsi is not None:
        output["rsi"] = rsi

    if macd is not None:
        output["macd"] = macd

    return json.dumps(output, indent=2)


def format_csv(
    data: dict,
    mas: dict[str, float],
    signal: tuple[str, str],
    interval: str = "1d",
    rsi: float | None = None,
    macd: dict[str, float] | None = None,
) -> str:
    """Format stock data as CSV."""
    from datetime import date

    lines = []

    lines.append(
        "ticker,exchange,date,period,interval,last_price,change,change_pct,open,high,low,close,signal,signal_description,rsi,macd_histogram"
    )

    rsi_val = f"{rsi}" if rsi is not None else ""
    macd_hist = f"{macd['histogram']}" if macd is not None else ""

    line = (
        f"{data['ticker']},"
        f"Jakarta Stock Exchange,"
        f"{date.today().isoformat()},"
        f"{data['period']},"
        f"{interval},"
        f"{data['last_price']},"
        f"{data['change']},"
        f"{data['change_pct']},"
        f"{data['open']},"
        f"{data['high']},"
        f"{data['low']},"
        f"{data['close']},"
        f"{signal[0]},"
        f"{signal[1]},"
        f"{rsi_val},"
        f"{macd_hist}"
    )
    lines.append(line)

    return "\n".join(lines)
