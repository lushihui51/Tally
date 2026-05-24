from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal

def get_db():
    with SessionLocal() as db:
        yield db

DbSession = Annotated[Session, Depends(get_db)]