import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions.base import AppException, NotFoundException
from app.exceptions.codes import ErrorCode
from app.schemas.errors import ErrorResponse

logger = structlog.get_logger(__name__)

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(error=exc.error_code, message=exc.message).model_dump(),
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error=ErrorCode.INTEGRITY_ERROR,
                message="Нарушение целостности данных, проверьте переданные значения",
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error=ErrorCode.VALIDATION_ERROR,
                message="Ошибка валидации входных данных",
                details={"errors": exc.errors()},
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(error=ErrorCode.INTERNAL_ERROR, message="Внутренняя ошибка сервера").model_dump(),
        )
