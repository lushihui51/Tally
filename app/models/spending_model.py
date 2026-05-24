from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.database import Base


class SpendingModel(Base):
    __tablename__ = "spending"

    spending_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255))
    aggregated: Mapped[bool]
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    spending_date: Mapped[date] = mapped_column(Date)
    essential: Mapped[bool]
    settled: Mapped[bool]
    primary_category_name: Mapped[str] = mapped_column(
        String(50),
        ForeignKey(
            "primary_category.primary_category_name",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
    )
    store_name: Mapped[str] = mapped_column(String(50))
    store_location: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return super().__repr__()

    @validates("cost")
    def validate_cost(self, key, value):
        if isinstance(value, str):
            return Decimal(value)
        return value

    @validates("date")
    def validate_date(self, key, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value
