from decimal import Decimal

from app.schemas.base_schema import BaseSchema


class SpendersIndividualInsertSchema(BaseSchema):
    spending_id: int
    individual_name: str
    contribution: Decimal


class SpendersIndividualSelectSchema(BaseSchema):
    spending_id: int | None = None
    individual_name: str | None = None
    contribution: Decimal | None = None


class SpendersIndividualResultSchema(BaseSchema):
    spending_id: int
    individual_name: str
    contribution: Decimal
