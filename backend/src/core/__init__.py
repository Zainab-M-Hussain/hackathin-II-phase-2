"""
Core application utilities and configuration.
"""

from src.core.config import settings
from src.core.errors import (
    TodoException,
    TaskNotFoundError,
    InvalidTaskDataError,
    DuplicateResourceError,
    DatabaseError,
    ValidationError,
    ErrorCode,
    ErrorResponse,
)

__all__ = [
    "settings",
    "TodoException",
    "TaskNotFoundError",
    "InvalidTaskDataError",
    "DuplicateResourceError",
    "DatabaseError",
    "ValidationError",
    "ErrorCode",
    "ErrorResponse",
]
