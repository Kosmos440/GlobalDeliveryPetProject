from app.exceptions.base import NotFoundException
from app.exceptions.codes import ErrorCode


class CategoryNotFoundException(NotFoundException):
    error_code: ErrorCode = ErrorCode.CATEGORY_NOT_FOUND
    status_code: int = 404

    def __init__(self, category_id: int) -> None:
        super().__init__(f"Category with id={category_id} not found")
