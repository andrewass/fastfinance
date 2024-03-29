from fastapi import APIRouter
from .pricerequests import SymbolsRequest, Period
from .priceservice import get_historical_prices, get_current_price

router = APIRouter(
    prefix="/price",
    tags=["price"],
)


@router.get("/current-price/{symbol}")
async def get_current_price_symbol(symbol: str):
    return get_current_price(symbol)


@router.post("/current-price-symbols")
async def get_current_price_symbols(symbols: SymbolsRequest):
    return list(map(get_current_price, symbols.symbols))


@router.get("/historical-prices")
async def get_historical_prices_symbol(symbol: str, period: Period):
    return get_historical_prices(symbol, period)
