"""Shared test fixtures."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from todo_api.main import create_app
from todo_api.models import Todo
from todo_api.repository import InMemoryTodoRepository


@pytest.fixture
def repository() -> InMemoryTodoRepository:
    """Create an isolated repository with mixed completion states."""
    return InMemoryTodoRepository(
        [
            Todo(id=1, title="Already done", completed=True),
            Todo(id=2, title="Still pending", completed=False),
        ]
    )


@pytest.fixture
def client(repository: InMemoryTodoRepository) -> Iterator[TestClient]:
    """Create a client backed by the isolated repository."""
    with TestClient(create_app(repository)) as test_client:
        yield test_client
