"""Exchange registry — defines supported exchanges and their properties."""

from __future__ import annotations


EXCHANGES: dict[str, dict] = {
    "IDX": {
        "suffix": ".JK",
        "name": "Jakarta Stock Exchange",
        "currency": "IDR",
        "currency_symbol": "Rp",
        "default": True,
        "lists": {
            "idx30": [
                "AADI",
                "ADMR",
                "ADRO",
                "AMRT",
                "ANTM",
                "ASII",
                "BBCA",
                "BBNI",
                "BBRI",
                "BMRI",
                "BRPT",
                "BUMI",
                "CPIN",
                "EMTK",
                "GOTO",
                "ICBP",
                "INCO",
                "INDF",
                "INKP",
                "JPFA",
                "KLBF",
                "MBMA",
                "MDKA",
                "MEDC",
                "PGAS",
                "PGEO",
                "PTBA",
                "TLKM",
                "UNTR",
                "UNVR",
            ],
        },
    },
    "US": {
        "suffix": "",
        "name": "US Market",
        "currency": "USD",
        "currency_symbol": "$",
        "default": False,
        "lists": {
            "etf": [
                "SPY",
                "QQQ",
                "VOO",
                "VTI",
                "SCHG",
                "SCHD",
                "IVV",
                "DIA",
                "QQQM",
                "VXUS",
                "VEA",
                "VWO",
                "AGG",
                "BND",
                "BNDX",
                "GLD",
                "VNQ",
                "IWM",
                "VTV",
                "VUG",
            ],
        },
    },
}


def get_exchange(exchange: str) -> dict:
    """Return exchange config for the given exchange code.

    Raises KeyError if exchange is not supported.
    """
    return EXCHANGES[exchange.upper()]


def ensure_suffix(symbol: str, exchange: str) -> str:
    """Append the appropriate suffix for the given exchange.

    Parameters
    ----------
    symbol :
        Stock symbol (e.g. "BBCA", "SPY").
    exchange :
        Exchange code (e.g. "IDX", "US").

    Returns
    -------
        Symbol with suffix (e.g. "BBCA.JK", "SPY").
    """
    config = get_exchange(exchange)
    suffix = config["suffix"]
    s = symbol.strip().upper()
    if suffix and not s.endswith(suffix):
        s += suffix
    return s


def get_stock_list(exchange: str, list_name: str) -> list[str]:
    """Return a stock list for the given exchange and list name.

    Raises KeyError if exchange or list name is not found.
    """
    config = get_exchange(exchange)
    return config["lists"][list_name]


def get_currency_symbol(exchange: str) -> str:
    """Return the currency symbol for the given exchange."""
    config = get_exchange(exchange)
    return config["currency_symbol"]
