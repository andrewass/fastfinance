from fastapi import APIRouter
from .financialsservice import get_financial_details

router = APIRouter(
    prefix="/financials",
    tags=["financials"],
)


@router.get("/financial-details-symbol/{symbol}")
async def get_financial_details_symbol(symbol: str):
    return get_financial_details(symbol)
