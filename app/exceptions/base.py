from app.exceptions.codes import ErrorCode


class AppException(Exception):
    error_code: ErrorCode = ErrorCode.INTERNAL_ERROR
    status_code: int = 500

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    error_code: ErrorCode = ErrorCode.NOT_FOUND
    status_code: int = 404
