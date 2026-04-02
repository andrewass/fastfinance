from fastapi import APIRouter
from .profileresponses import Profile
from .profileservice import get_profile

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.get("/{symbol}", response_model=Profile)
def get_profile_symbol(symbol: str) -> Profile:
    return get_profile(symbol)
