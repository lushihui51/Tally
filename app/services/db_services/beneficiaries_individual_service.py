from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.beneficiaries_individual_model import BeneficiariesIndividualModel
from app.schemas.beneficiaries_individual_schema import (
    BeneficiariesIndividualInsertSchema,
    BeneficiariesIndividualSelectSchema,
)


def insert_beneficiaries_individuals(
    beneficiaries_individuals_data: list[BeneficiariesIndividualInsertSchema],
    db: Session,
) -> list[BeneficiariesIndividualModel]:
    beneficiaries_individuals = [
        BeneficiariesIndividualModel(**data.model_dump())
        for data in beneficiaries_individuals_data
    ]
    db.add_all(beneficiaries_individuals)
    return beneficiaries_individuals


def select_beneficiaries_individuals(
    filters: BeneficiariesIndividualSelectSchema, db: Session
) -> Sequence[BeneficiariesIndividualModel]:
    stmt = select(BeneficiariesIndividualModel).filter_by(
        **filters.model_dump(exclude_none=True)
    )
    result = db.scalars(stmt).all()
    return result
