from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.spenders_individual_model import SpendersIndividualModel
from app.schemas.spenders_individual_schema import (
    SpendersIndividualInsertSchema,
    SpendersIndividualSelectSchema,
)


def insert_spenders_individuals(
    spenders_individuals_data: list[SpendersIndividualInsertSchema], db: Session
) -> list[SpendersIndividualModel]:
    spenders_individuals = [
        SpendersIndividualModel(**data.model_dump())
        for data in spenders_individuals_data
    ]
    db.add_all(spenders_individuals)
    return spenders_individuals


def select_spenders_individuals(
    filters: SpendersIndividualSelectSchema, db: Session
) -> Sequence[SpendersIndividualModel]:
    stmt = select(SpendersIndividualModel).filter_by(
        **filters.model_dump(exclude_none=True)
    )
    result = db.scalars(stmt).all()
    return result
