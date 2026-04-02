from fastapi import APIRouter
from .statisticsresponses import SymbolStatistics
from .statisticsservice import get_financial_details

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@router.get("/{symbol}", response_model=SymbolStatistics)
def get_financial_details_symbol(symbol: str) -> SymbolStatistics:
    return get_financial_details(symbol)
