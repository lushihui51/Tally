from datetime import date
from decimal import Decimal

from app.schemas.base_schema import BaseSchema


class SpendingInsertSchema(BaseSchema):
    description: str
    aggregated: bool
    cost: Decimal
    spending_date: date
    essential: bool
    settled: bool
    primary_category_name: str
    store_name: str
    store_location: str


class SpendingSelectSchema(BaseSchema):
    spending_id: int | None = None
    aggregated: bool | None = None
    cost: Decimal | None = None
    spending_date: date | None = None
    essential: bool | None = None
    settled: bool | None = None
    primary_category_name: str | None = None
    store_name: str | None = None
    store_location: str | None = None


class SpendingResultSchema(BaseSchema):
    spending_id: int
    description: str
    aggregated: bool
    cost: Decimal
    spending_date: date
    essential: bool
    settled: bool
    primary_category_name: str
    store_name: str
    store_location: str
