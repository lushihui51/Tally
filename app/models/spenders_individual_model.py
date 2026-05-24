from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base


class SpendersIndividualModel(Base):
    __tablename__ = "spenders_individual"

    spending_id: Mapped[int] = mapped_column(ForeignKey("spending.spending_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    individual_name: Mapped[str] = mapped_column(String(50), ForeignKey("individual.individual_name", ondelete="RESTRICT", onupdate="CASCADE"), primary_key=True)
    contribution: Mapped[int]

    def __repr__(self):
        return super().__repr__()
