from typing import Optional
from pydantic import BaseModel


class SymbolStatistics(BaseModel):
    symbol: str
    companyName: str
    currency: str
    marketCap: int
    priceToBook: float
    priceToEarnings: float
    earningsPerShare: float
    dividendRate: Optional[float] = None
    dividendYieldPercentage: Optional[float] = None
