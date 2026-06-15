from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, ConfigDict


class Base(DeclarativeBase):
    pass


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
