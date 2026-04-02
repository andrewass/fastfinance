import yfinance as yf
from fastapi import HTTPException

from .profileresponses import Profile
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


def get_profile(symbol: str):
    info = call_yfinance(symbol, "profile.details", lambda: yf.Ticker(symbol).info)
    require_fields(
        info,
        symbol,
        (
            "shortName",
            "address1",
            "city",
            "state",
            "zip",
            "country",
            "website",
            "industry",
            "sector",
            "longBusinessSummary",
            "fullTimeEmployees",
        ),
        "profile.details",
    )
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
