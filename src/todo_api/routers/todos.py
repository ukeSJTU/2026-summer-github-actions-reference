"""Expose HTTP endpoints for listing and creating Todos."""

from typing import Annotated, cast

from fastapi import APIRouter, Depends, Query, Request, status

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
def list_todos(
    repository: TodoRepositoryDep,
    completed: Annotated[bool | None, Query()] = None,
) -> list[Todo]:
    """List stored Todos, optionally filtered by completion status.

    Args:
        repository: Repository resolved from the current application.
        completed: When provided, restrict the results to Todos whose
            `completed` field matches this value. Omitting the parameter
            returns every stored Todo in insertion order.

    Returns:
        A snapshot of the stored Todos, filtered by `completed` when given,
        preserving their original insertion order.
    """
    todos = repository.list_all()
    if completed is None:
        return todos
    return [todo for todo in todos if todo.completed == completed]


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
