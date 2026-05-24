from fastapi import APIRouter
from app.schemas.spending_schema import SpendingInsertSchema
from app.dependencies.db_dependency import DbSession
from app.services.db_services.spending_service import select_all_spendings
from app.services.db_services.spending_service import insert_spendings

router = APIRouter()

@router.get("/")
def read_all_spendings(db: DbSession):
    return select_all_spendings(db)

@router.post("/")
def create_spending(spending_data: SpendingInsertSchema, db: DbSession):
    return insert_spendings([spending_data], db)