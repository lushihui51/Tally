from app.schemas.base_schema import BaseSchema


class BeneficiariesIndividualInsertSchema(BaseSchema):
    spending_id: int
    individual_name: str


class BeneficiariesIndividualSelectSchema(BaseSchema):
    spending_id: int | None = None
    individual_name: str | None = None


class BeneficiariesIndividualResultSchema(BaseSchema):
    spending_id: int
    individual_name: str
