import uuid

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, UUID
from sqlalchemy.orm import relationship

from app.db.Base import Base


class Package(Base):
    __tablename__ = "packages"

    package_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    weight = Column(Numeric(10, 3), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    value_usd = Column(Numeric(12, 2))
    delivery_cost_rub = Column(Numeric(12, 2))
    session_id = Column(UUID(as_uuid=True))

    category = relationship("Category", back_populates="packages")

    @property
    def category_name(self) -> str:
        return self.category.category_name if self.category else None
