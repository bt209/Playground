import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    storage.reset()


def test_welcome_and_health():
    assert client.get("/").status_code == 200
    assert client.get("/health").json() == {"status": "ok"}


def test_create_list_and_get_task():
    create_response = client.post("/tasks", json={"title": "Learn FastAPI", "completed": False})
    assert create_response.status_code == 201
    task = create_response.json()
    assert task == {"id": 1, "title": "Learn FastAPI", "completed": False}

    assert client.get("/tasks").json() == [task]
    assert client.get("/tasks/1").json() == task


def test_filter_tasks_by_completion():
    client.post("/tasks", json={"title": "Complete me", "completed": True})
    client.post("/tasks", json={"title": "Not yet", "completed": False})

    completed = client.get("/tasks", params={"completed": True}).json()
    incomplete = client.get("/tasks", params={"completed": False}).json()

    assert [task["title"] for task in completed] == ["Complete me"]
    assert [task["title"] for task in incomplete] == ["Not yet"]


def test_update_and_delete_task():
    client.post("/tasks", json={"title": "Old title"})

    update_response = client.put("/tasks/1", json={"title": "New title", "completed": True})
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "New title"

    delete_response = client.delete("/tasks/1")
    assert delete_response.status_code == 204
    assert client.get("/tasks/1").status_code == 404


def test_validation_error_and_missing_task():
    invalid_response = client.post("/tasks", json={"title": ""})
    assert invalid_response.status_code == 422
    assert client.get("/tasks/999").status_code == 404
