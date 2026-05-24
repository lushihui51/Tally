from sqlalchemy import select

from app.models.secondary_category_model import SecondaryCategoryModel
from app.schemas.secondary_category_schema import (
    SecondaryCategoryInsertSchema,
    SecondaryCategorySelectSchema,
)
from app.services.db_services.secondary_category_service import (
    insert_secondary_categories,
    select_secondary_categories,
)
from app.utils.files import json_to_dict


class TestSecondaryCategoryInsertAndSelect:
    def test_secondary_category_insert_and_select_valid_raw(
        self, td_secondary_category_json, db_factory
    ):
        """Test inserting valid rows into the secondary_category table directly."""
        secondary_categories = json_to_dict(td_secondary_category_json)
        secondary_category_models = []

        with db_factory() as db_insert:
            for secondary_category in secondary_categories:
                secondary_category_model = SecondaryCategoryModel(**secondary_category)
                db_insert.add(secondary_category_model)
                secondary_category_models.append(secondary_category_model)
            db_insert.commit()

        with db_factory() as db_select:
            for secondary_category in secondary_categories:
                stmt = select(SecondaryCategoryModel).where(
                    SecondaryCategoryModel.secondary_category_name
                    == secondary_category["secondary_category_name"]
                )
                result = db_select.scalars(stmt).all()
                assert len(result) == 1

    def test_secondary_category_insert_and_select_valid_service(
        self, td_secondary_category_json, db_factory
    ):
        """Test inserting valid rows into the secondary_category table using the service function insert_secondary_categories."""
        secondary_categories = json_to_dict(td_secondary_category_json)

        with db_factory() as db_insert:
            insert_secondary_categories(
                [
                    SecondaryCategoryInsertSchema(**secondary_category)
                    for secondary_category in secondary_categories
                ],
                db_insert,
            )
            db_insert.commit()

        with db_factory() as db_select:
            secondary_category_models = select_secondary_categories(
                SecondaryCategorySelectSchema(), db_select
            )
            assert len(secondary_category_models) == len(secondary_categories)
            result_names = {
                r.secondary_category_name for r in secondary_category_models
            }
            expected_names = {
                e["secondary_category_name"] for e in secondary_categories
            }
            assert result_names == expected_names
