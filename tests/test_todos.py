"""Tests for Todo endpoints."""

import pytest
from fastapi.testclient import TestClient

from todo_api.main import create_app
from todo_api.models import Todo
from todo_api.repository import InMemoryTodoRepository


def test_list_todos_preserves_order_and_mixed_states(client: TestClient) -> None:
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Already done", "completed": True},
        {"id": 2, "title": "Still pending", "completed": False},
    ]


def test_filter_todos_completed_true_returns_only_completed(
    client: TestClient,
) -> None:
    response = client.get("/todos", params={"completed": "true"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Already done", "completed": True},
    ]


def test_filter_todos_completed_false_returns_only_pending(
    client: TestClient,
) -> None:
    response = client.get("/todos", params={"completed": "false"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 2, "title": "Still pending", "completed": False},
    ]


def test_filter_todos_with_no_matches_returns_empty_list() -> None:
    # Every stored Todo is completed, so filtering for pending ones should
    # yield an empty list rather than 404 or null.
    repository = InMemoryTodoRepository(
        [
            Todo(id=1, title="First done", completed=True),
            Todo(id=2, title="Second done", completed=True),
        ]
    )
    with TestClient(create_app(repository)) as client:
        response = client.get("/todos", params={"completed": "false"})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("value", ["maybe", "2", ""])
def test_filter_todos_rejects_invalid_boolean(
    client: TestClient, value: str
) -> None:
    response = client.get("/todos", params={"completed": value})

    assert response.status_code == 422


def test_filter_todos_preserves_original_order_within_subset() -> None:
    # Alternating completion states across four Todos: filtering must keep
    # the matches in their original relative order, not re-sort them.
    repository = InMemoryTodoRepository(
        [
            Todo(id=1, title="First", completed=True),
            Todo(id=2, title="Second", completed=False),
            Todo(id=3, title="Third", completed=True),
            Todo(id=4, title="Fourth", completed=False),
        ]
    )
    with TestClient(create_app(repository)) as client:
        response = client.get("/todos", params={"completed": "true"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "First", "completed": True},
        {"id": 3, "title": "Third", "completed": True},
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
