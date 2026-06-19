from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.Base import Base


class Category(Base):
    __tablename__ = 'categories'

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(nullable=False, default="")

    packages: Mapped["Package"] = relationship(back_populates="category")
