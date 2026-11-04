import json
import logging
from datetime import UTC, datetime
from typing import Final

from app.core.settings import LogLevel

SERVICE_NAME: Final = "backend"
EVENT_HTTP_REQUEST: Final = "http_request"
ERROR_INTERNAL: Final = "internal_error"

_LOGGER_NAME: Final = "mocky.backend"
_HANDLER_MARKER: Final = "_mocky_json_handler"


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=UTC,
            ).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "service": SERVICE_NAME,
            "event": getattr(record, "event", "unknown"),
            "request_id": getattr(record, "request_id", None),
            "method": getattr(record, "method", None),
            "route": getattr(record, "route", None),
            "status_code": getattr(record, "status_code", None),
            "duration_ms": getattr(record, "duration_ms", None),
            "error_code": getattr(record, "error_code", None),
        }

        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )


def configure_logging(level: LogLevel = "INFO") -> None:
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False
    logger.disabled = False

    logging.getLogger("uvicorn.access").disabled = True

    handler = next(
        (current for current in logger.handlers if getattr(current, _HANDLER_MARKER, False)),
        None,
    )

    if handler is None:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        setattr(handler, _HANDLER_MARKER, True)
        logger.addHandler(handler)

    handler.setLevel(logging.NOTSET)


def log_http_request(
    *,
    level: int,
    request_id: str,
    method: str,
    route: str,
    status_code: int,
    duration_ms: float,
    error_code: str | None,
) -> None:
    logger = logging.getLogger(_LOGGER_NAME)
    logger.log(
        level,
        EVENT_HTTP_REQUEST,
        extra={
            "event": EVENT_HTTP_REQUEST,
            "request_id": request_id,
            "method": method,
            "route": route,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "error_code": error_code,
        },
    )
