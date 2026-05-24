from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.split_arrangement_model import SplitArrangementModel
from app.schemas.split_arrangement_schema import (
    SplitArrangementInsertSchema,
    SplitArrangementSelectSchema,
)


def insert_split_arrangements(
    split_arrangements_data: list[SplitArrangementInsertSchema], db: Session
) -> list[SplitArrangementModel]:
    split_arrangements = [
        SplitArrangementModel(**data.model_dump()) for data in split_arrangements_data
    ]
    db.add_all(split_arrangements)
    return split_arrangements


def select_split_arrangements(
    filters: SplitArrangementSelectSchema, db: Session
) -> Sequence[SplitArrangementModel]:
    stmt = select(SplitArrangementModel).filter_by(
        **filters.model_dump(exclude_none=True)
    )
    result = db.scalars(stmt).all()
    return result
