from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base


class PrimaryCategoryModel(Base):
    __tablename__ = 'primary_category'

    primary_category_name: Mapped[str] = mapped_column(String(50), primary_key=True)

    def __repr__(self):
        return super().__repr__()
