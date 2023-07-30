import yfinance as yf

from .financialsresponses import SymbolFinancials


def get_financial_details(symbol: str):
    info = yf.Ticker(symbol).info
    dividend_rate = info.get("dividendRate")
    dividend_yield = info.get("dividendYield")
    return SymbolFinancials(
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
