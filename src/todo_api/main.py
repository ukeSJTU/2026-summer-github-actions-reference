"""Create and configure the FastAPI application for the Todo API."""

from fastapi import FastAPI

from todo_api.repository import InMemoryTodoRepository
from todo_api.routers import health, todos


def create_app(repository: InMemoryTodoRepository | None = None) -> FastAPI:
    """Create a configured Todo API application.

    Args:
        repository: Repository to attach to the application. A new in-memory
            repository containing the default Todos is created when omitted.

    Returns:
        A FastAPI application with the health and Todo routers registered.
    """
    application = FastAPI(
        title="Todo API",
        description="A small API for learning CI/CD with GitHub Actions.",
        version="0.1.0",
    )
    # Store the repository on application state so request dependencies can
    # retrieve the same instance throughout this application's lifetime.
    application.state.todo_repository = (
        repository if repository is not None else InMemoryTodoRepository()
    )
    application.include_router(health.router)
    application.include_router(todos.router)
    return application


# Export a ready-to-run ASGI application for Uvicorn and other ASGI servers.
app = create_app()
