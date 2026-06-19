from collections.abc import Sequence
from decimal import Decimal
from uuid import UUID

from sqlalchemy import desc, func, select
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

        query = (
            select(Package)
            .where(Package.package_id == new_package.package_id)
            .options(selectinload(Package.category))
        )

        result = await self.db_session.execute(query)
        return result.scalar_one()

    async def get_package_by_id(self, package_id: UUID) -> Package | None:
        query = (
            select(Package)
            .where(Package.package_id == package_id)
            .options(selectinload(Package.category))
        )

        result = await self.db_session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_filtered_packages_by_session(
            self, session_id: UUID, page: int, size: int,
            column: str | None = None,
            change_direction: bool | None = None,
            search: str | None = None,
            category_id: int | None = None,
            min_weight: Decimal | None = None,
            max_weight: Decimal | None = None,
            min_value: Decimal | None = None,
            max_value: Decimal | None = None,
    ) -> Sequence[Package]:

        query = (
            select(Package).where(
            Package.session_id == session_id)
            .limit(size)
            .offset((page-1)*size)
        )

        if column is not None:
            query = query.order_by(desc(column)) if change_direction else query.order_by(column)

        if search is not None:
            query = query.where(Package.name.ilike(f"%{search}%"))

        if category_id is not None:
            query = query.where(Package.category_id == category_id)

        if min_weight is not None:
            query = query.where(Package.weight >= min_weight)
        if max_weight is not None:
            query = query.where(Package.weight <= max_weight)

        if min_value is not None:
            query = query.where(Package.value_usd >= min_value)
        if max_value is not None:
            query = query.where(Package.value_usd <= max_value)

        query = query.options(selectinload(Package.category))
        result = await self.db_session.execute(query)
        return result.scalars().unique().all()

    async def get_packages_count_by_session(self, session_id: UUID) -> int:
        query = (
            select(func.count(Package.package_id))
            .where(Package.session_id == session_id)
        )

        result = await self.db_session.execute(query)
        return result.scalar() or 0

    async def get_empty_packages(self) -> Sequence[Package] | None:
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
