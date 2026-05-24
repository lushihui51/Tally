from app.schemas.base_schema import BaseSchema


class SpendingSecondaryCategoryInsertSchema(BaseSchema):
    spending_id: int
    secondary_category_name: str


class SpendingSecondaryCategorySelectSchema(BaseSchema):
    spending_id: int | None = None
    secondary_category_name: str | None = None


class SpendingSecondaryCategoryResultSchema(BaseSchema):
    spending_id: int
    secondary_category_name: str
