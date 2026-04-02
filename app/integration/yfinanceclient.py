from typing import Callable, TypeVar

from fastapi import HTTPException

T = TypeVar("T")


def call_yfinance(symbol: str, context: str, operation: Callable[[], T]) -> T:
    try:
        return operation()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Failed to fetch data from upstream provider",
                "provider": "yfinance",
                "context": context,
                "symbol": symbol,
                "errorType": type(exc).__name__,
                "error": str(exc),
            },
        ) from exc
