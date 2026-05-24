from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.secondary_category_model import SecondaryCategoryModel
from app.schemas.secondary_category_schema import (
    SecondaryCategoryInsertSchema,
    SecondaryCategorySelectSchema,
)


def insert_secondary_categories(
    secondary_categories_data: list[SecondaryCategoryInsertSchema], db: Session
) -> list[SecondaryCategoryModel]:
    secondary_categories = [
        SecondaryCategoryModel(**data.model_dump())
        for data in secondary_categories_data
    ]
    db.add_all(secondary_categories)
    return secondary_categories


def select_secondary_categories(
    filters: SecondaryCategorySelectSchema, db: Session
) -> Sequence[SecondaryCategoryModel]:
    stmt = select(SecondaryCategoryModel).filter_by(
        **filters.model_dump(exclude_none=True)
    )
    result = db.scalars(stmt).all()
    return result
