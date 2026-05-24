from sqlalchemy import select

from app.models.spending_model import SpendingModel
from app.schemas.primary_category_schema import PrimaryCategoryInsertSchema
from app.schemas.spending_schema import (
    SpendingInsertSchema,
    SpendingResultSchema,
    SpendingSelectSchema,
)
from app.services.db_services.pirmary_category_service import insert_primary_categories
from app.services.db_services.spending_service import insert_spendings, select_spendings
from app.utils.files import json_to_dict


class TestSpendingInsertAndSelect:
    def test_spending_insert_and_select_valid_raw_rand100(
        self, td_spending_and_related_rand100_json, td_primary_category_json, db_factory
    ):
        """Test inserting valid rows into the spending table directly, using 100 random test data."""
        spendings = json_to_dict(td_spending_and_related_rand100_json)["spending"]
        primary_categories = json_to_dict(td_primary_category_json)

        with db_factory() as db_prefill:
            insert_primary_categories(
                [
                    PrimaryCategoryInsertSchema(**primary_category)
                    for primary_category in primary_categories
                ],
                db_prefill,
            )
            db_prefill.commit()

        spending_result_schemas = []

        with db_factory() as db_insert:
            for spending in spendings:
                spending_model = SpendingModel(**spending)
                db_insert.add(spending_model)
                db_insert.flush()
                assert spending_model.spending_id is not None
                spending_result_schemas.append(
                    SpendingResultSchema.model_validate(spending_model)
                )
            db_insert.commit()

        with db_factory() as db_select:
            for spending_result_schema in spending_result_schemas:
                stmt = select(SpendingModel).where(
                    SpendingModel.spending_id == spending_result_schema.spending_id
                )
                result = db_select.scalars(stmt).all()
                assert len(result) == 1
                assert (
                    SpendingResultSchema.model_validate(result[0])
                    == spending_result_schema
                )

    def test_spending_insert_and_select_valid_service_rand100(
        self, td_spending_and_related_rand100_json, db_factory, td_primary_category_json
    ):
        """Test inserting valid rows into the spending table using the service function insert_spendings, using 100 random test data."""
        spendings = json_to_dict(td_spending_and_related_rand100_json)["spending"]
        primary_categories = json_to_dict(td_primary_category_json)

        with db_factory() as db_prefill:
            insert_primary_categories(
                [
                    PrimaryCategoryInsertSchema(**primary_category)
                    for primary_category in primary_categories
                ],
                db_prefill,
            )
            db_prefill.commit()

        spending_insert_schemas = [
            SpendingInsertSchema(**spending) for spending in spendings
        ]
        spending_result_schemas = []

        with db_factory() as db_insert:
            for spending_id, spending in zip(
                insert_spendings(spending_insert_schemas, db_insert), spendings
            ):
                spending["spending_id"] = spending_id
                spending_result_schemas.append(SpendingResultSchema(**spending))
            db_insert.commit()

        with db_factory() as db_select:
            for spending_result_schema in spending_result_schemas:
                spending_models = select_spendings(
                    SpendingSelectSchema(
                        spending_id=spending_result_schema.spending_id
                    ),
                    db_select,
                )
                assert len(spending_models) == 1
                assert (
                    SpendingResultSchema.model_validate(spending_models[0])
                    == spending_result_schema
                )
