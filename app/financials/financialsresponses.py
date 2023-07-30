from dataclasses import dataclass
from typing import Optional


@dataclass
class SymbolFinancials:
    symbol: str
    companyName: str
    currency: str
    marketCap: int
    priceToBook: float
    priceToEarnings: float
    earningsPerShare: float
    dividendRate: Optional[float] = None
    dividendYieldPercentage: Optional[float] = None
