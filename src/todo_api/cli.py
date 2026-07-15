"""Provide the command-line entry point for running the Todo API server."""

import uvicorn


def main() -> None:
    """Start the Todo API locally with Uvicorn.

    The import string enables Uvicorn to load the module-level FastAPI
    application without this module importing it directly.
    """
    uvicorn.run(
        "todo_api.main:app",
        host="127.0.0.1",
        port=8000,
    )
