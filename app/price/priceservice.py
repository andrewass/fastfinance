import yfinance as yf

from pandas import DataFrame
from .pricerequests import Period
from .priceresponses import HistoricPrice, CurrentPrice


def get_current_price(symbol: str):
    info = yf.Ticker(symbol).info
    return CurrentPrice(
        symbol=symbol,
        companyName=info.get("shortName"),
        currentPrice=info.get("currentPrice"),
        previousClose=info.get("previousClose"),
        currency=info.get("currency")
    )


def get_historic_prices(symbol: str, period: Period):
    ticker = yf.Ticker(symbol)
    history = ticker.history(period=period)
    return map_historic(history, symbol)


def map_historic(frame: DataFrame, symbol: str):
    history_list = []
    for index, row in frame.iterrows():
        print(row)
        date = row.name
        price = row.get("Close")
        history_list.append(HistoricPrice(symbol, price, date))
    return history_list
