from enum import Enum

from pydantic import BaseModel


class Period(str, Enum):
    day1 = "1d",
    day5 = "5d",
    month1 = "1mo",
    month3 = "3mo",
    month6 = "6mo",
    year1 = "1y",
    year2 = "2y",
    year5 = "5y",
    year10 = "10y",
    ytd = "ytd",
    max_interval = "max"


class SymbolsRequest(BaseModel):
    symbols: list[str]
