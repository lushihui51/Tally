from sqlalchemy import select

from app.models.primary_category_model import PrimaryCategoryModel
from app.schemas.primary_category_schema import (
    PrimaryCategoryInsertSchema,
    PrimaryCategorySelectSchema,
)
from app.services.db_services.pirmary_category_service import (
    insert_primary_categories,
    select_primary_categories,
)
from app.utils.files import json_to_dict


class TestPrimaryCategoryInsertAndSelect:
    def test_primary_category_insert_and_select_valid_raw(
        self, td_primary_category_json, db_factory
    ):
        """Test inserting valid rows into the primary_category table directly."""
        primary_categories = json_to_dict(td_primary_category_json)
        primary_category_models = []

        with db_factory() as db_insert:
            for primary_category in primary_categories:
                primary_category_model = PrimaryCategoryModel(**primary_category)
                db_insert.add(primary_category_model)
                primary_category_models.append(primary_category_model)
            db_insert.commit()

        with db_factory() as db_select:
            for primary_category in primary_categories:
                stmt = select(PrimaryCategoryModel).where(
                    PrimaryCategoryModel.primary_category_name
                    == primary_category["primary_category_name"]
                )
                result = db_select.scalars(stmt).all()
                assert len(result) == 1

    def test_primary_category_insert_and_select_valid_service(
        self, td_primary_category_json, db_factory
    ):
        """Test inserting valid rows into the primary_category table using the service function insert_primary_categories."""
        primary_categories = json_to_dict(td_primary_category_json)

        with db_factory() as db_insert:
            insert_primary_categories(
                [
                    PrimaryCategoryInsertSchema(**primary_category)
                    for primary_category in primary_categories
                ],
                db_insert,
            )
            db_insert.commit()

        with db_factory() as db_select:
            primary_category_models = select_primary_categories(
                PrimaryCategorySelectSchema(), db_select
            )
            assert len(primary_category_models) == len(primary_categories)
            result_names = {r.primary_category_name for r in primary_category_models}
            expected_names = {e["primary_category_name"] for e in primary_categories}
            assert result_names == expected_names
