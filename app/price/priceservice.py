from datetime import timedelta

import yfinance as yf
from pandas import DataFrame, Timestamp

from .pricerequests import Period
from .priceresponses import HistoricalPrice, CurrentPrice, HistoricalPricesResponse
from ..cache.cachedecorator import simple_cache


def get_current_price(symbol: str):
    info = yf.Ticker(symbol).info
    return CurrentPrice(
        symbol=symbol,
        companyName=info.get("shortName"),
        currentPrice=info.get("currentPrice"),
        previousClose=info.get("previousClose"),
        currency=info.get("currency")
    )


@simple_cache(expire=timedelta(minutes=10))
def get_historical_prices(symbol: str, period: Period):
    ticker = yf.Ticker(symbol)
    history = ticker.history(period=period)
    return HistoricalPricesResponse(prices=map_historical_prices(history))


def map_historical_prices(frame: DataFrame):
    history_list = []
    for index, row in frame.iterrows():
        date: Timestamp = row.name
        price = row.get("Close")
        history_list.append(HistoricalPrice(
            price=price,
            price_date=date.to_pydatetime().date())
        )
    return history_list
