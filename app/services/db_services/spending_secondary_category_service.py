from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.spending_secondary_category_model import SpendingSecondaryCategoryModel
from app.schemas.spending_secondary_category_schema import (
    SpendingSecondaryCategoryInsertSchema,
    SpendingSecondaryCategorySelectSchema,
)


def insert_spending_secondary_categories(
    spending_secondary_categories_data: list[SpendingSecondaryCategoryInsertSchema],
    db: Session,
) -> list[SpendingSecondaryCategoryModel]:
    spending_secondary_categories = [
        SpendingSecondaryCategoryModel(**data.model_dump())
        for data in spending_secondary_categories_data
    ]
    db.add_all(spending_secondary_categories)
    return spending_secondary_categories


def select_spending_secondary_categories(
    filters: SpendingSecondaryCategorySelectSchema, db: Session
) -> Sequence[SpendingSecondaryCategoryModel]:
    stmt = select(SpendingSecondaryCategoryModel).filter_by(
        **filters.model_dump(exclude_none=True)
    )
    result = db.scalars(stmt).all()
    return result
