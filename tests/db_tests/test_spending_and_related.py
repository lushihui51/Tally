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

            insert_spenders_individuals(
                [
                    SpendersIndividualInsertSchema(**spenders_individual)
                    for spenders_individual in spenders_individuals
                ],
                db_insert,
            )
            insert_beneficiaries_individuals(
                [
                    BeneficiariesIndividualInsertSchema(**beneficiaries_individual)
                    for beneficiaries_individual in beneficiaries_individuals
                ],
                db_insert,
            )
            insert_spending_secondary_categories(
                [
                    SpendingSecondaryCategoryInsertSchema(**spending_secondary_category)
                    for spending_secondary_category in spending_secondary_categories
                ],
                db_insert,
            )
            db_insert.commit()

        with db_factory() as db_select:
            
