from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_applications():
    response = client.get("/applications")
    assert response.status_code == 200