from fastapi import APIRouter

router = APIRouter(
    prefix="/holders",
    tags=["holders"],
)


@router.get("/details/{symbol}")
async def get_holder_details(symbol: str):
    return get_holder_details(symbol)


