from datetime import timedelta

import yfinance as yf
from fastapi import HTTPException
from pandas import DataFrame, Timestamp

from .holdersresponse import HoldersResponse, Holder
from ..cache.cachedecorator import simple_cache


@simple_cache(expire=timedelta(minutes=5))
def get_holders_details_symbol(symbol: str) -> HoldersResponse:
    ticker = yf.Ticker(symbol)
    institutional_holders = ticker.institutional_holders
    mutual_fund_holders = ticker.mutualfund_holders
    missing = []
    if institutional_holders is None:
        missing.append("institutional_holders")
    if mutual_fund_holders is None:
        missing.append("mutualfund_holders")
    if missing:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Missing expected fields from upstream provider",
                "provider": "yfinance",
                "context": "holders.details",
                "symbol": symbol,
                "missingFields": missing,
            },
        )
    return HoldersResponse(
        institutionalHolders=map_holders(institutional_holders, symbol, "holders.institutional"),
        mutualFundHolders=map_holders(mutual_fund_holders, symbol, "holders.mutualFund")
    )


def map_holders(frame: DataFrame | None, symbol: str, context: str) -> list[Holder]:
    if frame is None:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Missing expected fields from upstream provider",
                "provider": "yfinance",
                "context": context,
                "symbol": symbol,
                "missingFields": ["frame"],
            },
        )
    required_columns = ("Date Reported", "Holder", "Shares", "% Out", "Value")
    missing_columns = [column for column in required_columns if column not in frame.columns]
    if missing_columns:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Missing expected fields from upstream provider",
                "provider": "yfinance",
                "context": context,
                "symbol": symbol,
                "missingFields": missing_columns,
            },
        )
    holders_list = []
    for index, row in frame.iterrows():
        date: Timestamp = row.get("Date Reported")
        name = row.get("Holder")
        shares = row.get("Shares")
        percentage_out = row.get("% Out")
        value = row.get("Value")
        missing = []
        if date is None:
            missing.append("Date Reported")
        if name is None:
            missing.append("Holder")
        if shares is None:
            missing.append("Shares")
        if percentage_out is None:
            missing.append("% Out")
        if value is None:
            missing.append("Value")
        if missing:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "Missing expected fields from upstream provider",
                    "provider": "yfinance",
                    "context": f"{context}.row",
                    "symbol": symbol,
                    "rowIndex": str(index),
                    "missingFields": missing,
                },
            )
        holders_list.append(Holder(
            name=name,
            reported=date.to_pydatetime().date(),
            shares=shares,
            percentageOut=percentage_out * 100,
            value=value
        ))
    return holders_list
