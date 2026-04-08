import pytest
from fastapi import HTTPException
from pandas import DataFrame, Timestamp

import app.holders.holdersservice as holdersservice
import app.price.priceservice as priceservice


def test_get_current_price_maps_required_fields(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        priceservice,
        "call_ticker",
        lambda symbol, context, operation: {
            "shortName": "Apple Inc.",
            "currentPrice": 210.25,
            "previousClose": 208.10,
            "currency": "USD",
        },
    )

    result = priceservice.get_current_price("AAPL")
    payload = result.model_dump()

    assert payload == {
        "symbol": "AAPL",
        "companyName": "Apple Inc.",
        "currentPrice": 210.25,
        "previousClose": 208.10,
        "currency": "USD",
    }


@pytest.mark.parametrize(
    "missing_field",
    ["shortName", "currentPrice", "previousClose", "currency"],
)
def test_get_current_price_missing_field_raises_502(
    monkeypatch: pytest.MonkeyPatch, missing_field: str
):
    payload = {
        "shortName": "Apple Inc.",
        "currentPrice": 210.25,
        "previousClose": 208.10,
        "currency": "USD",
    }
    payload.pop(missing_field)

    monkeypatch.setattr(
        priceservice,
        "call_ticker",
        lambda symbol, context, operation: payload,
    )

    with pytest.raises(HTTPException) as exc_info:
        priceservice.get_current_price("AAPL")

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail["provider"] == "yfinance"
    assert exc_info.value.detail["context"] == "price.current"
    assert exc_info.value.detail["missingFields"] == [missing_field]


def test_get_historical_prices_missing_close_column_raises_502(monkeypatch: pytest.MonkeyPatch):
    frame = DataFrame(
        {"Open": [100.0]},
        index=[Timestamp("2024-01-01")],
    )
    monkeypatch.setattr(priceservice, "call_ticker", lambda symbol, context, operation: frame)

    with pytest.raises(HTTPException) as exc_info:
        priceservice.get_historical_prices("AAPL", "1mo")

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail["provider"] == "yfinance"
    assert exc_info.value.detail["context"] == "price.historical"
    assert exc_info.value.detail["missingFields"] == ["Close"]


def test_map_holders_maps_percentage_to_percent():
    frame = DataFrame(
        [
            {
                "Date Reported": Timestamp("2024-01-01"),
                "Holder": "Big Fund",
                "Shares": 1000.0,
                "% Out": 0.25,
                "Value": 100000.0,
            }
        ]
    )

    holders = holdersservice.map_holders(frame, "AAPL", "holders.institutional")

    assert len(holders) == 1
    assert holders[0].name == "Big Fund"
    assert holders[0].shares == 1000.0
    assert holders[0].percentageOut == 25.0


@pytest.mark.parametrize(
    "frame,expected_missing",
    [
        (
            DataFrame([{"Date Reported": Timestamp("2024-01-01"), "Holder": "Big Fund"}]),
            ["Shares", "% Out", "Value"],
        ),
        (
            DataFrame(
                [
                    {
                        "Date Reported": Timestamp("2024-01-01"),
                        "Holder": "Big Fund",
                        "Shares": 1000.0,
                    }
                ]
            ),
            ["% Out", "Value"],
        ),
    ],
)
def test_map_holders_missing_column_raises_502(frame: DataFrame, expected_missing: list[str]):

    with pytest.raises(HTTPException) as exc_info:
        holdersservice.map_holders(frame, "AAPL", "holders.institutional")

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail["provider"] == "yfinance"
    assert exc_info.value.detail["context"] == "holders.institutional"
    assert exc_info.value.detail["missingFields"] == expected_missing
