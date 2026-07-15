"""Expose HTTP endpoints for listing and creating Todos."""

from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request, status

from todo_api.models import Todo, TodoCreate
from todo_api.repository import InMemoryTodoRepository

router = APIRouter(prefix="/todos", tags=["todos"])


def get_todo_repository(request: Request) -> InMemoryTodoRepository:
    """Resolve the Todo repository attached to the current application.

    Args:
        request: Incoming request whose application owns the repository.

    Returns:
        The shared in-memory repository configured by the application factory.
    """
    return cast(InMemoryTodoRepository, request.app.state.todo_repository)


# Reuse the same dependency declaration across all Todo path operations.
TodoRepositoryDep = Annotated[
    InMemoryTodoRepository,
    Depends(get_todo_repository),
]


@router.get("")
def list_todos(repository: TodoRepositoryDep) -> list[Todo]:
    """List every stored Todo in insertion order.

    Args:
        repository: Repository resolved from the current application.

    Returns:
        A snapshot of all stored Todos.
    """
    return repository.list_all()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo_create: TodoCreate, repository: TodoRepositoryDep) -> Todo:
    """Create and persist a Todo.

    Args:
        todo_create: Validated request body for the new Todo.
        repository: Repository resolved from the current application.

    Returns:
        The created Todo, including its assigned identifier.
    """
    return repository.create(todo_create)
