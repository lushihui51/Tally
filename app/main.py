from fastapi import FastAPI
from app.routes import individual_route
from app.routes import spending_route
from app.routes import statement_route

app = FastAPI(title="Tally")

app.include_router(spending_route.router, prefix="/spending", tags=["spending"])
# app.include_router(individual.router, prefix="/individual", tags=["individual"])
# app.include_router(statement.router, prefix="/statement", tags=["statement"])