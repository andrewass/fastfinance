from fastapi import APIRouter
from .statisticsservice import get_financial_details

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@router.get("/{symbol}")
async def get_financial_details_symbol(symbol: str):
    return get_financial_details(symbol)
