from app.schemas.base_schema import BaseSchema


class IndividualInsertSchema(BaseSchema):
    individual_name: str


class IndividualSelectSchema(BaseSchema):
    individual_name: str | None = None


class IndividualResultSchema(BaseSchema):
    individual_name: str
