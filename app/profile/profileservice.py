import yfinance as yf
from .profileresponses import Profile


def get_profile(symbol: str):
    info = yf.Ticker(symbol).info
    return Profile(
        companyName=info.get("shortName"),
        address=info.get("address1"),
        city=info.get("city"),
        country=info.get("country"),
        state=info.get("state"),
        industry=info.get("industry"),
        sector=info.get("sector"),
        businessSummary=info.get("longBusinessSummary"),
        website=info.get("website"),
        zip=info.get("zip"),
        fullTimeEmployees=info.get("fullTimeEmployees")
    )
