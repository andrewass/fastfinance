from dataclasses import dataclass
from typing import Optional


@dataclass
class SymbolFinancials:
    symbol: str
    currency: str
    marketCap: int
    priceToBook: float
    priceToEarningsRatio: float
    earningsPerShare: float
    dividendRate: Optional[float] = None
    dividendYieldPercentage: Optional[float] = None
