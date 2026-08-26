import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.package_category import PackageCategoryDAL
from app.schemas.package_category import PackageCategoryRead

logger = structlog.get_logger(__name__)

async def _get_categories(session: AsyncSession) -> list[PackageCategoryRead]:
    package_categories_dal = PackageCategoryDAL(session)
    categories = await package_categories_dal.get_all_categories()
    if not categories:
        logger.warning("category.list.not_found")
    return categories
