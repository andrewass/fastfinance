import yfinance as yf
from pandas import DataFrame, Timestamp

from .holdersresponse import HoldersDetails, Holder


def get_holders_details(symbol: str):
    ticker = yf.Ticker(symbol)
    return HoldersDetails(
        institutionalHolders=map_holders(ticker.institutional_holders),
        mutualFundHolders=map_holders(ticker.mutualfund_holders)
    )


def map_holders(frame: DataFrame):
    holders_list = []
    if frame is not None:
        for index, row in frame.iterrows():
            date: Timestamp = row.get("Date Reported")
            holders_list.append(Holder(
                name=row.get("Holder"),
                dateReported=date.to_pydatetime().date(),
                shares=row.get("Shares"),
                percentageOut=row.get("% Out") * 100,
                value=row.get("Value")
            ))
    return holders_list
