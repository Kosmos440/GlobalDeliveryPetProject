import uuid
from datetime import datetime
from decimal import Decimal
from typing import Generic, TypeVar

from pydantic import Field, field_serializer

from app.db.Base import TunedModel

T = TypeVar('T')

class CheckStatusSerializerMixIn:
    @field_serializer("delivery_cost_rub")
    def serialize_delivery_cost(self, value: Decimal | None) -> Decimal | str:
        if value is None:
            return "Не рассчитано"
        return value


class PackageCreate(TunedModel):
    name: str = Field(min_length=3, max_length=50)
    weight: Decimal = Field(gt=0, max_digits=10, decimal_places=3)
    category_id: int
    value_usd: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class PackageRead(CheckStatusSerializerMixIn, TunedModel):
    package_id: uuid.UUID
    name: str
    weight: Decimal
    category_id: int
    category_name: str | None = None
    value_usd: Decimal
    delivery_cost_rub: Decimal | None
    created_at: datetime


class PackageList(CheckStatusSerializerMixIn, TunedModel):
    package_id: uuid.UUID
    name: str
    weight: Decimal
    category_name: str
    value_usd: Decimal
    delivery_cost_rub: Decimal | None
    created_at: datetime


class PaginatedResponse(TunedModel, Generic[T]):
    packages: list[T]
    current_page: int
    total_pages: int
    page_size: int
