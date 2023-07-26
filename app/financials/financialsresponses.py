from dataclasses import dataclass


@dataclass
class SymbolFinancials:
    symbol: str
    currency: str
    marketCap: int
    priceToBook: float
    priceToEarningsRatio: float
    earningsPerShare: float
    
    
