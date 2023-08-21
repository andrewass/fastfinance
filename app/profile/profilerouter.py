from fastapi import APIRouter
from .profileservice import get_profile

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.get("/{symbol}")
async def get_profile_symbol(symbol: str):
    return get_profile(symbol)
