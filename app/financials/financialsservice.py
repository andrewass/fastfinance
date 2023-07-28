import yfinance as yf

from .financialsresponses import SymbolFinancials


def get_financial_details(symbol: str):
    info = yf.Ticker(symbol).info
    return SymbolFinancials(
        symbol=symbol,
        marketCap=info.get("marketCap"),
        currency=info.get("currency"),
        priceToBook=info.get("priceToBook"),
        priceToEarningsRatio=info.get("trailingPE"),
        earningsPerShare=info.get("trailingEps"),
        dividendRate=info.get("dividendRate"),
        dividendYieldPercentage=info.get("dividendYield") * 100
    )
