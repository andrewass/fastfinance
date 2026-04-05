from .statisticsresponses import SymbolStatistics
from ..integration.yfinanceclient import call_ticker, raise_upstream_data_error


def require_fields(info: dict, symbol: str, fields: tuple[str, ...], context: str):
    missing = [field for field in fields if info.get(field) is None]
    if missing:
        raise_upstream_data_error(symbol, context, missing)


def get_financial_details(symbol: str):
    info = call_ticker(symbol, "statistics.details", lambda ticker: ticker.info)
    require_fields(
        info,
        symbol,
        ("shortName", "marketCap", "currency", "priceToBook", "trailingPE", "trailingEps"),
        "statistics.details",
    )
    dividend_rate = info.get("dividendRate")
    dividend_yield = info.get("dividendYield")
    return SymbolStatistics(
        symbol=symbol,
        companyName=info.get("shortName"),
        marketCap=info.get("marketCap"),
        currency=info.get("currency"),
        priceToBook=info.get("priceToBook"),
        priceToEarnings=info.get("trailingPE"),
        earningsPerShare=info.get("trailingEps"),
        dividendRate=dividend_rate if dividend_rate is not None else None,
        dividendYieldPercentage=dividend_yield * 100 if dividend_yield is not None else None
    )
