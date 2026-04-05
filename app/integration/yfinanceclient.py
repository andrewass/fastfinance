from collections.abc import Sequence
from typing import Any, Callable, NoReturn, TypeVar

import yfinance as yf
from fastapi import HTTPException
from yfinance.exceptions import YFRateLimitError

T = TypeVar("T")
_PROVIDER = "yfinance"


def get_ticker(symbol: str, context: str) -> yf.Ticker:
    return call_yfinance(
        symbol,
        context,
        lambda: yf.Ticker(symbol),
    )


def call_ticker(symbol: str, context: str, operation: Callable[[yf.Ticker], T]) -> T:
    ticker = get_ticker(symbol, f"{context}.init")
    return call_yfinance(symbol, context, lambda: operation(ticker))


def raise_upstream_data_error(
    symbol: str,
    context: str,
    missing_fields: Sequence[str],
    **extensions: Any,
) -> NoReturn:
    detail: dict[str, Any] = {
        "message": "Missing expected fields from upstream provider",
        "provider": _PROVIDER,
        "context": context,
        "symbol": symbol,
        "missingFields": list(missing_fields),
    }
    detail.update(extensions)
    raise HTTPException(status_code=502, detail=detail)


def call_yfinance(symbol: str, context: str, operation: Callable[[], T]) -> T:
    try:
        return operation()
    except HTTPException:
        raise
    except YFRateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Upstream provider rate limit reached",
                "provider": _PROVIDER,
                "context": context,
                "symbol": symbol,
                "errorType": type(exc).__name__,
                "error": str(exc),
            },
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Failed to fetch data from upstream provider",
                "provider": _PROVIDER,
                "context": context,
                "symbol": symbol,
                "errorType": type(exc).__name__,
                "error": str(exc),
            },
        ) from exc
