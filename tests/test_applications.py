import pytest

from fastapi.testclient import TestClient
from app.main import app

import app.main as main_module

from sqlmodel import create_engine, SQLModel

from sqlmodel.pool import StaticPool

test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass= StaticPool)

@pytest.fixture
def test_db():
    main_module.engine = test_engine
    # setup: create fresh tables
    SQLModel.metadata.create_all(test_engine)
    yield
    # teardown: wipe them after the test
    SQLModel.metadata.drop_all(test_engine)

client = TestClient(app)

def test_list_applications(test_db):
    response = client.get("/applications")
    assert response.status_code == 200

def test_create_applications(test_db):
    new_app = {"company" : "test_company", "role_title" : "test_title", "status" : "applied"}
    response = client.post("/applications", json= new_app)

    assert response.status_code == 201

    response_body = response.json()
    assert response_body["company"] == new_app["company"] and response_body["role_title"] == new_app["role_title"] and response_body["status"] == new_app["status"]