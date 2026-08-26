from uuid import UUID

from app.exceptions.base import NotFoundException
from app.exceptions.codes import ErrorCode


class PackageNotFoundException(NotFoundException):
    error_code: ErrorCode = ErrorCode.PACKAGE_NOT_FOUND
    status_code: int = 404

    def __init__(self, package_id: UUID):
        super().__init__(f"Package with id={package_id} not found")
