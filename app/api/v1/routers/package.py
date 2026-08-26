from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.openapi_responses import (
    CATEGORY_NOT_FOUND_RESPONSE,
    COMMON_ERROR_RESPONSES,
    PACKAGE_NOT_FOUND_RESPONSE,
)
from app.core.session_manager import get_session_id
from app.db.session import get_session
from app.schemas.package import PackageCreate, PackageList, PackageRead, PaginatedResponse
from app.services.package_service import (
    _create_new_package,
    _get_package_by_id,
    _get_packages_by_session,
)

package_router = APIRouter()

@package_router.post(
    "/",
    response_model=PackageRead,
    summary="Создать новую посылку",
    description="Создать новую посылку.\nтребует name, weight, category_id, value в usd",
    responses=CATEGORY_NOT_FOUND_RESPONSE | COMMON_ERROR_RESPONSES,
)
async def create_new_package(
        body: PackageCreate,
        session_id: UUID = Depends(get_session_id),
        session: AsyncSession = Depends(get_session)
) -> PackageRead:

    return await _create_new_package(session=session, session_id=session_id, body=body)


@package_router.get(
    "/",
    response_model=PaginatedResponse[PackageList],
    summary="Получить все посылки этой сессии.",
    description="Получить все посылки этой сессии.",
    responses=COMMON_ERROR_RESPONSES,
)
async def get_packages_by_session(
        session_id: UUID = Depends(get_session_id),
        session: AsyncSession = Depends(get_session),
        page: int = Query(1, gt=0, le=100, description="Номер страницы"),
        size: int = Query(5, gt=0, description="Количество посылок на 1 странице"),
        sort_by: str | None = Query(
            None,
            description="Поле сортировки. Префикс `-` — по убыванию. Пример: `-created_at`, `name`",
        ),
        search: str | None = Query(None, description="Поиск по названию"),
        category_id: int | None = Query(None, description="Фильтр по ID категории"),
        min_weight: Decimal | None = Query(None, description="Минимальный вес (кг)"),
        max_weight: Decimal | None = Query(None, description="Максимальный вес (кг)"),
        min_value: Decimal | None = Query(None, description="Минимальная цена (доллары)"),
        max_value: Decimal | None = Query(None, description="Максимальная цена (доллары)"),
    ) -> PaginatedResponse[PackageList]:

    return await _get_packages_by_session(
        session=session,
        session_id=session_id,
        page=page,
        size=size,
        sort_by=sort_by,
        search=search,
        category_id=category_id,
        min_weight=min_weight,
        max_weight=max_weight,
        min_value=min_value,
        max_value=max_value,
    )


@package_router.get(
    "/{package_id}", response_model=PackageRead,
    summary="Получить посылку по id.",
    description="Получить подробную информацию о посылке по uuid.",
    responses=PACKAGE_NOT_FOUND_RESPONSE | COMMON_ERROR_RESPONSES,
)
async def get_package_by_id(
        package_id: UUID,
        session: AsyncSession = Depends(get_session)
    ) -> PackageRead:

    return await _get_package_by_id(session=session, package_id=package_id)
