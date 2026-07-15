"""Expose the endpoint used to check whether the application is running."""

from fastapi import APIRouter

from todo_api.models import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def get_health() -> HealthResponse:
    """Report that the application is running.

    Returns:
        A response containing the fixed healthy status.
    """
    return HealthResponse()
