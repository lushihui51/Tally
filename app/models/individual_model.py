from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base


class IndividualModel(Base):
    __tablename__ = 'individual'

    individual_name: Mapped[str] = mapped_column(String(50), primary_key=True)