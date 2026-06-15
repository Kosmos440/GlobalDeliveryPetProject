import sys

import logging
import structlog

from app.core.config import settings


def _get_render() -> structlog.types.Processor:
    if settings.DEBUG:
        return structlog.dev.ConsoleRenderer()
    return structlog.processors.JSONRenderer()


def setup_logging() -> None:
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    base_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[
            *base_processors,
            _get_render(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(message)s",
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
