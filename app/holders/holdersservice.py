import yfinance as yf


def get_holders_details(symbol: str):
    info = yf.Ticker(symbol).info
