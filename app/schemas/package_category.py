from app.db.Base import TunedModel


class PackageCategoryRead(TunedModel):
    category_id: int
    category_name: str
