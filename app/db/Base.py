from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
