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


def _sep(char: str = "═") -> str:
    return f"║{char * WIDTH}║"


def _kv(label: str, value: str, label_w: int = 12) -> str:
    val_w = WIDTH - label_w - 6
    return f"║  {label:<{label_w}}: {value:<{val_w}}  ║"


def _title(text: str) -> str:
    return f"║  {text:^{WIDTH - 4}}  ║"


def _section_header(text: str) -> str:
    return f"║  {text:<{WIDTH - 4}}  ║"


def _colorize(lines: list[str], data: dict, signal: tuple[str, str]) -> list[str]:
    """Apply rich markup to rendered lines for terminal color.

    Colors are applied *after* alignment so padding stays correct — rich
    renders markup tags as zero-width.
    """
    change = data.get("change", 0)
    change_color = "green" if change >= 0 else "red"
    signal_label = signal[0]

    colored: list[str] = []
    for line in lines:
        # Change value + percentage
        if "Change" in line and ":" in line:
            m = re.search(r"[+-]?[\d,]+\.?\d*\s*\([+-]?\d+\.\d+%\)", line)
            if m:
                wrapped = f"[{change_color}]{m.group()}[/{change_color}]"
                line = line[: m.start()] + wrapped + line[m.end() :]

        # MA arrows and trend labels
        elif "▲" in line and "bullish" in line:
            line = line.replace("▲  bullish", "[green]▲  bullish[/green]")
        elif "▼" in line and "bearish" in line:
            line = line.replace("▼  bearish", "[red]▼  bearish[/red]")

        # Signal line
        elif signal_label in line:
            sig_color = _SIGNAL_COLORS.get(signal_label, "")
            if sig_color:
                line = line.replace(
                    signal_label, f"[{sig_color}]{signal_label}[/{sig_color}]"
                )

        colored.append(line)
    return colored


def format_summary(
    data: dict,
    mas: dict[str, float],
    signal: tuple[str, str],
    interval: str = "1d",
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

    # ── signal ──
    signal_label, signal_desc = signal
    signal_text = f"  Signal : {signal_label}  ({signal_desc})"
    lines.append(f"║{signal_text:^{WIDTH}}║")

    # ── bottom ──
    lines.append("╚" + "═" * WIDTH + "╝")

    return "\n".join(_colorize(lines, data, signal))
