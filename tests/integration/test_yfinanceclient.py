import pytest
from fastapi import HTTPException
from yfinance.exceptions import YFRateLimitError

import app.integration.yfinanceclient as yfinanceclient


def test_call_yfinance_maps_rate_limit_to_429():
    def raise_rate_limit():
        raise YFRateLimitError()

    with pytest.raises(HTTPException) as exc_info:
        yfinanceclient.call_yfinance(
            "AAPL",
            "price.current",
            raise_rate_limit,
        )

    detail = exc_info.value.detail
    assert exc_info.value.status_code == 429
    assert detail["provider"] == "yfinance"
    assert detail["context"] == "price.current"
    assert detail["symbol"] == "AAPL"
    assert detail["errorType"] == "YFRateLimitError"


def test_call_yfinance_maps_unexpected_error_to_502():
    def raise_runtime_error():
        raise RuntimeError("boom")

    with pytest.raises(HTTPException) as exc_info:
        yfinanceclient.call_yfinance(
            "MSFT",
            "statistics.details",
            raise_runtime_error,
        )

    detail = exc_info.value.detail
    assert exc_info.value.status_code == 502
    assert detail["provider"] == "yfinance"
    assert detail["context"] == "statistics.details"
    assert detail["symbol"] == "MSFT"
    assert detail["errorType"] == "RuntimeError"
    assert detail["error"] == "boom"


def test_call_yfinance_rethrows_http_exception():
    def raise_http_exception():
        raise HTTPException(status_code=400, detail="bad request")

    with pytest.raises(HTTPException, match="bad request") as exc_info:
        yfinanceclient.call_yfinance(
            "AAPL",
            "profile.details",
            raise_http_exception,
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "bad request"


def test_raise_upstream_data_error_includes_extensions():
    with pytest.raises(HTTPException) as exc_info:
        yfinanceclient.raise_upstream_data_error(
            symbol="AAPL",
            context="holders.institutional.row",
            missing_fields=["Value"],
            rowIndex="7",
        )

    detail = exc_info.value.detail
    assert exc_info.value.status_code == 502
    assert detail["provider"] == "yfinance"
    assert detail["context"] == "holders.institutional.row"
    assert detail["symbol"] == "AAPL"
    assert detail["missingFields"] == ["Value"]
    assert detail["rowIndex"] == "7"


def test_call_ticker_runs_operation_with_ticker(monkeypatch: pytest.MonkeyPatch):
    sentinel_ticker = object()
    monkeypatch.setattr(yfinanceclient, "get_ticker", lambda symbol, context: sentinel_ticker)

    result = yfinanceclient.call_ticker(
        "AAPL",
        "price.current",
        lambda ticker: ticker is sentinel_ticker,
    )

    assert result is True
