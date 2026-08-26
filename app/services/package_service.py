from decimal import Decimal
from math import ceil
from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.exceptions.category import CategoryNotFoundException
from app.exceptions.package import PackageNotFoundException
from app.models.package import Package
from app.repositories.package import PackageDAL
from app.repositories.package_category import PackageCategoryDAL
from app.schemas.package import PackageCreate, PackageList, PackageRead, PaginatedResponse

logger = structlog.get_logger(__name__)

async def _create_new_package(body: PackageCreate, session: AsyncSession, session_id: UUID) -> PackageRead:
    package_category_dal = PackageCategoryDAL(session)
    if not await package_category_dal.get_id_in_categories(category_id=body.category_id):
        logger.warning(
            "category.not_found",
            category_id=str(body.category_id),
        )
        raise CategoryNotFoundException(category_id=body.category_id)

    package_dal = PackageDAL(session)
    package = await package_dal.create_package(
        name=body.name,
        weight=body.weight,
        category_id=body.category_id,
        value_usd=body.value_usd,
        session_id=session_id
    )
    logger.info("package.created", package_id=str(package.package_id))
    return package


async def _get_packages_by_session(
        session: AsyncSession,
        session_id: UUID,
        page: int,
        size: int,
        sort_by: str | None = None,
        search: str | None = None,
        category_id: int | None = None,
        min_weight: Decimal | None = None,
        max_weight: Decimal | None = None,
        min_value: Decimal | None = None,
        max_value: Decimal | None = None,
    ) -> PaginatedResponse[PackageList]:

    change_direction: bool | None = False
    column: InstrumentedAttribute | None = None

    if sort_by is not None:
        change_direction = sort_by[0] == '-'
        sort_by = sort_by.replace('-', '')
        column = getattr(Package, sort_by, None)

    package_dal = PackageDAL(session)
    packages = await package_dal.get_filtered_packages_by_session(
        session_id=session_id,
        page=page,
        size=size,
        column=column,
        change_direction=change_direction,
        search=search,
        category_id=category_id,
        min_weight=min_weight,
        max_weight=max_weight,
        min_value=min_value,
        max_value=max_value,
    )
    logger.info(
        "package.session.listed",
        session_id=str(session_id),
        packages_count=len(packages),
    )
    total_packages = await package_dal.get_packages_count_by_session(session_id=session_id)
    return PaginatedResponse(packages=packages, current_page=page, total_pages=ceil(total_packages / size), page_size=size)


async def _get_package_by_id(session: AsyncSession, package_id: UUID) -> PackageRead:
    package_dal = PackageDAL(session)
    package = await package_dal.get_package_by_id(package_id=package_id)

    if not package:
        logger.warning(
            "package.not_found",
            package_id=str(package_id),
        )
        raise PackageNotFoundException(package_id)
    logger.info(
        "package.retrieved",
        package_id=str(package.package_id),
    )
    return package
