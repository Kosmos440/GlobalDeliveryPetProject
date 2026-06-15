from collections.abc import Sequence
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.package import Package


class PackageDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_package(
        self,
        name: str,
        weight: Decimal,
        category_id: int,
        value_usd: Decimal,
        session_id: UUID,
    ) -> Package:
        new_package = Package(
            name=name,
            weight=weight,
            category_id=category_id,
            value_usd=value_usd,
            session_id=session_id,
        )
        self.db_session.add(new_package)
        await self.db_session.flush()
        result = await self.db_session.execute(
            select(Package)
            .where(Package.package_id == new_package.package_id)
            .options(selectinload(Package.category))
        )
        return result.scalar_one()

    async def get_package_by_id(self, package_id: UUID) -> Package | None:
        query = select(Package).where(
            Package.package_id == package_id
        ).options(
            selectinload(Package.category)
        )

        result = await self.db_session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_all_packages_by_session(self, session_id: UUID) -> Sequence[Package]:
        query = select(Package).where(
            Package.session_id == session_id
        ).options(selectinload(Package.category))

        res = await self.db_session.execute(query)
        return res.scalars().unique().all()

    async def get_zero_packages(self) -> Sequence[Package] | None:
        query = select(Package).where(Package.delivery_cost_rub.is_(None))
        result = await self.db_session.execute(query)
        packages = result.scalars().all()
        if not packages:
            return None
        return packages

    async def update_package_value(self, package_id: UUID, new_value: Decimal) -> Package | None:
        package = await self.db_session.get(Package, package_id)
        if not package:
            return None

        package.value_usd = new_value

        await self.db_session.flush()
        await self.db_session.refresh(package)
        return package
