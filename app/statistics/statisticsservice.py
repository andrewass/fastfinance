import yfinance as yf
from fastapi import HTTPException

from .statisticsresponses import SymbolStatistics
from ..integration.yfinanceclient import call_yfinance


def require_fields(info: dict, symbol: str, fields: tuple[str, ...], context: str):
    missing = [field for field in fields if info.get(field) is None]
    if missing:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Missing expected fields from upstream provider",
                "provider": "yfinance",
                "context": context,
                "symbol": symbol,
                "missingFields": missing,
            },
        )


def get_financial_details(symbol: str):
    info = call_yfinance(symbol, "statistics.details", lambda: yf.Ticker(symbol).info)
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
