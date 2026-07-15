"""Provide thread-safe, in-memory persistence for Todo records."""

from collections.abc import Iterable
from threading import Lock

from todo_api.models import Todo, TodoCreate

# Seed each default repository with examples that demonstrate both Todo states.
DEFAULT_TODOS = (
    Todo(id=1, title="Learn FastAPI", completed=True),
    Todo(id=2, title="Write API tests", completed=False),
    Todo(id=3, title="Build a CI pipeline", completed=False),
)


class InMemoryTodoRepository:
    """Store Todos in memory for the lifetime of an application.

    The repository serializes reads and writes with a lock so the shared
    instance can safely serve requests from multiple worker threads.
    """

    def __init__(self, todos: Iterable[Todo] | None = None) -> None:
        """Initialize the repository and its next available identifier.

        Args:
            todos: Initial Todos to store. The default seed data is used when
                this argument is omitted; an empty iterable creates an empty
                repository.
        """
        initial_todos = DEFAULT_TODOS if todos is None else todos
        self._todos = list(initial_todos)
        self._next_id = max((todo.id for todo in self._todos), default=0) + 1
        self._lock = Lock()

    def list_all(self) -> list[Todo]:
        """Return a snapshot of all Todos in insertion order.

        Returns:
            A new list containing the currently stored Todos.
        """
        with self._lock:
            return list(self._todos)

    def create(self, todo_create: TodoCreate) -> Todo:
        """Create and store a Todo with the next available identifier.

        Args:
            todo_create: Validated values for the new Todo.

        Returns:
            The newly created and persisted Todo.
        """
        with self._lock:
            todo = Todo(id=self._next_id, **todo_create.model_dump())
            self._todos.append(todo)
            self._next_id += 1
        return todo
