from app.exceptions.base import AppException
from app.exceptions.codes import ErrorCode


class ExternalServiceException(AppException):
    """Базовое исключение для ошибок внешних интеграций (отдает 502)."""
    status_code: int = 502


class CbrRateFetchError(ExternalServiceException):
    """Не удалось связаться с ЦБ."""
    error_code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_ERROR
    status_code: int = 502

    def __init__(self, message: str = "Failed to fetch rate from CBR"):
        super().__init__(message)


class CbrRateBadResponseError(ExternalServiceException):
    """Формат данных от api не соответствует ожидаемому."""
    error_code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_BAD_RESPONSE
    status_code: int = 502
    def __init__(self, message: str = "Received invalid response format from CBR"):
        super().__init__(message)
