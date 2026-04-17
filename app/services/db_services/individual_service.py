from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.individual_model import IndividualModel
from app.schemas.individual_schema import IndividualInsertSchema, IndividualSelectSchema


def insert_individuals(
    individuals_data: list[IndividualInsertSchema], db: Session
) -> list[IndividualModel]:
    individuals = [IndividualModel(**data.model_dump()) for data in individuals_data]
    db.add_all(individuals)
    return individuals


def select_individuals(
    filters: IndividualSelectSchema, db: Session
) -> Sequence[IndividualModel]:
    stmt = select(IndividualModel).filter_by(**filters.model_dump(exclude_none=True))
    result = db.scalars(stmt).all()
    return result
