from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.primary_category_model import PrimaryCategoryModel
from app.schemas.primary_category_schema import (
    PrimaryCategoryInsertSchema,
    PrimaryCategorySelectSchema,
)


def insert_primary_categories(
    primary_categories_data: list[PrimaryCategoryInsertSchema], db: Session
) -> list[PrimaryCategoryModel]:
    primary_categories = [
        PrimaryCategoryModel(**data.model_dump()) for data in primary_categories_data
    ]
    db.add_all(primary_categories)
    return primary_categories


def select_primary_categories(
    filters: PrimaryCategorySelectSchema, db: Session
) -> Sequence[PrimaryCategoryModel]:
    stmt = select(PrimaryCategoryModel).filter_by(
        **filters.model_dump(exclude_none=True)
    )
    result = db.scalars(stmt).all()
    return result
