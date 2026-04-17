from sqlalchemy import select

from app.models.split_arrangement_model import SplitArrangementModel
from app.schemas.individual_schema import IndividualInsertSchema
from app.schemas.primary_category_schema import PrimaryCategoryInsertSchema
from app.schemas.split_arrangement_schema import (
    SplitArrangementInsertSchema,
    SplitArrangementResultSchema,
    SplitArrangementSelectSchema,
)
from app.services.db_services.individual_service import insert_individuals
from app.services.db_services.pirmary_category_service import insert_primary_categories
from app.services.db_services.split_arrangement_service import (
    insert_split_arrangements,
    select_split_arrangements,
)
from app.utils.files import json_to_dict


class TestSplitArrangementInsertAndSelect:
    def test_split_arrangement_insert_and_select_valid_raw(
        self,
        td_split_arrangement_json,
        td_individual_json,
        td_primary_category_json,
        db_factory,
    ):
        """Test inserting valid rows into the split_arrangement table directly."""

        with db_factory() as db_prefill:
            individuals = json_to_dict(td_individual_json)
            primary_categories = json_to_dict(td_primary_category_json)
            insert_individuals(
                [IndividualInsertSchema(**individual) for individual in individuals],
                db_prefill,
            )
            insert_primary_categories(
                [
                    PrimaryCategoryInsertSchema(**primary_category)
                    for primary_category in primary_categories
                ],
                db_prefill,
            )
            db_prefill.commit()

        split_arrangements = json_to_dict(td_split_arrangement_json)
        split_arrangement_insert_schemas = []

        with db_factory() as db_insert:
            for split_arrangement in split_arrangements:
                db_insert.add(SplitArrangementModel(**split_arrangement))
                split_arrangement_insert_schemas.append(
                    SplitArrangementInsertSchema(**split_arrangement)
                )

            db_insert.commit()

        with db_factory() as db_select:
            for split_arrangement_insert_schema in split_arrangement_insert_schemas:
                stmt = select(SplitArrangementModel).where(
                    SplitArrangementModel.individual_a
                    == split_arrangement_insert_schema.individual_a
                    and SplitArrangementModel.individual_b
                    == split_arrangement_insert_schema.individual_b
                )
                result = db_select.scalars(stmt).all()
                assert len(result) == 1
                assert (
                    SplitArrangementResultSchema.model_validate(result[0]).model_dump()
                    == split_arrangement_insert_schema.model_dump()
                )

    def test_split_arrangement_insert_and_select_valid_service(
        self,
        td_split_arrangement_json,
        td_individual_json,
        td_primary_category_json,
        db_factory,
    ):
        """Test inserting valid rows into the split_arrangement table using the service function insert_split_arrangements."""

        with db_factory() as db_prefill:
            individuals = json_to_dict(td_individual_json)
            primary_categories = json_to_dict(td_primary_category_json)
            insert_individuals(
                [IndividualInsertSchema(**individual) for individual in individuals],
                db_prefill,
            )
            insert_primary_categories(
                [
                    PrimaryCategoryInsertSchema(**primary_category)
                    for primary_category in primary_categories
                ],
                db_prefill,
            )
            db_prefill.commit()

        split_arrangements = json_to_dict(td_split_arrangement_json)
        split_arrangement_insert_schemas = [
            SplitArrangementInsertSchema(**split_arrangement)
            for split_arrangement in split_arrangements
        ]

        with db_factory() as db_insert:
            insert_split_arrangements(
                split_arrangement_insert_schemas,
                db_insert,
            )
            db_insert.commit()

        with db_factory() as db_select:
            for split_arrangement_insert_schema in split_arrangement_insert_schemas:
                split_arrangement_models = select_split_arrangements(
                    SplitArrangementSelectSchema(
                        individual_a=split_arrangement_insert_schema.individual_a,
                        individual_b=split_arrangement_insert_schema.individual_b,
                    ),
                    db_select,
                )
                assert len(split_arrangement_models) == 1
                assert (
                    SplitArrangementResultSchema.model_validate(
                        split_arrangement_models[0]
                    ).model_dump()
                    == split_arrangement_insert_schema.model_dump()
                )
