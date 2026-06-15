from app.db.Base import TunedModel


class PackageCategoryRead(TunedModel):
    id: int
    category_name: str
