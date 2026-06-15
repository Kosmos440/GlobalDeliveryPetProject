from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session_manager import get_session_id
from app.db.session import get_session
from app.repositories.package import PackageDAL
from app.schemas.package import PackageCreate, PackageRead, PackageList

logger = structlog.get_logger(__name__)
package_router = APIRouter()

@package_router.post(
    "/",
    response_model=PackageRead,
    summary="Create a new package",
    description="Create a new package.\nRequires name, weight, category_id, value in usd",
)
async def create_new_package(
        body: PackageCreate,
        session_id: UUID = Depends(get_session_id),
        session: AsyncSession = Depends(get_session)
) -> PackageRead:
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


@package_router.get(
    "/", response_model=list[PackageList],
    summary="Get all packages by session",
    description="Get all packages by session.",
)
async def get_package_by_session(
        session_id: UUID = Depends(get_session_id),
        session: AsyncSession = Depends(get_session),

    ) -> list[PackageList]:

    package_dal = PackageDAL(session)
    packages =  await package_dal.get_all_packages_by_session(session_id=session_id)

    if not packages:
        logger.warning(
            "package.session.not_found",
            session_id=str(session_id),
        )
        raise HTTPException(
            status_code=404,
            detail=f"Packages.not_found."
        )
    logger.info(
        "package.session.listed",
        session_id=str(session_id),
        packages_count=len(packages),
    )
    return packages


@package_router.get(
    "/{package_id}", response_model=PackageRead,
    summary="Get package by id",
    description="Get all packages by session.",
)
async def get_package_by_id(
        package_id: UUID | None = None,
        session: AsyncSession = Depends(get_session)
    ) -> PackageRead:
    package_dal = PackageDAL(session)
    package = await package_dal.get_package_by_id(package_id=package_id)

    if not package:
        logger.warning(
            "package.not_found",
            package_id=str(package_id),
        )
        raise HTTPException(
            status_code=404,
            detail=f"Package.not_found."
        )
    logger.info(
        "package.retrieved",
        package_id=str(package.package_id),
    )
    return package
