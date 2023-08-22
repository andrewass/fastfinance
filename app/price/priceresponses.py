from pydantic import BaseModel
from datetime import date


class CurrentPrice(BaseModel):
    symbol: str
    companyName: str
    currentPrice: float
    previousClose: float
    currency: str


class HistoricalPrice(BaseModel):
    price: float
    date: date
