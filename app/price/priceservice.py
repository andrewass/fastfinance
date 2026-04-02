from datetime import timedelta
from typing import Any

from fastapi import HTTPException
from pandas import DataFrame, Timestamp

from .pricerequests import Period
from .priceresponses import HistoricalPrice, CurrentPrice, HistoricalPricesResponse
from ..cache.cachedecorator import simple_cache
from ..integration.yfinanceclient import call_ticker


def require_fields(info: dict[str, Any], symbol: str, fields: tuple[str, ...], context: str):
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


def get_current_price(symbol: str):
    info = call_ticker(symbol, "price.current", lambda ticker: ticker.info)
    require_fields(
        info,
        symbol,
        ("shortName", "currentPrice", "previousClose", "currency"),
        "price.current",
    )
    return CurrentPrice(
        symbol=symbol,
        companyName=info.get("shortName"),
        currentPrice=info.get("currentPrice"),
        previousClose=info.get("previousClose"),
        currency=info.get("currency")
    )


@simple_cache(expire=timedelta(minutes=10))
def get_historical_prices(symbol: str, period: Period):
    history = call_ticker(symbol, "price.historical", lambda ticker: ticker.history(period=period))
    if history.empty:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Missing expected fields from upstream provider",
                "provider": "yfinance",
                "context": "price.historical",
                "symbol": symbol,
                "missingFields": ["historyRows"],
            },
        )
    if "Close" not in history.columns:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Missing expected fields from upstream provider",
                "provider": "yfinance",
                "context": "price.historical",
                "symbol": symbol,
                "missingFields": ["Close"],
            },
        )
    return HistoricalPricesResponse(prices=map_historical_prices(history, symbol))


def map_historical_prices(frame: DataFrame, symbol: str):
    history_list = []
    for index, row in frame.iterrows():
        date: Timestamp = row.name
        price = row.get("Close")
        missing = []
        if date is None:
            missing.append("Date")
        if price is None:
            missing.append("Close")
        if missing:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "Missing expected fields from upstream provider",
                    "provider": "yfinance",
                    "context": "price.historical.row",
                    "symbol": symbol,
                    "rowIndex": str(index),
                    "missingFields": missing,
                },
            )
        history_list.append(HistoricalPrice(
            price=price,
            price_date=date.to_pydatetime().date())
        )
    return history_list
