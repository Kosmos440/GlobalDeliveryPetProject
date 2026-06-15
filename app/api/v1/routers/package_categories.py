import structlog
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.package_category import PackageCategoryDAL
from app.schemas.package_category import PackageCategoryRead

logger = structlog.get_logger(__name__)
package_categories_router = APIRouter()

@package_categories_router.get("/", response_model=list[PackageCategoryRead])
async def get_categories(
        session: AsyncSession = Depends(get_session)
) -> list[PackageCategoryRead]:
    package_categories_dal = PackageCategoryDAL(session)
    categories = await package_categories_dal.get_all_categories()
    if not categories:
        logger.warning("category.list.not_found")
        raise HTTPException(status_code=404, detail="No categories found.")
    return categories
