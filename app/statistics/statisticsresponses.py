from pydantic import BaseModel


class SymbolStatistics(BaseModel):
    symbol: str
    companyName: str
    currency: str
    marketCap: int
    priceToBook: float
    priceToEarnings: float
    earningsPerShare: float
    dividendRate: float | None = None
    dividendYieldPercentage: float | None = None
