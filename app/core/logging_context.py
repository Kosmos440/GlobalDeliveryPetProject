import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class LoggingContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        session_id = request.cookies.get("session_id")
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            **({"session_id": session_id} if session_id else {}),
        )
        try:
            response = await call_next(request)
            structlog.contextvars.bind_contextvars(status_code=response.status_code)
            return response
        finally:
            structlog.contextvars.clear_contextvars()
