from app.schemas.base_schema import BaseSchema


class PrimaryCategoryInsertSchema(BaseSchema):
    primary_category_name: str


class PrimaryCategorySelectSchema(BaseSchema):
    primary_category_name: str | None = None


class PrimaryCategoryResultSchema(BaseSchema):
    primary_category_name: str
