"""Define the validated request and response models exposed by the Todo API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """Represent a successful health-check response.

    Attributes:
        status: Fixed status value indicating that the application is running.
    """

    status: Literal["ok"] = "ok"


class TodoCreate(BaseModel):
    """Represent the validated input used to create a Todo.

    Leading and trailing whitespace is removed from all string fields before
    field constraints are evaluated.

    Attributes:
        title: Non-empty Todo title containing at most 200 characters.
        completed: Whether the new Todo is already complete.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    completed: bool = False


class Todo(BaseModel):
    """Represent an immutable Todo returned by the API.

    Attributes:
        id: Positive identifier assigned by the repository.
        title: Human-readable description of the work to complete.
        completed: Whether the work has been completed.
    """

    model_config = ConfigDict(frozen=True)

    id: int = Field(ge=1)
    title: str
    completed: bool
