from dataclasses import dataclass
from datetime import datetime


@dataclass
class CurrentPrice:
    symbol: str
    currentPrice: float
    previousClose: float
    currency: str


@dataclass
class HistoricPrice:
    symbol: str
    price: float
    date: datetime
