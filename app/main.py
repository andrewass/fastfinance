import json

from fastapi import FastAPI

import yfinance as yf

app = FastAPI(version="0.0.1")


@app.get("/get-random-number")
async def root():
    return {"example": "This is the example text", "number": 0}


@app.get("/current-price/{symbol}")
async def getCurrentPrice(symbol: str):
    ticker = yf.Ticker(symbol)
    history = ticker.info
    return json.dumps(history)
