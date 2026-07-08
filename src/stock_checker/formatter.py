"""Terminal output formatting — executive summary with box-drawing."""

from datetime import date

from stock_checker.indicators import _get_period_labels

# Inner content width (sans the ║ borders)
WIDTH = 46


def _sep(char: str = "═") -> str:
    return f"║{char * WIDTH}║"


def _kv(label: str, value: str, label_w: int = 12) -> str:
    """Render a key-value row inside the box."""
    val_w = WIDTH - label_w - 6
    return f"║  {label:<{label_w}}: {value:<{val_w}}  ║"


def _title(text: str) -> str:
    return f"║  {text:^{WIDTH - 4}}  ║"


def _section_header(text: str) -> str:
    """Render a full-width section label (no colon)."""
    return f"║  {text:<{WIDTH - 4}}  ║"


def format_summary(
    data: dict,
    mas: dict[str, float],
    signal: tuple[str, str],
    interval: str = "1d",
) -> str:
    """Build the full executive summary box table to stdout."""
    today = date.today().isoformat()
    signal_label, signal_desc = signal
    lp = data["last_price"]
    period_labels = _get_period_labels(interval)
    lines: list[str] = []

    # ── top ──
    lines.append("╔" + "═" * WIDTH + "╗")
    lines.append(_title("IDX Stock Checker — Executive Summary"))
    lines.append("╠" + "═" * WIDTH + "╣")

    # ── header metadata ──
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
    lines.append(
        _kv("Open / High", f"{data['open']:,.0f} / {data['high']:,.0f}")
    )
    lines.append(
        _kv("Low / Close", f"{data['low']:,.0f} / {data['close']:,.0f}")
    )

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
    signal_text = f"  Signal : {signal_label}  ({signal_desc})"
    lines.append(f"║{signal_text:^{WIDTH}}║")

    # ── bottom ──
    lines.append("╚" + "═" * WIDTH + "╝")

    return "\n".join(lines)
