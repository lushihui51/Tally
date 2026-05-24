from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import config
from app.database import Base
from app.dependencies.db_dependency import get_db
from app.main import app

TEST_DATABASE_URL = config.settings.TEST_DATABASE_URL
engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    with TestSessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


def assert_model_obj_matches_schema_obj(model: Base, schema: BaseModel) -> None:
    for field_name, field_value in schema:
        assert hasattr(model, field_name), f"Model missing attribute: {field_name}"
        attr_val = getattr(model, field_name)
        assert attr_val == field_value, (
            f"Mismatch on {field_name}: {attr_val} != {field_value}\nComparing type {type(attr_val)} with type {type(field_value)}"
        )


@pytest.fixture
def project_root(request):
    return Path(request.config.rootdir)


@pytest.fixture
def td_individual_json(project_root):
    return project_root / "tests" / "test_data" / "json" / "td_individual.json"


@pytest.fixture
def td_primary_category_json(project_root):
    return project_root / "tests" / "test_data" / "json" / "td_primary_category.json"


@pytest.fixture
def td_secondary_category_json(project_root):
    return project_root / "tests" / "test_data" / "json" / "td_secondary_category.json"


@pytest.fixture
def td_spending_and_related_rand5_json(project_root):
    return (
        project_root
        / "tests"
        / "test_data"
        / "json"
        / "td_spending_and_related_rand5.json"
    )


@pytest.fixture
def td_spending_and_related_rand100_json(project_root):
    return (
        project_root
        / "tests"
        / "test_data"
        / "json"
        / "td_spending_and_related_rand100.json"
    )


@pytest.fixture
def td_split_arrangement_json(project_root):
    return project_root / "tests" / "test_data" / "json" / "td_split_arrangement.json"


@pytest.fixture
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(setup_db):
    with TestSessionLocal() as session:
        yield session


@pytest.fixture
def db_factory(setup_db):
    def _create_session():
        return TestSessionLocal()

    return _create_session


@pytest.fixture
def client(setup_db):
    with TestClient(app) as c:
        yield c
