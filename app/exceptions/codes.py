import enum


class ErrorCode(enum.StrEnum):
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not_found"
    EXTERNAL_SERVICE_ERROR = "external_service_error"
    EXTERNAL_SERVICE_BAD_RESPONSE = "external_service_bad_response"
    PACKAGE_NOT_FOUND = "package_not_found"
    CATEGORY_NOT_FOUND = "category_not_found"
    INTEGRITY_ERROR = "integrity_error"
    VALIDATION_ERROR = "validation_error"
    INTERNAL_ERROR = "internal_error"
