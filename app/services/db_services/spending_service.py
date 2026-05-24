from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.spending_model import SpendingModel
from app.schemas.spending_schema import SpendingInsertSchema, SpendingSelectSchema


def insert_spendings(
    spendings_data: list[SpendingInsertSchema], db: Session
) -> list[int]:
    spendings = [SpendingModel(**data.model_dump()) for data in spendings_data]
    db.add_all(spendings)
    db.flush()
    spending_ids = [spending.spending_id for spending in spendings]
    return spending_ids


def select_spendings(
    filters: SpendingSelectSchema, db: Session
) -> Sequence[SpendingModel]:
    stmt = select(SpendingModel).filter_by(**filters.model_dump(exclude_none=True))
    result = db.scalars(stmt).all()
    return result


def select_all_spendings(db: Session) -> Sequence[SpendingModel]:
    stmt = select(SpendingModel)
    result = db.scalars(stmt).all()
    return result
