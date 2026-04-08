from fastapi import HTTPException

import app.price.pricerouter as pricerouter
from app.price.priceresponses import CurrentPrice


def test_current_price_endpoint_success_shape(monkeypatch, client):
    monkeypatch.setattr(
        pricerouter,
        "get_current_price",
        lambda symbol: CurrentPrice(
            symbol=symbol,
            companyName="Apple Inc.",
            currentPrice=210.25,
            previousClose=208.10,
            currency="USD",
        ),
    )

    response = client.get("/price/current-price/AAPL")

    assert response.status_code == 200
    assert response.json() == {
        "symbol": "AAPL",
        "companyName": "Apple Inc.",
        "currentPrice": 210.25,
        "previousClose": 208.10,
        "currency": "USD",
    }


def test_current_price_endpoint_problem_json_on_upstream_error(monkeypatch, client):
    def raise_upstream(_symbol: str):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Failed to fetch data from upstream provider",
                "provider": "yfinance",
                "context": "price.current",
                "symbol": "AAPL",
                "errorType": "RuntimeError",
                "error": "boom",
            },
        )

    monkeypatch.setattr(pricerouter, "get_current_price", raise_upstream)

    response = client.get("/price/current-price/AAPL")

    payload = response.json()
    assert response.status_code == 502
    assert response.headers["content-type"].startswith("application/problem+json")
    assert payload["type"] == "urn:fastfinance:problem:upstream-provider-failure"
    assert payload["title"] == "Upstream provider failure"
    assert payload["status"] == 502
    assert payload["detail"] == "Failed to fetch data from upstream provider"
    assert payload["instance"] == "/price/current-price/AAPL"
    assert payload["provider"] == "yfinance"
    assert payload["context"] == "price.current"
    assert payload["symbol"] == "AAPL"


def test_historical_prices_invalid_period_returns_validation_problem(client):
    response = client.get("/price/historical-prices?symbol=AAPL&period=not-valid")

    payload = response.json()
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert payload["type"] == "urn:fastfinance:problem:request-validation"
    assert payload["title"] == "Request validation failed"
    assert payload["status"] == 422
    assert payload["detail"] == "Request validation failed"
