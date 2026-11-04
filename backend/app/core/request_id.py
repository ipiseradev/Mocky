import logging
import re
from contextvars import ContextVar
from time import perf_counter
from typing import Final
from uuid import UUID, uuid4

from starlette.datastructures import Headers, MutableHeaders
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.logging import ERROR_INTERNAL, log_http_request

REQUEST_ID_HEADER: Final = "X-Request-ID"
_UNMATCHED_ROUTE: Final = "unmatched"
_ERROR_CODE_PATTERN: Final = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_request_id_context: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)


def normalize_request_id(value: str | None) -> str:
    if value:
        try:
            return str(UUID(value))
        except (AttributeError, TypeError, ValueError):
            pass

    return str(uuid4())


def get_request_id() -> str | None:
    return _request_id_context.get()


def _safe_error_code(value: object) -> str | None:
    if isinstance(value, str) and _ERROR_CODE_PATTERN.fullmatch(value):
        return value

    return None


def _level_for_status(status_code: int) -> int:
    if status_code >= 500:
        return logging.ERROR

    if status_code >= 400:
        return logging.WARNING

    return logging.INFO


def _error_code_for_status(status_code: int) -> str | None:
    if status_code >= 500:
        return ERROR_INTERNAL

    return None


def _route_path(scope: Scope) -> str:
    route = scope.get("route")
    path = getattr(route, "path", None)

    if isinstance(path, str) and path.startswith("/"):
        return path

    return _UNMATCHED_ROUTE


class RequestIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = normalize_request_id(Headers(scope=scope).get(REQUEST_ID_HEADER))
        method = str(scope.get("method", ""))
        started_at = perf_counter()
        status_code = 500
        response_started = False
        error_code: str | None = None
        request = Request(scope, receive)
        request.state.request_id = request_id

        async def send_with_request_id(message: Message) -> None:
            nonlocal status_code, response_started

            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_started = True
                MutableHeaders(scope=message)[REQUEST_ID_HEADER] = request_id

            await send(message)

        token = _request_id_context.set(request_id)
        try:
            try:
                await self.app(scope, receive, send_with_request_id)
            except HTTPException as exc:
                if response_started:
                    error_code = ERROR_INTERNAL
                else:
                    status_code = exc.status_code

                raise
            except Exception:
                if response_started:
                    error_code = ERROR_INTERNAL
                    raise

                status_code = 500
                error_code = ERROR_INTERNAL
                response = JSONResponse(
                    status_code=status_code,
                    content={
                        "error": {
                            "code": ERROR_INTERNAL,
                            "message": "Internal server error",
                        },
                        "request_id": request_id,
                    },
                )
                response.headers[REQUEST_ID_HEADER] = request_id
                response_started = True
                await response(scope, receive, send)
        finally:
            try:
                if error_code is None:
                    error_code = _safe_error_code(getattr(request.state, "error_code", None))

                if error_code is None:
                    error_code = _error_code_for_status(status_code)

                duration_ms = round(
                    (perf_counter() - started_at) * 1000,
                    3,
                )
                log_level = (
                    logging.ERROR
                    if error_code == ERROR_INTERNAL
                    else _level_for_status(status_code)
                )

                log_http_request(
                    level=log_level,
                    request_id=request_id,
                    method=method,
                    route=_route_path(scope),
                    status_code=status_code,
                    duration_ms=duration_ms,
                    error_code=error_code,
                )
            finally:
                _request_id_context.reset(token)
