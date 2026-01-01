"""
API endpoint routers.
"""

from src.api.endpoints.tasks import router as tasks_router
from src.api.endpoints.tags import router as tags_router

__all__ = ["tasks_router", "tags_router"]
