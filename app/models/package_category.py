from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship

from app.db.Base import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False, default="")

    packages = relationship("Package", back_populates="category")
