from decimal import Decimal
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base

class SplitArrangementModel(Base):
    __tablename__ = "split_arrangement"

    individual_a: Mapped[str] = mapped_column(ForeignKey("individual.individual_name", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    individual_b: Mapped[str] = mapped_column(ForeignKey("individual.individual_name", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    a_proportion: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    categories: Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        CheckConstraint("individual_a != individual_b", name = "check_different_individuals"),
        CheckConstraint("individual_a < individual_b", name = "check_ordered_pair")
    )

    def __repr__(self):
        return super().__repr__()