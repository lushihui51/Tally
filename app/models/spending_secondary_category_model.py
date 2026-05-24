from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SpendingSecondaryCategoryModel(Base):
    __tablename__ = "spending_secondary_category"

    spending_id: Mapped[int] = mapped_column(
        ForeignKey("spending.spending_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    secondary_category_name: Mapped[str] = mapped_column(
        String(50),
        ForeignKey(
            "secondary_category.secondary_category_name",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )

    def __repr__(self):
        return super().__repr__()
