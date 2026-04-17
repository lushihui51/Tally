from __future__ import annotations

from decimal import Decimal

from app.schemas.base_schema import BaseSchema


class BooleanExpASTOperands(BaseSchema):
    primary_category_name: str | None = None
    secondary_category_name: str | None = None


class BooleanExpAST(BaseSchema):
    AND: list[BooleanExpAST | BooleanExpASTOperands] | None = None
    OR: list[BooleanExpAST | BooleanExpASTOperands] | None = None
    NOT: BooleanExpAST | BooleanExpASTOperands | None = None
    primary_category_name: str | None = None
    secondary_category_name: str | None = None


class SplitArrangementInsertSchema(BaseSchema):
    individual_a: str
    individual_b: str
    a_proportion: Decimal
    categories: BooleanExpAST


class SplitArrangementSelectSchema(BaseSchema):
    individual_a: str | None = None
    individual_b: str | None = None
    a_proportion: Decimal | None = None
    categories: BooleanExpAST | None = None


class SplitArrangementResultSchema(BaseSchema):
    individual_a: str
    individual_b: str
    a_proportion: Decimal
    categories: BooleanExpAST
