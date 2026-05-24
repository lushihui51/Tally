from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column
from app.database import Base


class SecondaryCategoryModel(Base):
    __tablename__ = 'secondary_category'

    secondary_category_name = mapped_column(String(50), primary_key=True)

    def __repr__(self):
        return super().__repr__()