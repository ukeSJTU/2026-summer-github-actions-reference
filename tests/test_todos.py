"""Tests for Todo endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_list_todos_preserves_order_and_mixed_states(client: TestClient) -> None:
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Already done", "completed": True},
        {"id": 2, "title": "Still pending", "completed": False},
    ]


def test_create_todo_defaults_to_incomplete(client: TestClient) -> None:
    response = client.post("/todos", json={"title": "  Ship the starter  "})

    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "title": "Ship the starter",
        "completed": False,
    }


def test_create_completed_todo(client: TestClient) -> None:
    response = client.post(
        "/todos",
        json={"title": "Configure pytest", "completed": True},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "title": "Configure pytest",
        "completed": True,
    }


@pytest.mark.parametrize("title", ["", "   "])
def test_create_todo_rejects_empty_title(client: TestClient, title: str) -> None:
    response = client.post("/todos", json={"title": title})

    assert response.status_code == 422
