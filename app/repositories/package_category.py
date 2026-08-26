from sqlalchemy import Sequence, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.package_category import Category


class PackageCategoryDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_all_categories(self) -> Sequence[Category]:
        categories = await self.db_session.execute(select(Category))
        return categories.scalars().all()

    async def get_id_in_categories(self, category_id: int) -> bool:
        query = select(exists().where(Category.category_id == category_id))
        result = await self.db_session.execute(query)
        return result.scalar()
