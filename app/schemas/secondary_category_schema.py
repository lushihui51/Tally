from app.schemas.base_schema import BaseSchema


class SecondaryCategoryInsertSchema(BaseSchema):
    secondary_category_name: str


class SecondaryCategorySelectSchema(BaseSchema):
    secondary_category_name: str | None = None


class SecondaryCategoryResultSchema(BaseSchema):
    secondary_category_name: str
