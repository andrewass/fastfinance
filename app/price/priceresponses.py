from datetime import date

from pydantic import BaseModel, field_serializer


class CurrentPrice(BaseModel):
    symbol: str
    companyName: str
    currentPrice: float
    previousClose: float
    currency: str


class HistoricalPrice(BaseModel):
    price: float
    price_date: date

    @field_serializer("price_date")
    def serialize_price_date(self, price_date: date, _info):
        return price_date.strftime("%Y-%m-%d")


class HistoricalPricesResponse(BaseModel):
    prices: list[HistoricalPrice]
