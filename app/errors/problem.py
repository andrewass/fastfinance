import logging
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_problem_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return _problem_from_http_exception(request, exc.status_code, exc.detail)

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return _problem_from_http_exception(request, exc.status_code, exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _problem_response(
            status_code=422,
            title="Request validation failed",
            detail="Request validation failed",
            problem_type="urn:fastfinance:problem:request-validation",
            instance=_request_instance(request),
            extensions={"errors": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception while handling request")
        return _problem_response(
            status_code=500,
            title="Internal server error",
            detail="An unexpected error occurred.",
            problem_type="urn:fastfinance:problem:internal-server-error",
            instance=_request_instance(request),
        )


def _problem_from_http_exception(request: Request, status_code: int, raw_detail: Any) -> JSONResponse:
    detail, extensions = _extract_detail_and_extensions(raw_detail, status_code)
    return _problem_response(
        status_code=status_code,
        title=_problem_title(status_code),
        detail=detail,
        problem_type=_problem_type(status_code),
        instance=_request_instance(request),
        extensions=extensions,
    )


def _extract_detail_and_extensions(raw_detail: Any, status_code: int) -> tuple[str, dict[str, Any]]:
    if isinstance(raw_detail, dict):
        extensions = dict(raw_detail)
        detail = str(
            extensions.pop("detail", None)
            or extensions.pop("message", None)
            or _default_detail(status_code)
        )
        extensions.pop("title", None)
        extensions.pop("type", None)
        extensions.pop("status", None)
        extensions.pop("instance", None)
        return detail, extensions

    if raw_detail is None:
        return _default_detail(status_code), {}
    return str(raw_detail), {}


def _problem_response(
    status_code: int,
    title: str,
    detail: str,
    problem_type: str,
    instance: str,
    extensions: dict[str, Any] | None = None,
) -> JSONResponse:
    payload: dict[str, Any] = {
        "type": problem_type,
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": instance,
    }
    if extensions:
        payload.update(extensions)
    return JSONResponse(
        status_code=status_code,
        content=payload,
        media_type="application/problem+json",
    )


def _problem_title(status_code: int) -> str:
    if status_code == 422:
        return "Request validation failed"
    if status_code == 502:
        return "Upstream provider failure"
    if status_code == 500:
        return "Internal server error"
    return _default_detail(status_code)


def _problem_type(status_code: int) -> str:
    if status_code == 422:
        return "urn:fastfinance:problem:request-validation"
    if status_code == 502:
        return "urn:fastfinance:problem:upstream-provider-failure"
    if status_code == 500:
        return "urn:fastfinance:problem:internal-server-error"
    return "about:blank"


def _default_detail(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Unknown error"


def _request_instance(request: Request) -> str:
    path = request.url.path
    query = request.url.query
    if query:
        return f"{path}?{query}"
    return path
