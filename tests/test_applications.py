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

def test_patch_applications(test_db):
    # create application, extract id
    new_app = {"company" : "test_company", "role_title" : "test_title", "status" : "applied"}
    app_id = client.post("/applications", json= new_app).json()["id"]

    update_data = {"status" : "offer"}

    # attempt update
    response = client.patch(f"/applications/{app_id}", json= update_data)
    response_body = response.json()

    assert response.status_code == 200

    assert response_body["status"] == update_data["status"] and response_body["company"] == new_app["company"] and response_body["role_title"] == new_app["role_title"]

def test_failed_patch(test_db):
    update_data = {"status" : "offer"}

    null_id = 999999

    response = client.patch(f"/applications/{null_id}", json= update_data)

    assert response.status_code == 404

def test_delete_applications(test_db):
    # create application, extract id
    new_app = {"company" : "test_company", "role_title" : "test_title", "status" : "applied"}
    app_id = client.post("/applications", json= new_app).json()["id"]

    # attempt delete
    response = client.delete(f"/applications/{app_id}")

    assert response.status_code == 204

    assert client.get(f"/applications/{app_id}").status_code == 404