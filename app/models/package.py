import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.Base import Base


class Package(Base):
    __tablename__ = "packages"

    package_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    weight: Mapped[Decimal] = mapped_column(Numeric(10, 3))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"))
    value_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    delivery_cost_rub: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    session_id: Mapped[uuid.UUID | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.current_timestamp())

    category: Mapped["Category"] = relationship(back_populates="packages")

    @property
    def category_name(self) -> str:
        return self.category.category_name if self.category else None
