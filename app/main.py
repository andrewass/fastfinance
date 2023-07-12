import json
from dataclasses import dataclass

import yfinance as yf
from fastapi import FastAPI

app = FastAPI(version="0.0.1")


@dataclass
class SymbolsRequest:
    symbols: list[str]


@dataclass
class CurrentPrice:
    symbol: str
    currentPrice: float
    previousClose: float
    currency: str


@app.get("/current-price-symbol/{symbol}")
async def get_current_price_symbol(symbol: str):
    return get_current_price(symbol)


@app.post("/current-price-symbols")
async def get_current_price_symbols(symbols: SymbolsRequest):
    return list(map(get_current_price, symbols.symbols))


def get_current_price(symbol: str):
    ticker = yf.Ticker(symbol)
    current_price = ticker.info.get("currentPrice")
    previous_close = ticker.info.get("previousClose")
    currency = ticker.info.get("currency")
    return CurrentPrice(symbol, current_price, previous_close, currency)
