from fastapi import APIRouter
from .holdersservice import get_holders_details_symbol
from .holdersresponse import HoldersResponse


router = APIRouter(
    prefix="/holders",
    tags=["holders"],
)


@router.get("/{symbol}", response_model=HoldersResponse)
def get_holders_details(symbol: str) -> HoldersResponse:
    return get_holders_details_symbol(symbol)
