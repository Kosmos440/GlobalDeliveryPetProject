import uuid
from decimal import Decimal

from pydantic import Field, model_validator

from app.db.Base import TunedModel


class PackageCreate(TunedModel):
    name: str
    weight: Decimal = Field(gt=0, max_digits=10, decimal_places=3)
    category_id: int
    value_usd: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class PackageRead(TunedModel):
    package_id: uuid.UUID
    name: str
    weight: Decimal
    category_id: int
    category_name: str | None = None
    value_usd: Decimal
    delivery_cost_rub: Decimal | str | None

    @model_validator(mode="after")
    def check_status(self):
        if self.delivery_cost_rub is None:
            self.delivery_cost_rub = "Не рассчитано"
        return self


class PackageList(TunedModel):
    package_id: uuid.UUID
    name: str
    category_name: str
    delivery_cost_rub: Decimal | str | None

    @model_validator(mode="after")
    def check_status(self):
        if self.delivery_cost_rub is None:
            self.delivery_cost_rub = "Не рассчитано"
        return self
