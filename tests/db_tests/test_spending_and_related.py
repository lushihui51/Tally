from sqlalchemy import func, select, table

from app.schemas.beneficiaries_individual_schema import (
    BeneficiariesIndividualInsertSchema,
)
from app.schemas.individual_schema import IndividualInsertSchema
from app.schemas.primary_category_schema import PrimaryCategoryInsertSchema
from app.schemas.secondary_category_schema import SecondaryCategoryInsertSchema
from app.schemas.spenders_individual_schema import SpendersIndividualInsertSchema
from app.schemas.spending_schema import SpendingInsertSchema
from app.schemas.spending_secondary_category_schema import (
    SpendingSecondaryCategoryInsertSchema,
)
from app.services.db_services.beneficiaries_individual_service import (
    insert_beneficiaries_individuals,
)
from app.services.db_services.individual_service import insert_individuals
from app.services.db_services.pirmary_category_service import insert_primary_categories
from app.services.db_services.secondary_category_service import (
    insert_secondary_categories,
)
from app.services.db_services.spenders_individual_service import (
    insert_spenders_individuals,
)
from app.services.db_services.spending_secondary_category_service import (
    insert_spending_secondary_categories,
)
from app.services.db_services.spending_service import insert_spendings
from app.utils.files import json_to_dict


class TestSpendingAndRelatedInsertAndSelect:
    def test_spending_and_related_valid_service_rand100(
        self,
        td_spending_and_related_rand100_json,
        td_individual_json,
        td_primary_category_json,
        td_secondary_category_json,
        db_factory,
    ):
        spending_and_related = json_to_dict(td_spending_and_related_rand100_json)
        spendings = spending_and_related["spending"]
        spenders_individuals = spending_and_related["spenders_individual"]
        beneficiaries_individuals = spending_and_related["beneficiaries_individual"]
        spending_secondary_categories = spending_and_related[
            "spending_secondary_category"
        ]
        individuals = json_to_dict(td_individual_json)
        primary_categories = json_to_dict(td_primary_category_json)
        secondary_categories = json_to_dict(td_secondary_category_json)

        with db_factory() as db_prefill:
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
            insert_secondary_categories(
                [
                    SecondaryCategoryInsertSchema(**secondary_category)
                    for secondary_category in secondary_categories
                ],
                db_prefill,
            )
            db_prefill.commit()

        with db_factory() as db_insert:
            spending_ids = insert_spendings(
                [SpendingInsertSchema(**spending) for spending in spendings], db_insert
            )
            for (
                spenders_individual,
                beneficiaries_individual,
                spending_secondary_category,
                spending_id,
            ) in zip(
                spenders_individuals,
                beneficiaries_individuals,
                spending_secondary_categories,
                spending_ids,
            ):
                spenders_individual["spending_id"] = spending_id
                beneficiaries_individual["spending_id"] = spending_id
                spending_secondary_category["spending_id"] = spending_id

            spenders_individual_rows = []
            for spenders_individual in spenders_individuals:
                individual_names = spenders_individual["individual_names"]
                contributions = spenders_individual["contributions"]
                spending_id = spenders_individual["spending_id"]

                assert individual_names, "individual_names cannot be empty"
                assert contributions, "contributions cannot be empty"
                assert len(individual_names) == len(contributions), (
                    "individual_names and contributions must have the same length"
                )

                for individual_name, contribution in zip(
                    individual_names, contributions
                ):
                    spenders_individual_rows.append(
                        SpendersIndividualInsertSchema(
                            individual_name=individual_name,
                            contribution=contribution,
                            spending_id=spending_id,
                        )
                    )

            insert_spenders_individuals(
                spenders_individual_rows,
                db_insert,
            )
            beneficiaries_individual_rows = []
            for beneficiaries_individual in beneficiaries_individuals:
                individual_names = beneficiaries_individual.get("individual_names")
                spending_id = beneficiaries_individual["spending_id"]

                if individual_names is None:
                    beneficiaries_individual_rows.append(
                        BeneficiariesIndividualInsertSchema(**beneficiaries_individual)
                    )
                    continue

                assert individual_names, "individual_names cannot be empty"

                for individual_name in individual_names:
                    beneficiaries_individual_rows.append(
                        BeneficiariesIndividualInsertSchema(
                            individual_name=individual_name,
                            spending_id=spending_id,
                        )
                    )

            insert_beneficiaries_individuals(
                beneficiaries_individual_rows,
                db_insert,
            )
            spending_secondary_category_rows = []
            for spending_secondary_category in spending_secondary_categories:
                secondary_category_names = spending_secondary_category.get(
                    "secondary_category_names"
                )
                spending_id = spending_secondary_category["spending_id"]

                assert secondary_category_names, (
                    "secondary_category_names cannot be empty"
                )

                for secondary_category_name in secondary_category_names:
                    spending_secondary_category_rows.append(
                        SpendingSecondaryCategoryInsertSchema(
                            secondary_category_name=secondary_category_name,
                            spending_id=spending_id,
                        )
                    )

            insert_spending_secondary_categories(
                spending_secondary_category_rows,
                db_insert,
            )
            db_insert.commit()

        with db_factory() as db_select:

            def _count_rows(table_candidates):
                for table_name in table_candidates:
                    try:
                        table_ref = table(table_name)
                        stmt = select(func.count()).select_from(table_ref)
                        return db_select.execute(stmt).scalar_one()
                    except Exception:
                        continue
                raise AssertionError(
                    f"Could not query any of the candidate tables: {table_candidates}"
                )

            spendings_count = _count_rows(["spending", "spendings"])
            spenders_count = _count_rows(
                ["spenders_individual", "spenders_individuals"]
            )
            beneficiaries_count = _count_rows(
                ["beneficiaries_individual", "beneficiaries_individuals"]
            )
            spending_secondary_categories_count = _count_rows(
                ["spending_secondary_category", "spending_secondary_categories"]
            )

            assert spendings_count == len(spendings)
            assert spenders_count == len(spenders_individual_rows)
            assert beneficiaries_count == len(beneficiaries_individual_rows)
            assert spending_secondary_categories_count == len(
                spending_secondary_category_rows
            )
