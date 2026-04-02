from threading import Lock
from typing import Callable, TypeVar

import yfinance as yf
from curl_cffi import requests as curl_requests
from fastapi import HTTPException
from yfinance.exceptions import YFRateLimitError
from app.settings.settings import settings

T = TypeVar("T")
_session_lock = Lock()
_session_by_mode: dict[str, curl_requests.Session] = {}
_DEFAULT_IMPERSONATION_MODE = "auto"
_AUTO_PRIMARY_IMPERSONATION = "chrome"
_SUPPORTED_IMPERSONATION_MODES = {"auto", "chrome", "firefox", "none"}


def _resolve_impersonation_mode(mode: str | None = None) -> str:
    requested = (mode or settings.yf_impersonation_mode or _DEFAULT_IMPERSONATION_MODE).strip().lower()
    if requested in {"off", "disabled", "false", "no"}:
        requested = "none"
    if requested not in _SUPPORTED_IMPERSONATION_MODES:
        requested = _DEFAULT_IMPERSONATION_MODE
    return requested


def _session_key_for_mode(mode: str) -> str:
    if mode == "auto":
        return _AUTO_PRIMARY_IMPERSONATION
    return mode


def _create_session(session_key: str) -> curl_requests.Session:
    if session_key == "none":
        return curl_requests.Session()
    return curl_requests.Session(impersonate=session_key)


def _get_yfinance_session(mode: str) -> curl_requests.Session:
    session_key = _session_key_for_mode(mode)
    if session_key not in _session_by_mode:
        with _session_lock:
            if session_key not in _session_by_mode:
                _session_by_mode[session_key] = _create_session(session_key)
    return _session_by_mode[session_key]


def get_ticker(symbol: str, context: str, mode: str | None = None):
    resolved_mode = _resolve_impersonation_mode(mode)
    return call_yfinance(
        symbol,
        context,
        lambda: yf.Ticker(symbol, session=_get_yfinance_session(resolved_mode)),
    )


def call_ticker(symbol: str, context: str, operation: Callable[[yf.Ticker], T]) -> T:
    mode = _resolve_impersonation_mode()
    try:
        ticker = get_ticker(symbol, f"{context}.init", mode=mode)
        return call_yfinance(symbol, context, lambda: operation(ticker))
    except HTTPException as exc:
        if _should_retry_with_non_impersonated_session(mode, exc):
            fallback_ticker = get_ticker(symbol, f"{context}.init.fallback", mode="none")
            return call_yfinance(symbol, context, lambda: operation(fallback_ticker))
        raise


def _should_retry_with_non_impersonated_session(mode: str, exc: HTTPException) -> bool:
    if mode != "auto" or exc.status_code != 502:
        return False
    detail = exc.detail if isinstance(exc.detail, dict) else {}
    error_type = str(detail.get("errorType", ""))
    error_text = str(detail.get("error", "")).lower()
    return error_type in {"SSLError", "CurlError"} and (
        "tls connect error" in error_text
        or "openssl_internal:invalid library" in error_text
        or "curl: (35)" in error_text
    )


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
                "provider": "yfinance",
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
                "provider": "yfinance",
                "context": context,
                "symbol": symbol,
                "errorType": type(exc).__name__,
                "error": str(exc),
            },
        ) from exc
