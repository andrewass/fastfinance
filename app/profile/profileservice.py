from .profileresponses import Profile
from ..integration.yfinanceclient import call_ticker, raise_upstream_data_error


def require_fields(info: dict, symbol: str, fields: tuple[str, ...], context: str):
    missing = [field for field in fields if info.get(field) is None]
    if missing:
        raise_upstream_data_error(symbol, context, missing)


def get_profile(symbol: str):
    info = call_ticker(symbol, "profile.details", lambda ticker: ticker.info)
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
