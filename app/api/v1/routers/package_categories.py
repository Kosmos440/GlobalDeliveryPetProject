from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.openapi_responses import INTERNAL_ERROR_RESPONSE
from app.db.session import get_session
from app.schemas.package_category import PackageCategoryRead
from app.services.package_category_service import _get_categories

package_categories_router = APIRouter()

@package_categories_router.get(
    "/",
    response_model=list[PackageCategoryRead],
    summary="Получить список категорий",
    description="Справочник для формы создания посылки",
    responses=INTERNAL_ERROR_RESPONSE,
)
async def get_categories(
        session: AsyncSession = Depends(get_session)
) -> list[PackageCategoryRead]:
    categories = await _get_categories(session=session)
    return categories
