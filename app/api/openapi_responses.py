from typing import Any

from app.schemas.errors import ErrorResponse

type OpenAPIResponses = dict[int, dict[str, Any]]

INTEGRITY_ERROR_RESPONSE: OpenAPIResponses = {
    400: {
        "model": ErrorResponse,
        "description": "Нарушение целостности данных, проверьте переданные значения",
    },
}

VALIDATION_ERROR_RESPONSE: OpenAPIResponses = {
    422: {
        "model": ErrorResponse,
        "description": "Ошибка валидации входных данных",
    },
}

INTERNAL_ERROR_RESPONSE: OpenAPIResponses = {
    500: {
        "model": ErrorResponse,
        "description": "Внутренняя ошибка сервера",
    },
}

CATEGORY_NOT_FOUND_RESPONSE: OpenAPIResponses = {
    404: {
        "model": ErrorResponse,
        "description": "Категория не найдена",
    },
}

PACKAGE_NOT_FOUND_RESPONSE: OpenAPIResponses = {
    404: {
        "model": ErrorResponse,
        "description": "Посылка не найдена",
    },
}

COMMON_ERROR_RESPONSES: OpenAPIResponses = (
    INTEGRITY_ERROR_RESPONSE | VALIDATION_ERROR_RESPONSE | INTERNAL_ERROR_RESPONSE
)
