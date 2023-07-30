from dataclasses import dataclass
from datetime import date


@dataclass
class CurrentPrice:
    symbol: str
    companyName: str
    currentPrice: float
    previousClose: float
    currency: str


@dataclass
class HistoricalPrice:
    price: float
    date: date
