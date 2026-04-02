from fastapi import APIRouter
from .pricerequests import SymbolsRequest, Period
from .priceresponses import CurrentPrice, HistoricalPricesResponse
from .priceservice import get_historical_prices, get_current_price

router = APIRouter(
    prefix="/price",
    tags=["price"],
)


@router.get("/current-price/{symbol}", response_model=CurrentPrice)
def get_current_price_symbol(symbol: str) -> CurrentPrice:
    return get_current_price(symbol)


@router.post("/symbols", response_model=list[CurrentPrice])
def get_current_price_symbols(symbols: SymbolsRequest) -> list[CurrentPrice]:
    return list(map(get_current_price, symbols.symbols))


@router.get("/historical-prices", response_model=HistoricalPricesResponse)
def get_historical_prices_symbol(symbol: str, period: Period) -> HistoricalPricesResponse:
    return get_historical_prices(symbol, period)
