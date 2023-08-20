from fastapi import APIRouter
from .holdersservice import get_holders_details

router = APIRouter(
    prefix="/holders",
    tags=["holders"],
)


@router.get("/details/{symbol}")
async def get_holders_details(symbol: str):
    return get_holders_details(symbol)
